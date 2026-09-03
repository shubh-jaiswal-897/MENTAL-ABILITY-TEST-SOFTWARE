import random
import urllib.request
import json
import html
from quiz.models import Subject, Question, Choice

def _gen_number_series():
    diff = random.choice([3, 5, 7, 9])
    start = random.randint(10, 50)
    v1 = start + diff
    v2 = v1 + diff + 2
    v3 = v2 + diff + 4
    ans = v3 + diff + 6
    return {
        "text": f"Complete the logical number sequence: {start}, {v1}, {v2}, {v3}, ?",
        "explanation": f"The pattern increases difference by +2 each step: +{diff}, +{diff+2}, +{diff+4}, +{diff+6}.",
        "correct": str(ans),
        "wrongs": [str(ans + 2), str(ans - 4), str(ans + 5)]
    }

def _gen_coding_decoding():
    word = random.choice(["BRAIN", "LOGIC", "SMART", "FLASH"])
    shift = random.choice([1, 2, 3])
    code = "".join([chr((ord(c) - 65 + shift) % 26 + 65) for c in word])
    word2 = random.choice(["MIND", "DATA", "CODE", "NODE"])
    ans = "".join([chr((ord(c) - 65 + shift) % 26 + 65) for c in word2])
    w1 = "".join([chr((ord(c) - 65 + shift + 1) % 26 + 65) for c in word2])
    w2 = "".join([chr((ord(c) - 65 + max(1, shift - 1)) % 26 + 65) for c in word2])
    w3 = "".join([chr((ord(c) - 65 + shift + 2) % 26 + 65) for c in word2])
    return {
        "text": f"Coding & Decoding: If '{word}' is coded as '{code}', how is '{word2}' coded?",
        "explanation": f"Each letter is shifted forward by +{shift} in the alphabet.",
        "correct": ans,
        "wrongs": [w1, w2, w3]
    }

def _gen_train_speed():
    length = random.choice([120, 150, 180, 240])
    seconds = random.choice([10, 12, 15, 20])
    speed_ms = length / seconds
    ans_kmh = int(speed_ms * 3.6)
    return {
        "text": f"A train {length} meters long passes a signal post in {seconds} seconds. What is the speed of the train in km/h?",
        "explanation": f"Speed = Distance / Time = {length}m / {seconds}s = {speed_ms} m/s. Convert to km/h: {speed_ms} * 3.6 = {ans_kmh} km/h.",
        "correct": f"{ans_kmh} km/h",
        "wrongs": [f"{ans_kmh - 5} km/h", f"{ans_kmh + 10} km/h", f"{ans_kmh + 5} km/h"]
    }

def _gen_work_days():
    men = random.choice([10, 12, 15, 20])
    days = random.choice([12, 16, 20, 24])
    men2 = random.choice([8, 16, 24, 30])
    ans_days = round((men * days) / men2, 1)
    return {
        "text": f"If {men} workers can build a wall in {days} days, how many days will {men2} workers take?",
        "explanation": f"Man-days formula: M1 * D1 = M2 * D2 => {men} * {days} = {men2} * D2 => D2 = {ans_days} days.",
        "correct": f"{ans_days} days",
        "wrongs": [f"{ans_days + 2} days", f"{max(1, ans_days - 3)} days", f"{ans_days + 5} days"]
    }


# Pre-defined AI template banks for dynamic question generation
AI_TOPIC_TEMPLATES = {
    "Logical Reasoning": [
        {
            "template": "If {item_a} are {item_b} and all {item_b} are {item_c}, what is true?",
            "vars": [
                ("Robots", "Machines", "Automated Systems"),
                ("Laptops", "Computers", "Electronic Devices"),
                ("Falcons", "Birds", "Vertebrates"),
                ("Diamonds", "Minerals", "Precious Crystals")
            ],
            "correct_fn": lambda a, b, c: f"All {a} are {c}",
            "wrong_fn": lambda a, b, c: [f"All {c} are {a}", f"No {a} are {c}", f"Some {b} are not {c}"],
            "difficulty": Question.EASY,
            "explanation": "Syllogism rule: A ⊂ B ⊂ C implies A ⊂ C transitively."
        },
        {
            "gen_fn": _gen_number_series,
            "difficulty": Question.MEDIUM
        },
        {
            "gen_fn": _gen_coding_decoding,
            "difficulty": Question.MEDIUM
        }
    ],
    "Quantitative Aptitude": [
        {
            "gen_fn": _gen_train_speed,
            "difficulty": Question.MEDIUM
        },
        {
            "gen_fn": _gen_work_days,
            "difficulty": Question.EASY
        },
        {
            "template": "What is the probability of rolling a prime number (2, 3, 5) on a fair 6-sided die?",
            "difficulty": Question.EASY,
            "choices": [("1/2", True), ("1/3", False), ("2/3", False), ("1/6", False)],
            "explanation": "Prime numbers on a 6-sided die are 2, 3, 5 (3 favorable outcomes out of 6). Probability = 3/6 = 1/2."
        }
    ],
    "Verbal & Analogies": [
        {
            "template": "Select the word that is most opposite in meaning (Antonym) to '{word}':",
            "pairs": [
                ("METICULOUS", "Careless", ["Detailed", "Accurate", "Cautious"]),
                ("BENEVOLENT", "Malevolent", ["Kind", "Generous", "Helpful"]),
                ("CANDID", "Deceptive", ["Frank", "Honest", "Direct"]),
                ("EPHEMERAL", "Permanent", ["Fleeting", "Short", "Transient"])
            ],
            "difficulty": Question.MEDIUM
        }
    ]
}

