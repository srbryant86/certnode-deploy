import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def get_user_tier(api_key):
    return r.get(f"tier:{api_key}").decode("utf-8")

def set_user_tier(api_key, tier):
    r.set(f"tier:{api_key}", tier)

def increment_usage(api_key):
    return r.incr(f"usage:{api_key}")

def get_usage(api_key):
    val = r.get(f"usage:{api_key}")
    return int(val) if val else 0

def reset_usage(api_key):
    r.set(f"usage:{api_key}", 0)
