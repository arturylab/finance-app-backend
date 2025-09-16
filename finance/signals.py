# finance/signals.py
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.db.models import F
from django.contrib.auth.models import User
from .models import Transaction, Account, Category, Transfer
from decimal import Decimal

def _effect_amount(amount: Decimal, category: Category):
    """
    Determines the effect (positive/negative) on the account based on category type.
    
    Args:
        amount (Decimal): Transaction amount
        category (Category): Transaction category
        
    Returns:
        Decimal: Positive amount for INCOME, negative for EXPENSE, zero if category is None
    """
    if category is None:
        return Decimal('0.00')
    if category.type == 'INCOME':
        return +amount
    else:  # 'EXPENSE'
        return -amount

@receiver(pre_save, sender=Transaction)
def transaction_pre_save(sender, instance, **kwargs):
    """
    Stores the previous state of a transaction before saving to calculate balance differences.
    
    Saves:
        - Previous account ID
        - Previous effect on balance
    """
    if instance.pk:
        try:
            old = Transaction.objects.get(pk=instance.pk)
            instance._old_account_id = old.account_id
            instance._old_effect = _effect_amount(old.amount, old.category)
        except Transaction.DoesNotExist:
            instance._old_account_id = None
            instance._old_effect = Decimal('0.00')
    else:
        instance._old_account_id = None
        instance._old_effect = Decimal('0.00')

@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created, **kwargs):
    """
    Updates account balances after a transaction is saved.
    
    Behavior:
        - For new transactions: Apply effect to account
        - For updates: Reverse old effect (on old account) and apply new effect (possibly on different account)
    """
    new_effect = _effect_amount(instance.amount, instance.category)

    # For new transactions
    if created:
        if instance.account:
            acct = instance.account
            acct.balance = acct.balance + new_effect
            acct.save(update_fields=['balance'])
        return

    # For updates
    old_effect = getattr(instance, '_old_effect', Decimal('0.00'))
    old_account_id = getattr(instance, '_old_account_id', None)
    
    # Handle account changes
    if old_account_id and old_account_id != instance.account_id:
        try:
            old_acct = Account.objects.get(pk=old_account_id)
            old_acct.balance = old_acct.balance - old_effect
            old_acct.save(update_fields=['balance'])
        except Account.DoesNotExist:
            pass

    # Apply balance difference to current account
    delta = new_effect - old_effect
    if instance.account and delta != Decimal('0.00'):
        acct = instance.account
        acct.balance = acct.balance + delta
        acct.save(update_fields=['balance'])

@receiver(post_delete, sender=Transaction)
def transaction_post_delete(sender, instance, **kwargs):
    """
    Reverses the transaction's effect on account balance when deleted.
    """
    effect = _effect_amount(instance.amount, instance.category)
    if instance.account:
        acct = instance.account
        acct.balance = acct.balance - effect
        acct.save(update_fields=['balance'])

@receiver(pre_save, sender=Transfer)
def transfer_pre_save(sender, instance, **kwargs):
    """
    Stores the previous state of a transfer before saving to calculate balance differences.
    
    Saves:
        - Previous from_account ID
        - Previous to_account ID
        - Previous transfer amount
    """
    if instance.pk:
        try:
            old = Transfer.objects.get(pk=instance.pk)
            instance._old_from_account_id = old.from_account_id
            instance._old_to_account_id = old.to_account_id
            instance._old_amount = old.amount or Decimal('0.00')
        except Transfer.DoesNotExist:
            instance._old_from_account_id = None
            instance._old_to_account_id = None
            instance._old_amount = Decimal('0.00')
    else:
        instance._old_from_account_id = None
        instance._old_to_account_id = None
        instance._old_amount = Decimal('0.00')

@receiver(post_save, sender=Transfer)
def transfer_post_save(sender, instance, created, **kwargs):
    """
    Updates account balances after a transfer is saved.
    
    Behavior:
        - For new transfers: Apply transfer effects to both accounts
        - For updates: Reverse old effects and apply new effects (accounts may have changed)
    """
    current_amount = instance.amount or Decimal('0.00')

    # For new transfers
    if created:
        with transaction.atomic():
            if instance.from_account_id:
                Account.objects.filter(pk=instance.from_account_id).update(
                    balance=F('balance') - current_amount
                )
            if instance.to_account_id:
                Account.objects.filter(pk=instance.to_account_id).update(
                    balance=F('balance') + current_amount
                )
        return

    # For updates - get previous state
    old_from_account_id = getattr(instance, '_old_from_account_id', None)
    old_to_account_id = getattr(instance, '_old_to_account_id', None)
    old_amount = getattr(instance, '_old_amount', Decimal('0.00'))

    with transaction.atomic():
        # Reverse old transfer effects
        if old_from_account_id:
            Account.objects.filter(pk=old_from_account_id).update(
                balance=F('balance') + old_amount  # Restore what was subtracted
            )
        if old_to_account_id:
            Account.objects.filter(pk=old_to_account_id).update(
                balance=F('balance') - old_amount  # Remove what was added
            )

        # Apply new transfer effects
        if instance.from_account_id:
            Account.objects.filter(pk=instance.from_account_id).update(
                balance=F('balance') - current_amount
            )
        if instance.to_account_id:
            Account.objects.filter(pk=instance.to_account_id).update(
                balance=F('balance') + current_amount
            )

@receiver(post_delete, sender=Transfer)
def transfer_post_delete(sender, instance, **kwargs):
    """
    Reverses transfer effects when deleted.
    
    Actions:
        - Increases source account balance
        - Decreases destination account balance
        
    Note:
        Uses F() expressions in atomic transaction for thread-safety
    """
    amount = instance.amount or Decimal('0.00')
    from_id = instance.from_account_id
    to_id = instance.to_account_id

    with transaction.atomic():
        if from_id:
            Account.objects.filter(pk=from_id).update(balance=F('balance') + amount)
        if to_id:
            Account.objects.filter(pk=to_id).update(balance=F('balance') - amount)

@receiver(post_save, sender=User)
def create_user_categories(sender, instance, created, **kwargs):
    """
    Creates default category set for newly registered users.
    
    Triggered:
        Only on user creation, not on updates
    """
    if created:
        Category.create_default_categories(instance)