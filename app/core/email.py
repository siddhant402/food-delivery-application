def send_email(to_email: str, subject: str, body: str):
    print("\n--- EMAIL SENT ---")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print(body)
    print("------------------\n")

# This is intentionally a stub.
# Replace with SMTP / SendGrid / SES later.
