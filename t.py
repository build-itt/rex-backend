import smtplib

try:
    server = smtplib.SMTP('127.0.0.1', 1025)
    server.starttls()
    server.login('darkpass45@proton.me', 'acLN8l9oZNlLdCTFZrJthQ')
    print("Connection successful")
except Exception as e:
    print(f"Failed to connect: {e}")
