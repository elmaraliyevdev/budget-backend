from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Transaction


@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, created, **kwargs):
    print("instance", instance.transaction_type)
    if created:
        wallet = instance.wallet
        print('wallet', wallet.balance)
        print('type', instance.transaction_type)
        if instance.transaction_type == 'income':
            print('income', instance.amount)
            wallet.balance += instance.amount

            print('income', wallet.balance)
        elif instance.transaction_type == 'expense':
            print('expense', instance.amount)
            wallet.balance -= instance.amount
            print('expense', wallet.balance)

        instance.balance_after = wallet.balance

        instance.save()

        wallet.save()


post_save.connect(update_wallet_balance, sender=Transaction)
