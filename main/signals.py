from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from assignment import settings
from .models import Post

@receiver(post_save, sender=Post)
def send_post_creation_email(sender, instance, created, **kwargs):
    if created:
        subject = 'New post has been created. '
        user_content = f"""Dear {instance.author.email}:,<br><br>

                                          Congratulations! Your Post has been  successfully

                                          Thanks & regards<br>
                                          Team """

        recipient_list = [instance.author.email, ]
        sender = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, user_content, sender, recipient_list, html_message=user_content)

