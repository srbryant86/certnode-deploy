import requests
import json

# Replace with your local/dev webhook endpoint
WEBHOOK_URL = "http://localhost:8000/webhook"

# Simulated Stripe event payload
event_payload = {
  "id": "evt_test_webhook",
  "object": "event",
  "type": "invoice.payment_succeeded",
  "data": {
    "object": {
      "customer": "cus_TEST123",
      "lines": {
        "data": [{
          "price": {
            "id": "price_enterprise_123"
          }
        }]
      }
    }
  }
}

headers = {
    "Content-Type": "application/json",
    "stripe-signature": "t0kentest"  # Replace with valid sig for real
}

response = requests.post(WEBHOOK_URL, data=json.dumps(event_payload), headers=headers)
print("Status Code:", response.status_code)
print("Response:", response.text)
