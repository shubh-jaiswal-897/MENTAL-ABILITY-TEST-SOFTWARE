import os
import json
import urllib.request
import re
from pypdf import PdfReader
from docx import Document
from openai import OpenAI
from django.conf import settings

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY environment variable is not set. AI exam generation will fail or use fallback.")
        return None
    return OpenAI(api_key=api_key)

def extract_text_from_file(file_path):
    """Extracts text from PDF, DOCX, or TXT files."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    try:
        if ext == '.pdf':
            reader = PdfReader(file_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        elif ext == '.docx':
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
    return text

import os
import json
from openai import OpenAI

def generate_mcqs_from_text(text, title="", num_questions=5, use_internet=True):
    """
    Uses OpenAI to generate MCQs from the given text using the provided API key.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "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")
    
    prompt = f"""
    You are an expert educator and assessor. Your task is to generate exactly {num_questions} accurate, high-quality multiple-choice questions strictly based on the following text. 
    Do NOT include any external facts or assumptions not present in the text.
    Each question must be unambiguous, have exactly 4 choices (A, B, C, D), and have only one clearly correct choice.
    Return the output STRICTLY as a JSON list of objects, without any markdown formatting or extra text.
    Each object should have the following exact keys:
    - "question_text"
    - "choice_a"
    - "choice_b"
    - "choice_c"
    - "choice_d"
    - "correct_choice" (must be strictly "A", "B", "C", or "D")

    Source Text:
    {text[:10000]}
    """

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You output JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        
        if isinstance(data, dict):
            for key in data:
                if isinstance(data[key], list):
                    return data[key], None
            return [], "Could not find a list of questions in the AI response."
        elif isinstance(data, list):
            return data, None
            
    except Exception as e:
        print(f"OpenAI Error: {e}")
        
        # Fallback 1: Local Ollama AI (Reads PDF Content)
        print("Falling back to local Ollama AI to read PDF content...")
        import urllib.request
        try:
            available_model = "llama3.1:latest"
            try:
                req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
                with urllib.request.urlopen(req, timeout=3.0) as resp:
                    if resp.status == 200:
                        tags_data = json.loads(resp.read().decode("utf-8"))
                        models = [m.get("name") for m in tags_data.get("models", []) if m.get("name")]
                        if models:
                            preferred = [m for m in models if 'llama' in m or 'mistral' in m or 'qwen' in m]
                            available_model = preferred[0] if preferred else models[0]
            except:
                pass
                
            payload = {
                "model": available_model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "format": "json"
            }
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                "http://127.0.0.1:11434/api/chat",
                data=req_data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=120.0) as resp:
                if resp.status == 200:
                    resp_json = json.loads(resp.read().decode("utf-8"))
                    content = resp_json.get("message", {}).get("content", "").strip()
                    
                    # Manual JSON extraction for Ollama
                    try:
                        import re
                        match = re.search(r'\[.*\]', content, re.DOTALL)
                        if match:
                            data = json.loads(match.group(0))
                        else:
                            data = json.loads(content)
                            
                        if isinstance(data, dict):
                            for key in data:
                                if isinstance(data[key], list):
                                    return data[key], None
                        elif isinstance(data, list):
                            return data, None
                    except:
                        pass
        except Exception as ollama_e:
            print(f"Ollama failed: {ollama_e}")
            
        print("Falling back to free internet database (OpenTDB) as final resort...")
        
        # Fallback to OpenTDB
        import html
        import random
        import requests
        
        title_lower = title.lower() if title else ""
        category = "9"  # Default: General Knowledge
        if "computer" in title_lower or "web" in title_lower or "html" in title_lower or "tech" in title_lower:
            category = "18"
        elif "math" in title_lower:
            category = "19"
        elif "history" in title_lower:
            category = "23"
        elif "geography" in title_lower:
            category = "22"
        elif "science" in title_lower:
            category = "17"
            
        url = f"https://opentdb.com/api.php?amount={num_questions}&category={category}&type=multiple"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("response_code") == 0:
                    results = data.get("results", [])
                    questions = []
                    for r in results:
                        q_text = html.unescape(r['question'])
                        correct = html.unescape(r['correct_answer'])
                        incorrect = [html.unescape(ans) for ans in r['incorrect_answers']]
                        all_choices = incorrect + [correct]
                        random.shuffle(all_choices)
                        letters = ['A', 'B', 'C', 'D']
                        correct_letter = letters[all_choices.index(correct)]
                        
                        questions.append({
                            "question_text": q_text,
                            "choice_a": all_choices[0] if len(all_choices) > 0 else "N/A",
                            "choice_b": all_choices[1] if len(all_choices) > 1 else "N/A",
                            "choice_c": all_choices[2] if len(all_choices) > 2 else "N/A",
                            "choice_d": all_choices[3] if len(all_choices) > 3 else "N/A",
                            "correct_choice": correct_letter
                        })
                    return questions, None
            return [], f"OpenAI failed ({str(e)}) and fallback internet database also failed."
        except Exception as fallback_e:
            return [], f"OpenAI failed ({str(e)}) and fallback failed: {str(fallback_e)}"
