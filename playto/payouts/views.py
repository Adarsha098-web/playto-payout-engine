
from django.shortcuts import render
from django.db.models import Sum, Case, When, IntegerField, F
from django.db import transaction

import random
import time


from payouts.models import Ledger, Merchant, Payout, IdempotencyKey


# 💰 Balance calculation
def get_balance(merchant):
    result = Ledger.objects.filter(merchant=merchant).aggregate(
        balance=Sum(
            Case(
                When(type='credit', then=F('amount_paise')),
                When(type='debit', then=-1 * F('amount_paise')),
                output_field=IntegerField()
            )
        )
    )
    return result['balance'] or 0


# 💸 Create payout with idempotency + concurrency safety
def create_payout(merchant_id, amount_paise, idempotency_key):
    with transaction.atomic():

        # 🔁 Idempotency check
        existing = IdempotencyKey.objects.filter(
            merchant_id=merchant_id,
            key=idempotency_key
        ).first()

        if existing:
            return existing.response_data

        # 🔒 Lock merchant row (prevents race condition)
        merchant = Merchant.objects.select_for_update().get(id=merchant_id)

        # 💰 Check balance
        balance = get_balance(merchant)

        if balance < amount_paise:
            return {"error": "Insufficient balance"}

        # 💸 Create payout
        payout = Payout.objects.create(
            merchant=merchant,
            amount_paise=amount_paise,
            status='pending'
        )

        # Response
        response = {
            "payout_id": payout.id,
            "status": payout.status
        }

        # 🔁 Save idempotency key
        IdempotencyKey.objects.create(
            merchant=merchant,
            key=idempotency_key,
            response_data=response
        )

        return response
    
    import random
import time

def process_payout(payout_id):
    payout = Payout.objects.get(id=payout_id)

    # Only process if still pending
    if payout.status != 'pending':
        return payout.status

    # Move to processing
    payout.status = 'processing'
    payout.save()

    time.sleep(2)  # simulate delay

    rand = random.randint(1, 100)

    if rand <= 70:
        payout.status = 'completed'
    elif rand <= 90:
        payout.status = 'failed'
    else:
        payout.status = 'processing'  # stuck case

    payout.save()

    return payout.status