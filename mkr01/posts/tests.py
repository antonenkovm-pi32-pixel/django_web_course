from django.test import TestCase
from .models import Post
from django.urls import reverse

# Create your tests here.
class PostTest(TestCase):
    

    def test_database_as_dict(self):
    # This returns a QuerySet of dictionaries
        data = Post.objects.values() 
        for row in data:
            print(row)

    def test_url_exists_at_correct_location(self):
        response = self.client.get("") # отримання відповіді від серверу
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("home")) # звернення до сторінки за її псевдонімом
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html") # тестуємо наявність шаблону сторінки

    def test_template_content(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "<h2>Дошка атмосферних вимірювань</h2>") # перевіряємо наявність заголовку на сторінці