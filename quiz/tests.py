from django.test import TestCase
from quiz.models import Question, Choice
from django.urls import reverse


class QuizModelTests(TestCase):
    def test_create_question_and_choice(self):
        q = Question.objects.create(text='What is 2+2?')
        Choice.objects.create(question=q, text='3', is_correct=False)
        Choice.objects.create(question=q, text='4', is_correct=True)
        self.assertEqual(q.choices.count(), 2)


class QuizViewTests(TestCase):
    def setUp(self):
        self.q = Question.objects.create(text='What is 2+2?')
        self.c1 = Choice.objects.create(question=self.q, text='3', is_correct=False)
        self.c2 = Choice.objects.create(question=self.q, text='4', is_correct=True)

    def test_index_shows_question(self):
        resp = self.client.get(reverse('quiz:index'))
        self.assertContains(resp, self.q.text)

    def test_take_quiz_get(self):
        resp = self.client.get(reverse('quiz:take_quiz', args=[self.q.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.c1.text)

    def test_submit_correct_answer_redirects_to_result(self):
        resp = self.client.post(reverse('quiz:take_quiz', args=[self.q.pk]), {'choice': self.c2.pk})
        self.assertEqual(resp.status_code, 302)

    def test_result_page_shows_correct(self):
        resp = self.client.get(reverse('quiz:result', args=[self.q.pk, 1]))
        self.assertContains(resp, 'Correct')
