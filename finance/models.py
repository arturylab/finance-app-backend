from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    """Represents a financial account owned by a user."""
    
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (${self.balance})"

    class Meta:
        ordering = ['name']


class Category(models.Model):
    """Represents a transaction category with type (income/expense)."""
    
    CATEGORY_TYPE = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=7, choices=CATEGORY_TYPE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.type})"

    class Meta:
        ordering = ['name']
        verbose_name_plural = "categories"

    @classmethod
    def create_default_categories(cls, user):
        """
        Creates default categories for a specific user.
        """
        default_categories = [
            # Income
            ("Salary", "INCOME"),
            ("Investments", "INCOME"),
            ("Gifts", "INCOME"),
            ("Deposits", "INCOME"),

            # Expense
            ("Food", "EXPENSE"),
            ("Housing", "EXPENSE"),
            ("Utilities", "EXPENSE"),
            ("Transportation", "EXPENSE"),
            ("Health", "EXPENSE"),
            ("Entertainment", "EXPENSE"),
            ("Education", "EXPENSE"),
            ("Debt Payments", "EXPENSE"),

            # Special
            ("Initial Balance (+)", "INCOME"),
            ("Initial Balance (-)", "EXPENSE"),
            ("Balance Adjustment (+)", "INCOME"),
            ("Balance Adjustment (-)", "EXPENSE"),
        ]

        for name, cat_type in default_categories:
            cls.objects.get_or_create(
                name=name,
                type=cat_type,
                owner=user
            )



class Transaction(models.Model):
    """Represents a financial transaction linked to an account and category."""
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}: {self.amount} ({self.category})"

    class Meta:
        ordering = ['-date']


class Transfer(models.Model):
    """Represents a money transfer between two accounts."""
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)
    
    from_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transfers_from'
    )
    to_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transfers_to'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transfers'
    )

    def __str__(self):
        return f"{self.from_account} -> {self.to_account}: {self.amount}"

    class Meta:
        ordering = ['-date']