from django.db import models
from django.contrib.auth.models import User # For linking to Django's built-in User model

class FamilyMember(models.Model):
    """
    Represents a family member, linked to a Django User account.
    This separation allows you to store additional member-specific
    data beyond what's in Django's User model.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='family_member',
        help_text="Links to the Django User account for this family member."
    )
    name = models.CharField(
        max_length=255,
        help_text="The display name of the family member."
    )
    # You might add other fields here, e.g., age, avatar, etc.
    # age = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Family Member"
        verbose_name_plural = "Family Members"
        ordering = ['name'] # Order members by name by default

    def __str__(self):
        return self.name

class Account(models.Model):
    """
    Represents a financial account belonging to a family member.
    Each member can have multiple accounts (e.g., 'Allowance', 'Savings').
    """
    member = models.ForeignKey(
        FamilyMember,
        on_delete=models.CASCADE,
        related_name='accounts',
        help_text="The family member who owns this account."
    )
    account_name = models.CharField(
        max_length=255,
        help_text="A descriptive name for the account (e.g., 'Allowance', 'Savings Account')."
    )
    balance_current = models.DecimalField(
        max_digits=19, # Max 19 digits total
        decimal_places=2, # 2 decimal places for currency
        default=0.00,
        help_text="The current balance of the account."
    )
    currency = models.CharField(
        max_length=3,
        default='USD', # Default currency code (e.g., USD, EUR, ILS)
        help_text="The ISO 4217 currency code for this account (e.g., 'USD', 'EUR')."
    )

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        unique_together = ('member', 'account_name') # A member can't have two accounts with the same name
        ordering = ['member__name', 'account_name']

    def __str__(self):
        return f"{self.member.name}'s {self.account_name} ({self.currency})"

class TransactionCategory(models.Model):
    """
    Defines categories for transactions (e.g., 'Food', 'Entertainment', 'Allowance').
    """
    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    name = models.CharField(
        max_length=255,
        unique=True, # Category names should be unique
        help_text="The name of the transaction category (e.g., 'Food', 'Allowance')."
    )
    type = models.CharField(
        max_length=7, # Max length for 'expense'
        choices=CATEGORY_TYPES,
        help_text="Whether this category is for income or expense."
    )

    class Meta:
        verbose_name = "Transaction Category"
        verbose_name_plural = "Transaction Categories"
        ordering = ['type', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Transaction(models.Model):
    """
    Records an individual financial transaction (income or expense).
    """
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions',
        help_text="The account involved in this transaction."
    )
    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.SET_NULL, # Don't delete transactions if category is removed
        null=True,
        blank=True,
        related_name='transactions',
        help_text="The category of this transaction."
    )
    amount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        help_text="The amount of the transaction. Positive for income, negative for expense (though 'type' is also used)."
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="A brief description of the transaction (e.g., 'Bought a toy', 'Weekly allowance')."
    )
    date = models.DateField(
        help_text="The date the transaction occurred."
    )
    TRANSACTION_TYPES = [
        ('credit', 'Credit (Income)'),
        ('debit', 'Debit (Expense)'),
    ]
    type = models.CharField(
        max_length=6, # Max length for 'credit' or 'debit'
        choices=TRANSACTION_TYPES,
        help_text="Whether this transaction is a credit (adds money) or debit (removes money)."
    )
    # Consider adding a 'created_at' and 'updated_at' for auditing
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-date', '-id'] # Order by newest first

    def __str__(self):
        sign = '+' if self.type == 'credit' else '-'
        return f"{self.date}: {self.account.member.name}'s {self.account.account_name} - {sign}{self.amount} ({self.description or 'No description'})"

    def save(self, *args, **kwargs):
        """
        Override save to automatically update the account balance.
        """
        if self._state.adding: # Only on creation
            if self.type == 'credit':
                self.account.balance_current += self.amount
            elif self.type == 'debit':
                self.account.balance_current -= self.amount
            self.account.save()
        # You might also add logic here for updates to transactions,
        # which would require more complex balance adjustments.
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Override delete to automatically revert the account balance.
        """
        if self.type == 'credit':
            self.account.balance_current -= self.amount
        elif self.type == 'debit':
            self.account.balance_current += self.amount
        self.account.save()
        super().delete(*args, **kwargs)


class Budget(models.Model):
    """
    Allows family members to set monthly budgets for specific categories.
    """
    member = models.ForeignKey(
        FamilyMember,
        on_delete=models.CASCADE,
        related_name='budgets',
        help_text="The family member who set this budget."
    )
    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.CASCADE,
        related_name='budgets',
        help_text="The category for which this budget is set."
    )
    amount_monthly = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        help_text="The maximum amount budgeted for this category per month."
    )
    start_date = models.DateField(
        help_text="The start date from which this budget is active."
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="The end date until which this budget is active (optional, for recurring budgets)."
    )

    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
        unique_together = ('member', 'category', 'start_date') # A member can't have duplicate budgets for the same category on the same start date
        ordering = ['member__name', 'start_date', 'category__name']

    def __str__(self):
        end_date_str = self.end_date.strftime('%Y-%m-%d') if self.end_date else 'Ongoing'
        return (
            f"{self.member.name}'s Budget: {self.category.name} - "
            f"{self.amount_monthly} from {self.start_date.strftime('%Y-%m-%d')} to {end_date_str}"
        )