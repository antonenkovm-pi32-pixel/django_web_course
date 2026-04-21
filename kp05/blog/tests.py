from django.test import TestCase

# Create your tests here.
# blog/tests.py
from django.contrib.auth import get_user_model # модель таблиці клієнтів
from django.test import TestCase
from django.urls import reverse
from .models import Post
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
# створення тестової бази даних
# створення таблиці клієнтів з одним клієнтом
        cls.user = get_user_model().objects.create_user(
        username='testuser',
        email='test@email.com',
        password='secret',
        )
# створення таблиці дописів з одним дописом
        cls.title = "New title"
        cls.body = 'Body content'
        cls.author = cls.user
        cls.post = Post.objects.create(
        title=cls.title,
        body=cls.body,
        author=cls.author
        )
    def test_post_model(self):
# тестування моделі допису
        self.assertEqual(self.post.title, self.title)
        self.assertEqual(self.post.body, self.body)
        self.assertEqual(self.post.author, self.author)
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')
    def test_url_exists_at_correct_location_listview(self):
# перевірка адреси початкової сторінки
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    def test_url_exists_at_correct_location_detailview(self):
# перевірка адреси сторінки першого допису
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
# перевірка початкової сторінки
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.body)
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detailview(self):
# перевірка сторінки допису
        response = self.client.get(reverse("post_detail", kwargs={"pk":

        self.post.pk}))

        no_response = self.client.get("/post/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, self.title)
        self.assertTemplateUsed(response, "post_detail.html")
