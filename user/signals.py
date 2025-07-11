from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.db.models.signals import m2m_changed
from events.models import Event

@receiver(post_save, sender = User)
def send_activation_mail(sender,instance,created,**kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f'{settings.FRONTEND_URL}/user/activate/{instance.id}/{token}/'

        subject = 'Activate Your Account'
        message = f'Hi {instance.username},\n\nplease activate your account by checking the link below:\n{activation_url},\n\nThank You!'
        recipient_list = [instance.email]

        try:
            send_mail(subject,message, settings.EMAIL_HOST_USER,recipient_list)
        except Exception as e:
            print(f'Faild to send email to {instance.email}: {str(e)}')

@receiver(m2m_changed, sender=Event.participants.through)
def send_booking_email(sender, instance, action, pk_set, **kwargs):

    if action == "post_add":
        for user_id in pk_set:
            user = instance.participants.model.objects.get(pk=user_id)

            subject = f'Booking Confirmation for {instance.name}'
            message = (
                f"Hi {user.first_name or user.username},\n\n"
                f"You have successfully booked the event:\n\n"
                f"Event: {instance.name}\n"
                f"Date: {instance.date}\n"
                f"Location: {instance.location}\n\n"
                f"Thank you for booking with Evora!"
            )
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
            except Exception as e:
                print(f"Failed to send confirmation email to {user.email}: {str(e)}")