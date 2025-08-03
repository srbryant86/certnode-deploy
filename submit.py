def handler(request):
    body = request.get("body", {})
    content = body.get("content", "")

    if not content:
        return {
            "statusCode": 400,
            "body": "Missing content"
        }

    return {
        "statusCode": 200,
        "body": {
            "tier": "T7",
            "valence": "Low",
            "recursion": False,
            "confidence": 91
        }
    }
