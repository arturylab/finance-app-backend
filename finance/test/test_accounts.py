# finance/tests/test_accounts.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from finance.models import Account

class AccountCRUDTest(APITestCase):
    def setUp(self):
        # Create user to assign to accounts
        self.user = User.objects.create_user(
            username="accountuser",
            password="testpassword123",
            email="accountuser@example.com"
        )
        # Simulate authentication
        self.client.force_authenticate(user=self.user)
        self.account_list_url = "/api/accounts/"

    def test_account_crud_flow(self):
        """
        Complete CRUD test for accounts:
        Create -> List -> Detail -> Update -> Delete
        """
        # 1️⃣ Create account
        create_data = {
            "name": "Checking",
            "balance": "1000.00",
            "owner": self.user.id
        }
        response = self.client.post(self.account_list_url, create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        account_id = response.data['id']

        # 2️⃣ List accounts
        response = self.client.get(self.account_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Handle pagination if exists
        accounts = response.data.get("results", response.data)
        self.assertTrue(any(acc["id"] == account_id for acc in accounts))

        # 3️⃣ Account detail
        response = self.client.get(f"/api/accounts/{account_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Checking")
        self.assertEqual(str(response.data["balance"]), "1000.00")

        # 4️⃣ Update account
        update_data = {"name": "Updated Checking", "balance": "1200.00"}
        response = self.client.patch(f"/api/accounts/{account_id}/", update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_account = Account.objects.get(id=account_id)
        self.assertEqual(updated_account.name, "Updated Checking")
        self.assertEqual(str(updated_account.balance), "1200.00")

        # 5️⃣ Delete account
        response = self.client.delete(f"/api/accounts/{account_id}/")
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])
        self.assertFalse(Account.objects.filter(id=account_id).exists())
