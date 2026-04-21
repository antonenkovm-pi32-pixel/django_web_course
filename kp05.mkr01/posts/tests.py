from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Post

class PostTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Створення тестового користувача
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret',
        )
        # Дані для поста
        cls.title = "Test Post Title"
        cls.text = "Це текст поста (опис вимірювання)"
        cls.data = timezone.now()   # обов'язкове поле
        cls.temperature = 22.5
        cls.pressure = 1013.0
        cls.speed = 5.2
        cls.probability = 0.75
        
        # Створення поста
        cls.post = Post.objects.create(
            title=cls.title,
            text=cls.text,
            data=cls.data,
            temperature=cls.temperature,
            pressure=cls.pressure,
            speed=cls.speed,
            probability=cls.probability,
            author=cls.user,
        )

    # --- Тести моделі ---
    def test_post_model_fields(self):
        """Перевірка, що всі поля моделі зберігаються коректно"""
        self.assertEqual(self.post.title, self.title)
        self.assertEqual(self.post.text, self.text)
        self.assertEqual(self.post.data, self.data)
        self.assertEqual(self.post.temperature, self.temperature)
        self.assertEqual(self.post.pressure, self.pressure)
        self.assertEqual(self.post.speed, self.speed)
        self.assertEqual(self.post.probability, self.probability)
        self.assertEqual(self.post.author, self.user)

    def test_post_str_method(self):
        """Перевірка методу __str__ (повертає text)"""
        self.assertEqual(str(self.post), self.text)

    def test_absolute_url(self):
        """Перевірка методу get_absolute_url"""
        expected_url = reverse('post_detail', kwargs={'pk': self.post.pk})
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    # --- Тести головної сторінки (список постів) ---
    def test_home_url_exists(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_url_available_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_template_used(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

    def test_home_contains_post_title(self):
        """Перевірка, що заголовок поста з'являється на головній сторінці"""
        response = self.client.get(reverse("home"))
        self.assertContains(response, self.title)

    def test_home_contains_post_text(self):
        """Перевірка, що текст поста (або його частина) з'являється на головній сторінці"""
        response = self.client.get(reverse("home"))
        self.assertContains(response, self.text)

    # --- Тести сторінки детального перегляду поста ---
    def test_detail_url_exists(self):
        response = self.client.get(f"/post/{self.post.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_detail_url_for_nonexistent_post(self):
        response = self.client.get("/post/99999/")
        self.assertEqual(response.status_code, 404)

    def test_detail_url_by_name(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_detail_template_used(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        self.assertTemplateUsed(response, "post_detail.html")

    def test_detail_contains_title(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        self.assertContains(response, self.title)

    def test_detail_contains_text(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        self.assertContains(response, self.text)

    def test_detail_contains_temperature(self):
        """Перевірка, що на сторінці детального перегляду є значення температури"""
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        self.assertContains(response, str(self.temperature))

    # --- Додатковий тест для виведення даних у вигляді словника (опціонально) ---
    def test_database_as_dict(self):
        data = Post.objects.values()
        self.assertEqual(data.count(), 1)
        row = data[0]
        self.assertEqual(row['title'], self.title)
        self.assertEqual(row['text'], self.text)
        self.assertEqual(row['author_id'], self.user.id)