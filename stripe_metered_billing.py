import stripe
import os
from datetime import datetime

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")

def create_metered_subscription(customer_email, price_id):
    # Create customer
    customer = stripe.Customer.create(email=customer_email)

    # Create subscription with metered usage
    subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[{
            "price": price_id,
            "billing_thresholds": {"usage_gte": 1}
        }],
        expand=["latest_invoice.payment_intent"]
    )
    return subscription

def report_usage(subscription_item_id, quantity=1):
    usage_record = stripe.UsageRecord.create(
        subscription_item=subscription_item_id,
        quantity=quantity,
        timestamp=int(datetime.utcnow().timestamp()),
        action="increment"
    )
    return usage_record
