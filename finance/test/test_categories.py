from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from finance.models import Category

class CategoryCRUDTest(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username="categoryuser",
            password="testpassword123",
            email="categoryuser@example.com"
        )
        self.client.force_authenticate(user=self.user)
        self.category_list_url = "/api/categories/"

    def test_category_crud_flow(self):
        """
        Full CRUD test for categories using a custom category
        (not included in the default_categories):
        Create -> List -> Retrieve -> Update -> Delete
        """
        # 1️⃣ Create category
        create_data = {
            "name": "Freelance",
            "type": "INCOME",
            "owner": self.user.id
        }
        response = self.client.post(self.category_list_url, create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = response.data['id']

        # 2️⃣ Listar categorías
        response = self.client.get(self.category_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categories = response.data.get("results", response.data)
        self.assertTrue(any(cat["id"] == category_id for cat in categories))

        # 3️⃣ Detalle de categoría
        response = self.client.get(f"/api/categories/{category_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Freelance")
        self.assertEqual(response.data["type"], "INCOME")

        # 4️⃣ Actualizar categoría
        update_data = {"name": "Freelance Projects", "type": "INCOME"}
        response = self.client.patch(f"/api/categories/{category_id}/", update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_category = Category.objects.get(id=category_id)
        self.assertEqual(updated_category.name, "Freelance Projects")

        # 5️⃣ Eliminar categoría
        response = self.client.delete(f"/api/categories/{category_id}/")
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])
        self.assertFalse(Category.objects.filter(id=category_id).exists())
