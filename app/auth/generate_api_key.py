
import secrets
import string
import argparse

def generate_api_key(prefix="sk_tlr_crm"):
    
    random_part = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    api_key = f"{prefix}_{random_part}"
    return api_key

def main():
    parser = argparse.ArgumentParser(description='Generate secure API keys for the TLR Email API')
    parser.add_argument('--prefix', default='sk_tlr_crm', help='API key prefix')
    parser.add_argument('--count', type=int, default=1, help='Number of keys to generate')
    
    args = parser.parse_args()
    
    print(f"Generated {args.count} API key(s):")
    for i in range(args.count):
        api_key = generate_api_key(args.prefix)
        print(f"{api_key}")

if __name__ == "__main__":
    main()