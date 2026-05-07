from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Post

class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret',
        )
        # Без title
        cls.text = 'Текст вимірювання'
        cls.data = timezone.now()
        cls.temperature = 22.5
        cls.pressure = 1013.0
        cls.speed = 5.2
        cls.probability = 0.75
        cls.post = Post.objects.create(
            text=cls.text,
            data=cls.data,
            temperature=cls.temperature,
            pressure=cls.pressure,
            speed=cls.speed,
            probability=cls.probability,
            author=cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.text, self.text)
        self.assertEqual(self.post.author, self.user)
        # Перевірка get_absolute_url
        self.assertEqual(self.post.get_absolute_url(), f'/post/{self.post.pk}/')

    def test_url_exists(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.text)
        self.assertTemplateUsed(response, 'home.html')

    def test_post_createview(self):
        self.client.login(username='testuser', password='secret')
        new_text = 'Новий текст'
        new_data = timezone.now()
        response = self.client.post(
            reverse('post_new'),
            {
                'text': new_text,
                'data': new_data,
                'temperature': 25.0,
                'pressure': 1015,
                'speed': 6.0,
                'probability': 0.9,
                'author': self.user.id,
            }
        )
        self.assertEqual(response.status_code, 302)
        last_post = Post.objects.last()
        self.assertEqual(last_post.text, new_text)

    def test_post_editview(self):
        self.client.login(username='testuser', password='secret')
        updated_text = 'Оновлений текст'
        response = self.client.post(
            reverse('post_edit', args=[self.post.pk]),
            {
                'text': updated_text,
                'data': self.data,
                'temperature': self.temperature,
                'pressure': self.pressure,
                'speed': self.speed,
                'probability': self.probability,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, updated_text)

    def test_post_deleteview(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.post(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)