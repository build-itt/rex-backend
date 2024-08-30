from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def handle_password_reset_token(sender, instance, reset_password_token, *args, **kwargs):
     # Encode user ID
    token = reset_password_token.key  # Generate token

    # Construct the reset link/reset
    reset_link = f"http://localhost/password/reset/?token={token}"
    user = reset_password_token.user
    # Send the reset link to the user's email
    subject = "Password Reset Link"
    message = f"Click the link below to reset your password:\n\n{reset_link}"
    from_email = "support@darkpass.net"  # Set your sender email address
    recipient_list = [user.email]
    try:
        send_mail(subject, message, from_email, recipient_list)
        print(f"Password reset email sent to {user.email}")
    except Exception as e:
        print(e)
        pass
