from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from django.template.loader import render_to_string


@shared_task()
def send_feedback_email_task(subject,message,email_from,recipient_list,data_list):
    print("_______________BEFORE 10 SEC_________________")
    sleep(60)  # Simulate expensive operation(s) that freeze Django
    print("_______________AFTER 10 SEC_________________")
    send_mail(
        subject,
        message,
        email_from,
        recipient_list,
        html_message = render_to_string('mail.html',{'log_data_list': data_list})
    )


# @shared_task
# def send_feedback_email_task():
#     print("______હા મોજ હા_____")
#     return True

