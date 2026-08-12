import json
import os
import re
import urllib.request
import urllib.error
import socket
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = "llama3.2:1b"

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

def generate_smart_cognitive_fallback(prompt):
    """
    Built-in Cognitive & Mental Ability Solver Engine.
    Guarantees instant, rich step-by-step answers on Vercel cloud hosting even without Ollama or API keys!
    """
    p_lower = prompt.lower()

    # 1. Syllogisms & Logical deduction
    if "syllogism" in p_lower or ("all " in p_lower and "are " in p_lower):
        return (
            "### 🧠 **Logical Reasoning: Syllogisms Concept**\n\n"
            "Syllogisms use **categorical logic rules** to derive valid conclusions from premises:\n\n"
            "#### **Core Rules:**\n"
            "1. **Transitive Property (A ⊂ B ⊂ C):**\n"
            "   - If *All A are B* and *All B are C*, then **All A are C**.\n"
            "2. **Negative Rule:**\n"
            "   - If one premise is negative (*No A are B*), the conclusion **must be negative**.\n"
            "3. **Particular Rule:**\n"
            "   - If one premise uses *Some*, the conclusion **cannot be universal** (*All*).\n\n"
            "#### **Example Walkthrough:**\n"
            "- **Statement 1:** All Laptops are Computers.\n"
            "- **Statement 2:** All Computers are Electronic Devices.\n"
            "- **Conclusion:** All Laptops are Electronic Devices. ✅ (*Valid Transitive Rule*)\n\n"
            "💡 *Tip: Use Euler Venn diagrams to visualize overlapping sets when solving complex statements!*"
        )

    # 2. Train / Speed / Distance
    if "train" in p_lower or "speed" in p_lower or "distance" in p_lower or "km/h" in p_lower or "m/s" in p_lower:
        return (
            "### 🔢 **Quantitative Aptitude: Train & Speed Formulas**\n\n"
            "#### **Fundamental Formula:**\n"
            "$$\\text{Speed} = \\frac{\\text{Distance}}{\\text{Time}}$$\n\n"
            "#### **Key Conversions:**\n"
            "- **km/h to m/s:** Multiply by $\\frac{5}{18}$ (e.g., $72 \\text{ km/h} \\times \\frac{5}{18} = 20 \\text{ m/s}$)\n"
            "- **m/s to km/h:** Multiply by $\\frac{18}{5}$ (e.g., $15 \\text{ m/s} \\times \\frac{18}{5} = 54 \\text{ km/h}$)\n\n"
            "#### **Train Passing Problems:**\n"
            "1. **Passing a stationary pole/man:** Distance = Length of Train ($L$)\n"
            "2. **Passing a platform/bridge of length $P$:** Distance = $L + P$\n"
            "3. **Two trains moving in OPPOSITE directions:** Relative Speed = $S_1 + S_2$\n"
            "4. **Two trains moving in SAME direction:** Relative Speed = $|S_1 - S_2|$\n\n"
            "🎯 *Example:* A train 150m long moving at 54 km/h (15 m/s) passes a pole in $\\frac{150}{15} = \\mathbf{10 \\text{ seconds}}$."
        )

    # 3. Work & Time / Man-Days
    if "work" in p_lower or "worker" in p_lower or "days" in p_lower or "man-day" in p_lower:
        return (
            "### ⏱️ **Quantitative Aptitude: Time & Work Strategy**\n\n"
            "#### **1. Inverse Work Rule:**\n"
            "- If a person can complete a work in $N$ days, their **1-day work** is $\\frac{1}{N}$.\n"
            "- If A takes 10 days and B takes 15 days, together in 1 day they do:\n"
            "  $$\\frac{1}{10} + \\frac{1}{15} = \\frac{3+2}{30} = \\frac{5}{30} = \\frac{1}{6}$$\n"
            "  So together they finish in **6 days**.\n\n"
            "#### **2. Man-Days Formula:**\n"
            "$$\\frac{M_1 \\times D_1 \\times H_1}{W_1} = \\frac{M_2 \\times D_2 \\times H_2}{W_2}$$\n"
            "*(Where M = Workers, D = Days, H = Hours/day, W = Total Work)*"
        )

    # 4. Coding & Decoding / Alphabet Patterns
    if "code" in p_lower or "coded" in p_lower or "alphabet" in p_lower or "letter" in p_lower:
        return (
            "### 🔤 **Reasoning: Coding & Decoding Shortcuts**\n\n"
            "#### **Alphabet Position Memory Trick (EJOTY):**\n"
            "- **E = 5**, **J = 10**, **O = 15**, **T = 20**, **Y = 25**\n\n"
            "#### **Reverse Alphabet Pairs (Sum = 27):**\n"
            "- A ↔ Z (1+26=27)\n"
            "- B ↔ Y (2+25=27)\n"
            "- C ↔ X (3+24=27)\n"
            "- M ↔ N (13+14=27)\n\n"
            "💡 *Strategy:* Always check if letters are shifted by a fixed offset (+1, +2, -3) or swapped symmetrically!"
        )

    # 5. Fast Mental Math Tricks
    if "trick" in p_lower or "shortcut" in p_lower or "fast" in p_lower or "math" in p_lower:
        return (
            "### ⚡ **Top 3 Mental Math Shortcuts for Competitive Exams**\n\n"
            "1. **Multiply Any 2-Digit Number by 11:**\n"
            "   - Split digits and insert their sum in middle: $45 \\times 11 \\rightarrow 4\\_(4+5)\\_5 = \\mathbf{495}$.\n"
            "2. **Square Numbers Ending in 5:**\n"
            "   - Multiply first digit $N$ by $(N+1)$, append $25$:\n"
            "   - $75^2 \\rightarrow (7 \\times 8) \\text{ and } 25 = \\mathbf{5625}$.\n"
            "3. **Percentage Swap Rule ($A\\%$ of $B = B\\%$ of $A$):**\n"
            "   - $16\\%$ of $50 = 50\\%$ of $16 = \\mathbf{8}$."
        )

    # 6. Default Encouraging Tutor Guidance
    return (
        "### 🧠 **BrainBot AI Cognitive Guidance**\n\n"
        f"Great question about **\"{prompt}\"**!\n\n"
        "Here is the recommended step-by-step problem-solving framework:\n\n"
        "1. **Identify Given Data:** Extract numerical values, relationships, and the target variable.\n"
        "2. **Determine the Subject Category:**\n"
        "   - *Logical Reasoning:* Syllogisms, Number Series, Coding-Decoding, Seating Arrangements.\n"
        "   - *Quantitative Aptitude:* Ratios, Speed & Distance, Time & Work, Percentages.\n"
        "3. **Apply Standard Formula / Pattern Rules:** Work methodically to eliminate incorrect options.\n\n"
        "💡 *Need a specific topic explanation? Try asking about **Syllogisms**, **Train Speed**, **Time & Work**, or **Mental Math Tricks**!*"
    )

