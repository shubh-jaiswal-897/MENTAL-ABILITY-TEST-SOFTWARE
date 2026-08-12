import random
import urllib.request
import json
import html
from quiz.models import Subject, Question, Choice

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
            "template": "Complete the logical number sequence: {start}, {v1}, {v2}, {v3}, ?",
            "vars_fn": lambda: (
                diff := random.choice([3, 5, 7, 9]),
                start := random.randint(10, 50),
                v1 := start + diff,
                v2 := v1 + diff + 2,
                v3 := v2 + diff + 4,
                ans := v3 + diff + 6,
                (start, v1, v2, v3, ans, f"The pattern increases difference by +2 each step: +{diff}, +{diff+2}, +{diff+4}, +{diff+6}.")
            ),
            "difficulty": Question.MEDIUM
        },
        {
            "template": "Coding & Decoding: If '{word}' is coded as '{code}', how is '{word2}' coded?",
            "vars_fn": lambda: (
                word := random.choice(["BRAIN", "LOGIC", "SMART", "FLASH"]),
                shift := random.choice([1, 2, 3]),
                code := "".join([chr((ord(c) - 65 + shift) % 26 + 65) for c in word]),
                word2 := random.choice(["MIND", "DATA", "CODE", "NODE"]),
                ans := "".join([chr((ord(c) - 65 + shift) % 26 + 65) for c in word2]),
                f"Each letter is shifted forward by +{shift} in the alphabet."
            ),
            "difficulty": Question.MEDIUM
        }
    ],
    "Quantitative Aptitude": [
        {
            "template": "A train {length} meters long passes a signal post in {seconds} seconds. What is the speed of the train in km/h?",
            "vars_fn": lambda: (
                length := random.choice([120, 150, 180, 240]),
                seconds := random.choice([10, 12, 15, 20]),
                speed_ms := length / seconds,
                ans_kmh := int(speed_ms * 3.6),
                (length, seconds, f"{ans_kmh} km/h", [f"{ans_kmh - 5} km/h", f"{ans_kmh + 10} km/h", f"{ans_kmh + 5} km/h"],
                 f"Speed = Distance / Time = {length}m / {seconds}s = {speed_ms} m/s. Convert to km/h: {speed_ms} * 3.6 = {ans_kmh} km/h.")
            ),
            "difficulty": Question.MEDIUM
        },
        {
            "template": "If {men} workers can build a wall in {days} days, how many days will {men2} workers take?",
            "vars_fn": lambda: (
                men := random.choice([10, 12, 15, 20]),
                days := random.choice([12, 16, 20, 24]),
                men2 := random.choice([8, 16, 24, 30]),
                ans_days := round((men * days) / men2, 1),
                (men, days, men2, f"{ans_days} days", [f"{ans_days + 2} days", f"{max(1, ans_days - 3)} days", f"{ans_days + 5} days"],
                 f"Man-days formula: M1 * D1 = M2 * D2 => {men} * {days} = {men2} * D2 => D2 = {ans_days} days.")
            ),
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

        if "vars_fn" in tmpl_data:
            res = tmpl_data["vars_fn"]()
            if len(res) == 7: # number series template
                start, v1, v2, v3, ans, exp = res
                q_text = tmpl_data["template"].format(start=start, v1=v1, v2=v2, v3=v3)
                explanation = exp
                choices_data = [(str(ans), True), (str(ans + 2), False), (str(ans - 4), False), (str(ans + 5), False)]
            elif len(res) == 6: # coding or ratio template
                word, shift, code, word2, ans, exp = res
                q_text = tmpl_data["template"].format(word=word, code=code, word2=word2)
                explanation = exp
                choices_data = [(ans, True), ("WRONG1", False), ("WRONG2", False), ("WRONG3", False)]
            elif len(res) == 6 or len(res) == 5: # train / work template
                length, seconds, ans_str, wrong_strs, exp = res[0], res[1], res[2], res[3], res[4]
                q_text = tmpl_data["template"].format(length=length, seconds=seconds) if "length" in tmpl_data["template"] else tmpl_data["template"].format(men=res[0], days=res[1], men2=res[2])
                explanation = exp
                choices_data = [(ans_str, True)] + [(w, False) for w in wrong_strs[:3]]

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

        # Save question to DB
        q = Question.objects.create(
            text=f"[AI] {q_text}",
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
    """
    created_questions = []

    diff_api_map = {
        Question.EASY: 'easy',
        Question.MEDIUM: 'medium',
        Question.HARD: 'hard',
    }

    url = f"https://opentdb.com/api.php?amount={min(count, 20)}&type=multiple"
    if difficulty in diff_api_map:
        url += f"&difficulty={diff_api_map[difficulty]}"

    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) MentalAbilityTestSoftware/1.0'}
    )

    try:
        with urllib.request.urlopen(req, timeout=7) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                results = data.get('results', [])

                target_subject = None
                if subject_id:
                    target_subject = Subject.objects.filter(pk=subject_id).first()

                for item in results:
                    q_text = html.unescape(item.get('question', '')).strip()
                    corr_ans = html.unescape(item.get('correct_answer', '')).strip()
                    incorr_ans = [html.unescape(x).strip() for x in item.get('incorrect_answers', [])]

                    if not q_text or not corr_ans or len(incorr_ans) < 3:
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
                        text=f"[Web] {q_text}",
                        subject=sub,
                        difficulty=diff_val,
                        explanation=exp
                    )

                    choices_data = [(corr_ans, True)] + [(w, False) for w in incorr_ans[:3]]
                    random.shuffle(choices_data)

                    for c_text, is_corr in choices_data:
                        Choice.objects.create(question=q, text=c_text, is_correct=is_corr)

                    created_questions.append(q)

    except Exception as e:
        print(f"Internet Question Fetch Notice: {e}")

    # Fallback to local AI generator if internet fetch returns 0 or offline
    if not created_questions:
        created_questions = generate_ai_questions(subject_id=subject_id, difficulty=difficulty, count=count)

    return created_questions
