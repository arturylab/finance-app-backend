from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from finance.models import Account, Category, Transaction
from decimal import Decimal

class TransactionCRUDTest(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username="transuser",
            password="testpassword123",
            email="transuser@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Create account
        self.account = Account.objects.create(
            name="Checking",
            balance=Decimal('1000.00'),
            owner=self.user
        )

        # Test categories
        self.income_category = Category.objects.create(
            name="Freelance",
            type="INCOME",
            owner=self.user
        )
        self.expense_category = Category.objects.create(
            name="Food",
            type="EXPENSE",
            owner=self.user
        )

        self.transaction_list_url = "/api/transactions/"

    def test_transaction_crud_flow_and_balance(self):
        """
        Transactions CRUD + account balance verification
        """

        # 1️⃣ Create INCOME transaction
        create_data = {
            "account": self.account.id,
            "category": self.income_category.id,
            "amount": "500.00",
            "description": "Freelance project",
            "owner": self.user.id
        }
        response = self.client.post(self.transaction_list_url, create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transaction_id = response.data['id']

        # Verify balance (1000 + 500)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1500.00'))

        # 2️⃣ Create EXPENSE transaction
        create_data_exp = {
            "account": self.account.id,
            "category": self.expense_category.id,
            "amount": "200.00",
            "description": "Groceries",
            "owner": self.user.id
        }
        response = self.client.post(self.transaction_list_url, create_data_exp, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transaction_id_exp = response.data['id']

        # Verify balance (1500 - 200)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1300.00'))

        # 3️⃣ Update transaction (increase expense from 200 to 300)
        update_data = {"amount": "300.00"}
        response = self.client.patch(f"/api/transactions/{transaction_id_exp}/", update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify balance (1500 - 300)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1200.00'))

        # 4️⃣ Delete INCOME transaction
        response = self.client.delete(f"/api/transactions/{transaction_id}/")
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])

        # Balance should decrease by 500
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('700.00'))

        # 5️⃣ Delete EXPENSE transaction
        response = self.client.delete(f"/api/transactions/{transaction_id_exp}/")
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])

        # Final balance should return to the initial 1000
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1000.00'))
