from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from finance.models import Account, Transfer
from decimal import Decimal

class TransferCRUDTest(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username="transferuser",
            password="testpassword123",
            email="transferuser@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Create accounts
        self.account_from = Account.objects.create(
            name="Checking",
            balance=Decimal('1000.00'),
            owner=self.user
        )
        self.account_to = Account.objects.create(
            name="Savings",
            balance=Decimal('500.00'),
            owner=self.user
        )

        self.transfer_list_url = "/api/transfers/"

    def test_transfer_crud_flow(self):
        """
        Transfer CRUD (without UPDATE) and balance verification
        """

        # 1️⃣ Create transfer
        create_data = {
            "from_account": self.account_from.id,
            "to_account": self.account_to.id,
            "amount": "300.00",
            "description": "Move money to savings",
            "owner": self.user.id
        }
        response = self.client.post(self.transfer_list_url, create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transfer_id = response.data['id']

        # ⚡ Refresh balances from DB
        self.account_from.refresh_from_db()
        self.account_to.refresh_from_db()

        print(f"Balance FROM after create: {self.account_from.balance}")
        print(f"Balance TO after create: {self.account_to.balance}")

        # Verify balances
        self.assertEqual(self.account_from.balance, Decimal('700.00'))
        self.assertEqual(self.account_to.balance, Decimal('800.00'))

        # 2️⃣ List transfers
        response = self.client.get(self.transfer_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transfers = response.data.get("results", response.data)
        self.assertTrue(any(tr["id"] == transfer_id for tr in transfers))

        # 3️⃣ Transfer detail
        response = self.client.get(f"/api/transfers/{transfer_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], "300.00")

        # 4️⃣ Delete transfer
        response = self.client.delete(f"/api/transfers/{transfer_id}/")
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])

        # ⚡ Refresh balances from DB
        self.account_from.refresh_from_db()
        self.account_to.refresh_from_db()

        print(f"Balance FROM after delete: {self.account_from.balance}")
        print(f"Balance TO after delete: {self.account_to.balance}")

        # Verify that balances were reverted
        self.assertEqual(self.account_from.balance, Decimal('1000.00'))
        self.assertEqual(self.account_to.balance, Decimal('500.00'))
