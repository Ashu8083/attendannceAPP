import secrets

def generate_otp_for_user(length=6):
    digits = "0123456789"
    return "".join(secrets.choice(digits) for _ in range(length))

# Example
