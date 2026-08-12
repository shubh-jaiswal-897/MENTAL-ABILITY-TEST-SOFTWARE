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

    def test_test_session_shuffles_choices(self):
        # Create a test question with 4 choices where choice 1 is correct
        from quiz.models import Subject
        sub = Subject.objects.create(name='LogicTest')
        q = Question.objects.create(text='Sample Question', subject=sub)
        Choice.objects.create(question=q, text='Option 1 (Correct)', is_correct=True)
        Choice.objects.create(question=q, text='Option 2', is_correct=False)
        Choice.objects.create(question=q, text='Option 3', is_correct=False)
        Choice.objects.create(question=q, text='Option 4', is_correct=False)

        # Login a test user
        from django.contrib.auth.models import User
        user = User.objects.create_user('testuser', 'test@test.com', 'password123')
        self.client.force_login(user)

        from django.utils import timezone
        session = self.client.session
        session['test_qs'] = [q.id]
        session['test_index'] = 0
        session['test_start'] = timezone.now().timestamp()
        session['test_duration'] = 600
        session.save()

        resp = self.client.get(reverse('quiz:test_session'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('shuffled_choices', resp.context)
        shuffled = resp.context['shuffled_choices']
        self.assertEqual(len(shuffled), 4)

    def test_test_session_timeout_calculates_score(self):
        from quiz.models import Subject
        sub = Subject.objects.create(name='TimeoutTest')
        q = Question.objects.create(text='Question 1', subject=sub)
        c_corr = Choice.objects.create(question=q, text='Right', is_correct=True)

        from django.contrib.auth.models import User
        user = User.objects.create_user('timeout_user', 't@test.com', 'pwd')
        self.client.force_login(user)

        from django.utils import timezone
        session = self.client.session
        session['test_qs'] = [q.id]
        session['test_index'] = 0
        # Set start timestamp in past (expired duration)
        session['test_start'] = timezone.now().timestamp() - 700
        session['test_duration'] = 600
        session['test_answers'] = {str(q.id): c_corr.id}
        session.save()

        resp = self.client.post(reverse('quiz:test_session'), {'choice': c_corr.id, 'action': 'next'})
        self.assertEqual(resp.status_code, 302)

        # Verify result page persistence
        result_resp = self.client.get(reverse('quiz:test_result'))
        self.assertEqual(result_resp.status_code, 200)
        self.assertEqual(result_resp.context['score'], 1)

        # Refresh result page and verify score persists
        refresh_resp = self.client.get(reverse('quiz:test_result'))
        self.assertEqual(refresh_resp.status_code, 200)
        self.assertEqual(refresh_resp.context['score'], 1)

    def test_goodie_redemption_address_flow(self):
        from quiz.models import GoodieItem, UserGoodieRedemption, UserProfile
        from django.contrib.auth.models import User

        user = User.objects.create_user('goodie_buyer', 'buyer@test.com', 'pwd123')
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.total_xp = 500
        profile.save()

        goodie = GoodieItem.objects.create(name='Test T-Shirt', description='Cool Shirt', coin_cost=100, stock=5)
        self.client.force_login(user)

        # GET address checkout page
        resp_get = self.client.get(reverse('quiz:redeem_address', args=[goodie.id]))
        self.assertEqual(resp_get.status_code, 200)
        self.assertContains(resp_get, 'Test T-Shirt')

        # POST shipping address details
        post_data = {
            'full_name': 'Rahul Sharma',
            'phone_number': '9876543210',
            'shipping_address': 'Flat 101, Star Heights, Main Road',
            'city': 'New Delhi',
            'state': 'Delhi',
            'pincode': '110001',
        }
        resp_post = self.client.post(reverse('quiz:redeem_address', args=[goodie.id]), post_data)
        self.assertEqual(resp_post.status_code, 302)

        # Verify DB updates: XP deducted, stock reduced, UserGoodieRedemption created with shipping address
        profile.refresh_from_db()
        goodie.refresh_from_db()
        self.assertEqual(profile.total_xp, 400)
        self.assertEqual(goodie.stock, 4)

        order = UserGoodieRedemption.objects.get(user=user, goodie=goodie)
        self.assertEqual(order.full_name, 'Rahul Sharma')
        self.assertEqual(order.city, 'New Delhi')
        self.assertEqual(order.status, 'Pending Processing')

    def test_admin_cancel_order_refunds_xp(self):
        from quiz.models import GoodieItem, UserGoodieRedemption, UserProfile
        from django.contrib.auth.models import User

        user = User.objects.create_user('refund_user', 'refund@test.com', 'pwd123')
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.total_xp = 300
        profile.save()

        goodie = GoodieItem.objects.create(name='Reward Mug', description='Ceramic Mug', coin_cost=150, stock=10)

        # Create order (subtracting XP to 150, stock to 9)
        profile.total_xp -= goodie.coin_cost
        profile.save()
        goodie.stock -= 1
        goodie.save()

        order = UserGoodieRedemption.objects.create(
            user=user,
            goodie=goodie,
            full_name='Test User',
            phone_number='1234567890',
            shipping_address='123 Street',
            city='Delhi',
            pincode='110001',
            status='Pending Processing'
        )

        self.assertEqual(profile.total_xp, 150)
        self.assertEqual(goodie.stock, 9)

        # Admin cancels order
        order.status = 'Cancelled ❌'
        order.save()

        # Verify XP is refunded (+150) back to 300, and stock is restored (+1) back to 10
        profile.refresh_from_db()
        goodie.refresh_from_db()
        self.assertEqual(profile.total_xp, 300)
        self.assertEqual(goodie.stock, 10)

    def test_fetch_internet_questions(self):
        from quiz.ai_generator import fetch_internet_questions
        from quiz.models import Question

        initial_count = Question.objects.count()
        created = fetch_internet_questions(count=3)
        self.assertTrue(len(created) >= 1)
        self.assertTrue(Question.objects.count() > initial_count)
        first_q = created[0]
        self.assertEqual(first_q.choices.count(), 4)
        self.assertTrue(first_q.choices.filter(is_correct=True).exists())


