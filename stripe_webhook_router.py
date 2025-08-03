import stripe
import os
from fastapi import Request, HTTPException

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")

# User tier registry — in production, this should be a secure DB
USER_TIERS = {
    "user_free_key": "free"
}

def get_api_key_by_customer(customer_id):
    # Lookup logic to match Stripe customer ID to API key
    return "user_pro_key"  # Stub: replace with DB lookup

async def handle_webhook_event(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature', '')
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_...")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "invoice.payment_succeeded":
        customer_id = event["data"]["object"]["customer"]
        price_id = event["data"]["object"]["lines"]["data"][0]["price"]["id"]

        # Match customer to internal API key
        api_key = get_api_key_by_customer(customer_id)

        # Upgrade tier based on price ID (mock logic)
        if "pro" in price_id:
            USER_TIERS[api_key] = "pro"
        elif "enterprise" in price_id:
            USER_TIERS[api_key] = "enterprise"

    return {"status": "ok"}
