import json
import os
import re
import html
import urllib.request
import urllib.parse
import urllib.error
import socket
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from quiz.models import Question, Subject, Choice, UserProfile, TestAttempt, Contest, GoodieItem

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = "brain-ai"

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are BrainBot AI, a friendly and highly knowledgeable Cognitive & Mental Ability tutor built into "
        "the Mental Ability Test Software platform. Your role is to help users master logical reasoning, "
        "quantitative aptitude, verbal analogies, pattern recognition, spatial reasoning, math puzzles, and competitive exam questions. "
        "Provide clear, step-by-step explanations, helpful formulas, shortcuts, and encouraging responses. "
        "Use Markdown formatting (bolding, lists, code snippets) to make answers structured and easy to read."
    )
}

STOP_WORDS = {"what", "is", "how", "the", "a", "an", "to", "in", "for", "on", "of", "and", "or", "tell", "me", "about", "give", "explain", "find", "solve", "question", "with", "can", "you", "show", "please", "my"}

def search_google_web(query):
    """
    Live Web Search Engine:
    Performs real-time web search over the internet and extracts top search snippets & facts.
    """
    snippets = []
    if not query or len(query.strip()) < 2:
        return snippets

    try:
        q_encoded = urllib.parse.quote(query.strip())
        req = urllib.request.Request(
            'https://lite.duckduckgo.com/lite/',
            data=f'q={q_encoded}'.encode('utf-8'),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r"class='result-snippet'>(.*?)</td>", content, re.DOTALL)
            for m in matches[:4]:
                clean_text = html.unescape(re.sub(r'<[^>]+>', '', m)).strip()
                if clean_text and clean_text not in snippets:
                    snippets.append(clean_text)
    except Exception as e:
        print(f"[Brain AI Web Search Notice] {e}")

    return snippets


def retrieve_rag_context(prompt, user=None):
    """
    RAG Retrieval Engine:
    Searches local SQLite database for matching Questions, Explanations, Subjects, User Stats, and Contests/Goodies.
    """
    context_blocks = []
    retrieved_questions = []

    if not prompt:
        return "", []

    p_clean = prompt.strip()
    p_lower = p_clean.lower()

    # --- 1. User Profile & Account Data RAG ---
    user_stats_str = ""
    if user and user.is_authenticated and hasattr(user, 'profile'):
        prof = user.profile
        recent_attempt = TestAttempt.objects.filter(user=user).order_by('-started_at').first()
        recent_str = f"Last Score: {recent_attempt.score}/{recent_attempt.total} ({recent_attempt.percentage}%)" if recent_attempt else "No quiz attempts yet"
        user_stats_str = f"User: {user.username} | Streak: {prof.streak_count}🔥 | Total XP: {prof.total_xp}⚡ | Rank: {prof.rank_title} 👑 | Solved Questions: {prof.solved_questions_count} | {recent_str}"
        context_blocks.append(f"• User Profile Info: {user_stats_str}")

    # --- 2. Contests / Goodies RAG Retrieval ---
    if any(k in p_lower for k in ["contest", "tournament", "competition", "weekly", "monthly", "challenge"]):
        contests = Contest.objects.all()[:3]
        c_strs = [f"'{c.title}' (Type: {c.get_contest_type_display()}, XP Prize: {c.xp_prize} XP, Duration: {c.duration_minutes}m)" for c in contests]
        if c_strs:
            context_blocks.append(f"• Platform Contests: {'; '.join(c_strs)}")

    if any(k in p_lower for k in ["goodie", "reward", "coin", "store", "shop", "item", "redeem"]):
        goodies = GoodieItem.objects.all()[:4]
        g_strs = [f"'{g.name}' (Cost: {g.coin_cost} XP, Stock: {g.stock})" for g in goodies]
        if g_strs:
            context_blocks.append(f"• Goodies Reward Store: {'; '.join(g_strs)}")

    # --- 3. Database Question Search RAG ---
    words = [w for w in re.findall(r'\w+', p_lower) if w not in STOP_WORDS and len(w) > 2]
    query = Q()
    for w in words[:6]:
        query |= Q(text__icontains=w) | Q(explanation__icontains=w) | Q(subject__name__icontains=w)

    if words:
        qs = Question.objects.filter(query).select_related('subject').prefetch_related('choices').distinct()[:3]
        for q in qs:
            choices_list = [f"{c.text}{' ✅(Correct)' if c.is_correct else ''}" for c in q.choices.all()]
            choices_str = " | ".join(choices_list) if choices_list else "No options"
            retrieved_questions.append({
                "id": q.id,
                "text": q.text,
                "subject": q.subject.name if q.subject else "General Aptitude",
                "difficulty": q.difficulty,
                "explanation": q.explanation,
                "choices": choices_str
            })
            context_blocks.append(
                f"• Database Question #{q.id} [{q.subject.name if q.subject else 'General'} | {q.difficulty}]:\n"
                f"  Text: {q.text}\n"
                f"  Options: {choices_str}\n"
                f"  Explanation: {q.explanation}"
            )

    rag_context_text = "\n".join(context_blocks)
    return rag_context_text, retrieved_questions


