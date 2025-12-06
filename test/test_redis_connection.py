from app.config import settings
from app.redis.client import get_redis_client

def test_redis_connection():
    try:
        client = get_redis_client()

        # Test SET
        client.set("test_key", "hello_redis")

        # Test GET
        value = client.get("test_key")

        print("SET/GET Test Passed")
        print("Value returned:", value)

        # Optional: Delete the key
        client.delete("test_key")

        print("Redis connection successful!")

    except Exception as e:
        print("Redis connection failed!")
        print("Error:", str(e))


if __name__ == "__main__":
    #print(settings.redis_url)
    test_redis_connection()
