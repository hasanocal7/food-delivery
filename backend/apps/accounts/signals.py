# Django-specific imports
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import loader


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def activate_user(sender, instance, created, **kwargs):
    """
    Function triggered after saving a user instance. Checks if it's a new
    user creation and activates the account, sending a welcome email.
    """
    print(instance.first_name, "is Created: ", created)
    if created:
        # Render the account activation email template
        html_message = loader.render_to_string(
            "account_activation_message.html",
            {
                "first_name": instance.first_name,
                "subject": "Congratulations!",
            },
        )

        # Send the welcome email to the newly created user
        instance.email_user(
            subject="Welcome to Food Delivery", html_message=html_message
        )

        # Activate the user account
        instance.is_active = True
        instance.save()