def fetch_ollama_models():
    """Queries local Ollama instance for list of available models."""
    try:
        req = urllib.request.Request(
            f"{OLLAMA_BASE_URL}/api/tags",
            headers={"User-Agent": "MentalAbilityTestSoftware/1.0"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("name") for m in data.get("models", []) if m.get("name")]
                return models
    except Exception:
        pass
    return []


def query_groq_api(messages_payload, model="llama-3.2-1b-preview"):
    """Cloud AI online hosting using free Groq API (Llama 3.2 1B Cloud)."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None

    try:
        payload = {
            "model": model,
            "messages": messages_payload,
            "max_tokens": 512,
            "temperature": 0.7
        }
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=req_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "MentalAbilityTestSoftware/1.0"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                res_data = json.loads(resp.read().decode("utf-8"))
                choices = res_data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "")
    except Exception as e:
        print(f"[BrainBot AI] Groq API Notice: {e}")
    return None


def generate_smart_cognitive_fallback(prompt, rag_context_str="", retrieved_qs=None, user=None, web_snippets=None):
    """
    RAG-Augmented Cognitive & Live Web Search AI Engine.
    Combines live web search results, SQLite database retrieval, dynamic calculations, and logic solving.
    """
    if not prompt:
        return "Hello! I am **Brain AI**. Ask me any mental ability, reasoning, or aptitude question!"

    p_clean = prompt.strip()
    p_lower = p_clean.lower()

    # User performance / profile query
    if user and user.is_authenticated and hasattr(user, 'profile') and any(k in p_lower for k in ["my profile", "my xp", "my streak", "my rank", "my score", "my stats", "who am i"]):
        prof = user.profile
        recent_attempt = TestAttempt.objects.filter(user=user).order_by('-started_at').first()
        recent_str = f"**{recent_attempt.score}/{recent_attempt.total}** ({recent_attempt.percentage}%)" if recent_attempt else "No attempts recorded yet"
        return (
            f"### 👤 **Your Live Database Performance Stats**\n\n"
            f"- **Username:** `{user.username}`\n"
            f"- **Daily Streak:** 🔥 **{prof.streak_count} Days**\n"
            f"- **Total XP Earned:** ⚡ **{prof.total_xp} XP**\n"
            f"- **Current Rank Title:** 👑 **{prof.rank_title}**\n"
            f"- **Solved Questions:** 🎯 **{prof.solved_questions_count}**\n"
            f"- **Latest Test Result:** {recent_str}\n\n"
            "Keep up the daily practice to earn more XP and level up your rank!"
        )

    # 1. Live Web Search Result Presentation
    if web_snippets:
        web_blocks = "\n\n".join([f"• {s}" for s in web_snippets[:3]])
        db_block = ""
        if retrieved_qs:
            q_match = retrieved_qs[0]
            db_block = (
                f"\n\n#### 📌 **Related Database Question Match:**\n"
                f"**Question:** {q_match['text']} (Subject: *{q_match['subject']}*)\n"
                f"**Options:** {q_match['choices']}\n"
                f"**Explanation:** {q_match['explanation']}"
            )

        return (
            f"### 🌐 **Live Web Search & AI Explanation**\n\n"
            f"**Query:** *\"{p_clean}\"*\n\n"
            f"#### 🌐 **Web Search Results:**\n"
            f"{web_blocks}"
            f"{db_block}\n\n"
            f"💡 *Fetched live over the internet to answer your query!*"
        )

    # 2. RAG Question Match from Database
    if retrieved_qs:
        q_match = retrieved_qs[0]
        return (
            f"### 🔍 **RAG Knowledge Base Result (Database Match)**\n\n"
            f"Found relevant question from **{q_match['subject']}** (Difficulty: `{q_match['difficulty']}`):\n\n"
            f"**Question:** {q_match['text']}\n\n"
            f"#### **Options & Correct Answer:**\n"
            f"{q_match['choices']}\n\n"
            f"#### **Step-by-Step Explanation:**\n"
            f"{q_match['explanation']}\n\n"
            f"💡 *Retrieved from local Database Question #{q_match['id']}!*"
        )

    # 3. Percentage calculation
    pct_match = re.search(r'(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)', p_lower) or \
                re.search(r'(\d+(?:\.\d+)?)\s*percent(?:age)?\s*of\s*(\d+(?:\.\d+)?)', p_lower)
    if pct_match:
        pct_val = float(pct_match.group(1))
        total_val = float(pct_match.group(2))
        res = (pct_val * total_val) / 100.0
        res_str = f"{res:g}"
        return (
            f"### 🔢 **Percentage Solution**\n\n"
            f"**Question:** What is **{pct_val}% of {total_val}**?\n\n"
            f"#### **Step-by-Step Calculation:**\n"
            f"1. **Formula:** $\\text{{Result}} = \\frac{{\\text{{Percentage}} \\times \\text{{Base}}}}{{100}}$\n"
            f"2. **Substitute values:** $\\frac{{{pct_val} \\times {total_val}}}{{100}}$\n"
            f"3. **Compute:** $\\frac{{{pct_val * total_val}}}{{100}} = \\mathbf{{{res_str}}}$\n\n"
            f"🎯 **Final Answer:** **{res_str}**"
        )

    # 4. Arithmetic Math Evaluation
    math_match = re.search(r'^(\d+(?:\.\d+)?)\s*([\+\-\*/\^])\s*(\d+(?:\.\d+)?)$', p_clean)
    if math_match:
        n1 = float(math_match.group(1))
        op = math_match.group(2)
        n2 = float(math_match.group(3))
        res = None
        if op == '+': res = n1 + n2
        elif op == '-': res = n1 - n2
        elif op == '*': res = n1 * n2
        elif op == '/' and n2 != 0: res = n1 / n2
        elif op == '^': res = n1 ** n2

        if res is not None:
            res_str = f"{res:g}"
            return (
                f"### ⚡ **Math Calculation**\n\n"
                f"**Expression:** `{n1} {op} {n2}`\n\n"
                f"$$\\mathbf{{{n1} {op} {n2} = {res_str}}}$$\n\n"
                f"🎯 **Answer:** **{res_str}**"
            )

    # 5. Syllogisms & Categorical Logic
    if "syllogism" in p_lower or ("all " in p_lower and "are " in p_lower) or ("some " in p_lower and "are " in p_lower):
        return (
            "### 🧠 **Logical Reasoning: Syllogisms & Categorical Logic**\n\n"
            "Syllogisms use **logical rules** to evaluate conclusions from given statements:\n\n"
            "#### **Core Rules:**\n"
            "1. **Transitive Property:** If *All A are B* and *All B are C*, then **All A are C**.\n"
            "2. **Negative Rule:** If any premise is negative (*No A are B*), the conclusion must be negative.\n"
            "3. **Particular Rule:** If a premise uses *Some*, the conclusion cannot be universal (*All*).\n\n"
            "#### **Walkthrough Example:**\n"
            "- **Statement 1:** All Laptops are Computers.\n"
            "- **Statement 2:** All Computers are Electronic Devices.\n"
            "- **Valid Conclusion:** All Laptops are Electronic Devices ✅\n\n"
            "💡 *Tip: Draw Euler Venn diagrams to visualize overlapping sets clearly!*"
        )

    # 6. Speed, Distance & Time
    if "train" in p_lower or "speed" in p_lower or "distance" in p_lower or "km/h" in p_lower or "m/s" in p_lower:
        return (
            "### 🔢 **Quantitative Aptitude: Speed, Distance & Time**\n\n"
            "#### **Core Formula:**\n"
            "$$\\text{Speed} = \\frac{\\text{Distance}}{\\text{Time}} \\quad | \\quad \\text{Time} = \\frac{\\text{Distance}}{\\text{Speed}} \\quad | \\quad \\text{Distance} = \\text{Speed} \\times \\text{Time}$$\n\n"
            "#### **Unit Conversions:**\n"
            "- **km/h to m/s:** Multiply by $\\frac{5}{18}$ (e.g., $72 \\text{ km/h} = 72 \\times \\frac{5}{18} = 20 \\text{ m/s}$)\n"
            "- **m/s to km/h:** Multiply by $\\frac{18}{5}$ (e.g., $15 \\text{ m/s} = 15 \\times \\frac{18}{5} = 54 \\text{ km/h}$)\n\n"
            "#### **Train Special Cases:**\n"
            "- **Passing a pole/man:** Distance = Length of Train ($L$).\n"
            "- **Passing a platform:** Distance = Length of Train ($L$) + Platform ($P$).\n"
            "- **Opposite directions:** Relative Speed = $S_1 + S_2$.\n"
            "- **Same direction:** Relative Speed = $|S_1 - S_2|$."
        )

    # 7. Time & Work
    if "work" in p_lower or "worker" in p_lower or "man-day" in p_lower or "days" in p_lower:
        return (
            "### ⏱️ **Time & Work Strategy**\n\n"
            "#### **1. Unit Work Rate:**\n"
            "- If A completes a job in $N$ days, A's 1-day work rate is $\\frac{1}{N}$.\n"
            "- If A takes 10 days and B takes 15 days, together in 1 day:\n"
            "  $$\\frac{1}{10} + \\frac{1}{15} = \\frac{3+2}{30} = \\frac{5}{30} = \\frac{1}{6}$$\n"
            "  Together they finish in **6 days**.\n\n"
            "#### **2. Man-Days Formula:**\n"
            "$$\\frac{M_1 \\times D_1 \\times H_1}{W_1} = \\frac{M_2 \\times D_2 \\times H_2}{W_2}$$\n"
            "*(M = Workers, D = Days, H = Hours, W = Work)*"
        )

    # 8. Coding & Decoding
    if "code" in p_lower or "coded" in p_lower or "alphabet" in p_lower or "letter" in p_lower:
        return (
            "### 🔤 **Reasoning: Coding & Decoding Shortcuts**\n\n"
            "#### **Alphabet Position Trick (EJOTY):**\n"
            "- **E = 5**, **J = 10**, **O = 15**, **T = 20**, **Y = 25**\n\n"
            "#### **Opposite Letter Pairs (Sum = 27):**\n"
            "- **A ↔ Z** (1+26=27)\n"
            "- **B ↔ Y** (2+25=27)\n"
            "- **C ↔ X** (3+24=27)\n"
            "- **M ↔ N** (13+14=27)\n\n"
            "💡 *Check if letters are shifted by $+k$ / $-k$ or reversed symmetrically!*"
        )

    # 9. Fast Mental Math
    if "trick" in p_lower or "shortcut" in p_lower or "fast" in p_lower or "math" in p_lower:
        return (
            "### ⚡ **Top 3 Mental Math Shortcuts**\n\n"
            "1. **Multiply Any 2-Digit Number by 11:**\n"
            "   - Insert sum of digits in middle: $45 \\times 11 \\rightarrow 4\\_(4+5)\\_5 = \\mathbf{495}$.\n"
            "2. **Square Numbers Ending in 5:**\n"
            "   - Multiply first digit $N$ by $(N+1)$ and append $25$:\n"
            "   - $75^2 \\rightarrow (7 \\times 8) \\text{ and } 25 = \\mathbf{5625}$.\n"
            "3. **Percentage Swap Rule:**\n"
            "   - $A\\%$ of $B = B\\%$ of $A$ (e.g., $16\\%$ of $50 = 50\\%$ of $16 = \\mathbf{8}$)."
        )

    # 10. Dynamic General Tutor Guidance for Any Query
    return (
        f"### 🧠 **Brain AI Tutor Explanation**\n\n"
        f"Regarding your query **\"{p_clean}\"**:\n\n"
        "#### 📝 **Methodology & Step-by-Step Approach:**\n"
        "1. **Identify Key Variables:** Parse given data, figures, and conditions.\n"
        "2. **Determine Subject Category:**\n"
        "   - **Quantitative Aptitude:** Arithmetic, Percentages, Ratios, Speed & Work.\n"
        "   - **Logical Reasoning:** Syllogisms, Series, Coding Shift, Venn Diagrams.\n"
        "3. **Solve & Verify:** Apply relevant mathematical or logical formulas step-by-step.\n\n"
        "💡 *Tip: Try asking specific questions like **\"15% of 400\"**, **\"Train speed formula\"**, **\"Syllogism rules\"**, or search for any problem in your database!*"
    )


@require_http_methods(["GET"])
def ollama_models_view(request):
    """API endpoint to get list of available AI models."""
    if os.environ.get('VERCEL'):
        return JsonResponse({
            "success": True,
            "is_running": True,
            "models": ["Brain AI Web & RAG Engine", DEFAULT_MODEL],
            "default_model": "Brain AI Web & RAG Engine"
        })
    models = fetch_ollama_models()
    is_running = len(models) > 0
    return JsonResponse({
        "success": True,
        "is_running": is_running,
        "models": models if is_running else ["Brain AI Web & RAG Engine"],
        "default_model": models[0] if is_running else "Brain AI Web & RAG Engine"
    })


@csrf_exempt
@require_http_methods(["POST"])
def ollama_chat_view(request):
    """
    Web-Search & RAG-Augmented AI Endpoint:
    1. Performs real-time Live Web Search over the internet for top search results.
    2. Retrieves relevant Questions, Choices, User Stats, Contests from local SQLite Database.
    3. Augments LLM System prompt with Web Search & RAG context payloads.
    4. Tries Local Ollama -> Groq Cloud API -> Web & RAG Cognitive Solver Engine.
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"success": False, "error": "Invalid JSON request body."}, status=400)

    user_messages = data.get("messages", [])
    user_prompt = data.get("prompt", "").strip()
    selected_model = data.get("model", "").strip() or DEFAULT_MODEL

    if not user_messages and user_prompt:
        user_messages = [{"role": "user", "content": user_prompt}]

    if not user_messages:
        return JsonResponse({"success": False, "error": "No prompt or message history provided."}, status=400)

    last_user_prompt = user_messages[-1].get("content", "").strip() if user_messages else ""
    user = request.user if hasattr(request, 'user') else None

    # --- Step 1: Execute Live Web Search on Internet ---
    web_snippets = search_google_web(last_user_prompt)

    # --- Step 2: Execute RAG Retrieval from local SQLite database ---
    rag_context_str, retrieved_qs = retrieve_rag_context(last_user_prompt, user)

    # --- Step 3: Augment System Prompt with Live Web Search & RAG Context ---
    augmented_system = SYSTEM_PROMPT.copy()
    context_additions = []

    if web_snippets:
        web_text = "\n".join([f"• {s}" for s in web_snippets])
        context_additions.append(f"[LIVE WEB SEARCH RESULTS FROM INTERNET]\n{web_text}")

    if rag_context_str:
        context_additions.append(f"[RELEVANT LOCAL DATABASE KNOWLEDGE CONTEXT (RAG)]\n{rag_context_str}")

    if context_additions:
        augmented_system["content"] += (
            "\n\n" + "\n\n".join(context_additions) +
            "\n\nUse the above live web search results and database facts to provide exact, authoritative, step-by-step answers."
        )

    messages_payload = [augmented_system] + [
        msg for msg in user_messages[-10:] if msg.get("role") in ["user", "assistant"]
    ]

    is_vercel = bool(os.environ.get('VERCEL'))

    # --- Tier 1: Try Local Ollama Instance ---
    if not is_vercel:
        try:
            payload = {
                "model": selected_model,
                "messages": messages_payload,
                "stream": False,
                "options": {
                    "num_predict": 450,
                    "temperature": 0.7
                }
            }
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{OLLAMA_BASE_URL}/api/chat",
                data=req_data,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "MentalAbilityTestSoftware/1.0"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                if resp.status == 200:
                    resp_json = json.loads(resp.read().decode("utf-8"))
                    content = resp_json.get("message", {}).get("content", "").strip()
                    if content:
                        return JsonResponse({
                            "success": True,
                            "source": "ollama_local",
                            "model": selected_model,
                            "response": content
                        })
        except Exception as e:
            print(f"[BrainBot AI] Local Ollama notice ({e}). Trying cloud/smart RAG fallback...")

    # --- Tier 2: Try Free Cloud API (Groq API Llama 3.2 1B Cloud) ---
    cloud_reply = query_groq_api(messages_payload)
    if cloud_reply:
        return JsonResponse({
            "success": True,
            "source": "cloud_groq",
            "model": "llama-3.2-1b-preview (Web & RAG Augmented)",
            "response": cloud_reply
        })

    # --- Tier 3: Live Web Search & RAG Smart Cognitive Solver Engine ---
    smart_reply = generate_smart_cognitive_fallback(
        last_user_prompt,
        rag_context_str=rag_context_str,
        retrieved_qs=retrieved_qs,
        user=user,
        web_snippets=web_snippets
    )
    return JsonResponse({
        "success": True,
        "source": "web_rag_smart_engine",
        "model": "Brain AI Web & RAG Engine v4",
        "response": smart_reply
    })