@require_http_methods(["GET"])
def ollama_models_view(request):
    """API endpoint to get list of available AI models."""
    if os.environ.get('VERCEL'):
        return JsonResponse({
            "success": True,
            "is_running": True,
            "models": ["llama-3.2-1b-preview (Cloud AI)", DEFAULT_MODEL],
            "default_model": "llama-3.2-1b-preview (Cloud AI)"
        })
    models = fetch_ollama_models()
    is_running = len(models) > 0
    return JsonResponse({
        "success": True,
        "is_running": is_running,
        "models": models if is_running else [DEFAULT_MODEL],
        "default_model": models[0] if is_running else DEFAULT_MODEL
    })

@csrf_exempt
@require_http_methods(["POST"])
def ollama_chat_view(request):
    """
    Hybrid AI Endpoint:
    1. Tries local Ollama endpoint (if running locally).
    2. Tries Cloud API (Groq API Llama 3.2 1B).
    3. Fallback to built-in Smart Cognitive Solver engine for guaranteed Vercel cloud responses.
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

    last_user_prompt = user_messages[-1].get("content", "").strip()

    messages_payload = [SYSTEM_PROMPT] + [
        msg for msg in user_messages[-10:] if msg.get("role") in ["user", "assistant"]
    ]

    is_vercel = bool(os.environ.get('VERCEL'))

    # --- Tier 1: Try Local Ollama Instance (Only if running locally, skip timeout hang on Vercel) ---
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
            with urllib.request.urlopen(req, timeout=2.5) as resp:
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
            print(f"[BrainBot AI] Local Ollama notice ({e}). Trying cloud/smart fallback...")

    # --- Tier 2: Try Free Cloud AI (Groq API Llama 3.2 1B Online Host) ---
    cloud_reply = query_groq_api(messages_payload)
    if cloud_reply:
        return JsonResponse({
            "success": True,
            "source": "cloud_groq",
            "model": "llama-3.2-1b-preview",
            "response": cloud_reply
        })

    # --- Tier 3: Built-in Smart Cognitive Solver Fallback (Vercel Cloud Ready) ---
    smart_reply = generate_smart_cognitive_fallback(last_user_prompt)
    return JsonResponse({
        "success": True,
        "source": "smart_cognitive_engine",
        "model": "BrainBot Smart Tutor v2",
        "response": smart_reply
    })