def generate_ai_questions(subject_id=None, difficulty=None, count=5):
    """
    AI Generator engine to synthesize latest reasoning & aptitude questions.
    """
    created_questions = []

    subjects = Subject.objects.all()
    if not subjects.exists():
        sub_default, _ = Subject.objects.get_or_create(name="Logical Reasoning")
        subjects = [sub_default]

    for _ in range(count):
        if subject_id:
            try:
                subject = Subject.objects.get(pk=subject_id)
            except Exception:
                subject = random.choice(list(subjects))
        else:
            subject = random.choice(list(subjects))

        sub_name = subject.name
        templates = AI_TOPIC_TEMPLATES.get(sub_name, AI_TOPIC_TEMPLATES["Logical Reasoning"])
        tmpl_data = random.choice(templates)

        q_diff = difficulty if difficulty in [Question.EASY, Question.MEDIUM, Question.HARD] else tmpl_data.get("difficulty", Question.MEDIUM)

        q_text = ""
        explanation = ""
        choices_data = []

        if "gen_fn" in tmpl_data:
            data = tmpl_data["gen_fn"]()
            q_text = data["text"]
            explanation = data["explanation"]
            choices_data = [(data["correct"], True)] + [(w, False) for w in data["wrongs"]]

        elif "pairs" in tmpl_data:
            word, correct_word, wrong_words = random.choice(tmpl_data["pairs"])
            q_text = tmpl_data["template"].format(word=word)
            explanation = f"'{word}' is opposite to '{correct_word}'."
            choices_data = [(correct_word, True)] + [(w, False) for w in wrong_words]

        elif "vars" in tmpl_data:
            a, b, c = random.choice(tmpl_data["vars"])
            q_text = tmpl_data["template"].format(item_a=a, item_b=b, item_c=c)
            explanation = tmpl_data["explanation"]
            correct = tmpl_data["correct_fn"](a, b, c)
            wrongs = tmpl_data["wrong_fn"](a, b, c)
            choices_data = [(correct, True)] + [(w, False) for w in wrongs]

        else:
            q_text = tmpl_data.get("template", "What is the next logical pattern?")
            explanation = tmpl_data.get("explanation", "Standard logical sequence rule applies.")
            choices_data = tmpl_data.get("choices", [("Option A", True), ("Option B", False), ("Option C", False), ("Option D", False)])

        # Skip if duplicate question already exists in DB
        if Question.objects.filter(text=q_text).exists():
            continue

        # Save question to DB
        q = Question.objects.create(
            text=q_text,
            subject=subject,
            difficulty=q_diff,
            explanation=explanation
        )

        random.shuffle(choices_data)
        for c_text, is_corr in choices_data:
            Choice.objects.create(question=q, text=c_text, is_correct=is_corr)

        created_questions.append(q)

    return created_questions


def fetch_internet_questions(subject_id=None, difficulty=None, count=5):
    """
    Fetches real-world aptitude and reasoning questions over the internet via Open REST APIs.
    Supports fetching up to 100 questions.
    """
    created_questions = []
    target_count = min(max(1, int(count)), 100)

    diff_api_map = {
        Question.EASY: 'easy',
        Question.MEDIUM: 'medium',
        Question.HARD: 'hard',
    }

    target_subject = None
    if subject_id:
        target_subject = Subject.objects.filter(pk=subject_id).first()

    attempts = 0
    while len(created_questions) < target_count and attempts < 10:
        attempts += 1
        batch_needed = target_count - len(created_questions)
        amount_to_request = min(max(batch_needed * 2, 20), 50)

        url = f"https://opentdb.com/api.php?amount={amount_to_request}&type=multiple"
        if difficulty in diff_api_map:
            url += f"&difficulty={diff_api_map[difficulty]}"

        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) MentalAbilityTestSoftware/1.0'}
        )

        try:
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    results = data.get('results', [])

                    if not results:
                        break

                    added_in_batch = 0
                    for item in results:
                        if len(created_questions) >= target_count:
                            break

                        q_text = html.unescape(item.get('question', '')).strip()
                        corr_ans = html.unescape(item.get('correct_answer', '')).strip()
                        incorr_ans = [html.unescape(x).strip() for x in item.get('incorrect_answers', [])]

                        if not q_text or not corr_ans or len(incorr_ans) < 3:
                            continue

                        # Prevent duplicate questions in database
                        if Question.objects.filter(text=q_text).exists():
                            continue

                        cat_name = html.unescape(item.get('category', 'General Aptitude'))
                        sub = target_subject
                        if not sub:
                            sub, _ = Subject.objects.get_or_create(name=cat_name[:40])

                        diff_val = item.get('difficulty', '').upper()
                        if diff_val not in [Question.EASY, Question.MEDIUM, Question.HARD]:
                            diff_val = Question.MEDIUM

                        exp = f"Category: {cat_name}. Correct Answer: {corr_ans}."

                        q = Question.objects.create(
                            text=q_text,
                            subject=sub,
                            difficulty=diff_val,
                            explanation=exp
                        )

                        choices_data = [(corr_ans, True)] + [(w, False) for w in incorr_ans[:3]]
                        random.shuffle(choices_data)

                        for c_text, is_corr in choices_data:
                            Choice.objects.create(question=q, text=c_text, is_correct=is_corr)

                        created_questions.append(q)
                        added_in_batch += 1

                    if added_in_batch == 0:
                        break

        except Exception as e:
            print(f"Internet Question Fetch Notice: {e}")
            break

    # Fallback to local AI generator if internet fetch returns 0 or offline
    if not created_questions:
        created_questions = generate_ai_questions(subject_id=subject_id, difficulty=difficulty, count=target_count)

    return created_questions
