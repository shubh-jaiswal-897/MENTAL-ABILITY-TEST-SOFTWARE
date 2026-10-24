"""
Helper utilities and builders for generating 100 high-quality, authentic questions
per subject categorized strictly into EASY (34), MEDIUM (33), and HARD (33).
"""

def make_q(text, correct_answer, wrong_answers, difficulty, explanation):
    """
    Constructs a verified question dictionary with 4 choices.
    Ensures question and choice text lengths conform to models.py (<= 255 chars).
    """
    assert len(wrong_answers) == 3, f"Question must have exactly 3 wrong answers: {text}"
    assert len(text) <= 255, f"Question text exceeds 255 chars ({len(text)}): {text}"
    assert len(correct_answer) <= 255, f"Correct choice exceeds 255 chars: {correct_answer}"
    for wa in wrong_answers:
        assert len(wa) <= 255, f"Wrong choice exceeds 255 chars: {wa}"
    
    return {
        "text": text.strip(),
        "difficulty": difficulty,
        "explanation": explanation.strip(),
        "choices": [
            (correct_answer.strip(), True),
            (wrong_answers[0].strip(), False),
            (wrong_answers[1].strip(), False),
            (wrong_answers[2].strip(), False),
        ]
    }
