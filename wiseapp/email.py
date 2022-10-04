from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from Wise.settings import BASE_URL
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
import os


def verification_email(username, email, code):
    context = {
        'name': username.title,
        'email': email,
        'code': code,
    }

    email_subject = 'Wise-X OTP'
    email_body = render_to_string('verificationmail.html', context)

    email = EmailMultiAlternatives(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    email.content_subtype = "html"
    # email.mixed_subtype = 'related'
    # img_dir = 'static'
    # logo = 'images/LOGO.png'
    # file_path = os.path.join(os.path.dirname(__file__), logo)
    # with open(file_path, 'r') as f:
    #     img = MIMEImage(f.read())
    #     img.add_header('Content-ID', '<{name}>'.format(name=logo))
    #     img.add_header('Content-Disposition', 'inline', filename=logo)
    # email.attach(img)
    return email.send(fail_silently=False)


def transaction_created_email(username, email, txid, amount, recvr_addr):
    context = {
        'name': username.title,
        'email': email,
        'txid': txid,
        'amount': amount,
        'recvr_addr': recvr_addr
    }

    email_subject = f"Wise-X Transaction Created: {txid}"
    email_body = render_to_string('transaction_created.html', context)

    email = EmailMultiAlternatives(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    email.content_subtype = "html"
    # email.mixed_subtype = 'related'
    # img_dir = 'static'
    # logo = 'images/LOGO.png'
    # file_path = os.path.join(os.path.dirname(__file__), logo)
    # with open(file_path, 'r') as f:
    #     img = MIMEImage(f.read())
    #     img.add_header('Content-ID', '<{name}>'.format(name=logo))
    #     img.add_header('Content-Disposition', 'inline', filename=logo)
    # email.attach(img)
    return email.send(fail_silently=False)


def transaction_successful_email(username, email, txid, amount, recvr_addr):
    context = {
        'name': username.title,
        'email': email,
        'txid': txid,
        'amount': amount,
        'recvr_addr': recvr_addr
    }

    email_subject = f"Wise-X Transaction Successful: {txid}"
    email_body = render_to_string('transaction_successful.html', context)

    email = EmailMultiAlternatives(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    email.content_subtype = "html"
    # email.mixed_subtype = 'related'
    # img_dir = 'static'
    # logo = 'images/LOGO.png'
    # file_path = os.path.join(os.path.dirname(__file__), logo)
    # with open(file_path, 'r') as f:
    #     img = MIMEImage(f.read())
    #     img.add_header('Content-ID', '<{name}>'.format(name=logo))
    #     img.add_header('Content-Disposition', 'inline', filename=logo)
    # email.attach(img)
    # image = 'images/check-icon.png'
    # file_path = os.path.join(os.path.dirname(__file__), image)
    # with open(file_path, 'r') as f:
    #     img1 = MIMEImage(f.read())
    #     img1.add_header('Content-ID', '<{name}>'.format(name=image))
    #     img1.add_header('Content-Disposition', 'inline', filename=image)
    # email.attach(img1)
    return email.send(fail_silently=False)


def transaction_timeout_email(username, email, txid, amount, recvr_addr):
    context = {
        'name': username.title,
        'email': email,
        'txid': txid,
        'amount': amount,
        'recvr_addr': recvr_addr
    }

    email_subject = f"Wise-X Transaction Timed Out: {txid}"
    email_body = render_to_string('transaction_timeout.html', context)

    email = EmailMultiAlternatives(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    email.content_subtype = "html"
    # email.mixed_subtype = 'related'
    # img_dir = 'static'
    # logo = 'images/LOGO.png'
    # file_path = os.path.join(os.path.dirname(__file__), logo)
    # with open(file_path, 'r') as f:
    #     img = MIMEImage(f.read())
    #     img.add_header('Content-ID', '<{name}>'.format(name=logo))
    #     img.add_header('Content-Disposition', 'inline', filename=logo)
    # email.attach(img)
    # image = 'images/x.png'
    # file_path = os.path.join(os.path.dirname(__file__), image)
    # with open(file_path, 'r') as f:
    #     img1 = MIMEImage(f.read())
    #     img1.add_header('Content-ID', '<{name}>'.format(name=image))
    #     img1.add_header('Content-Disposition', 'inline', filename=image)
    # email.attach(img1)
    return email.send(fail_silently=False)


def monthly_reminder_mail(some_par, email):
    context = {
        'email': email,
    }

    email_subject = f"Wise-X Activation Reminder"
    email_body = render_to_string('monthly_reminder.html', context)

    email = EmailMultiAlternatives(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    email.content_subtype = "html"
    # email.mixed_subtype = 'related'
    # img_dir = 'static'
    # logo = 'images/LOGO.png'
    # file_path = os.path.join(os.path.dirname(__file__), logo)
    # with open(file_path, 'r') as f:
    #     img = MIMEImage(f.read())
    #     img.add_header('Content-ID', '<{name}>'.format(name=logo))
    #     img.add_header('Content-Disposition', 'inline', filename=logo)
    # email.attach(img)
    # image = 'images/mail.png'
    # file_path = os.path.join(os.path.dirname(__file__), image)
    # with open(file_path, 'r') as f:
    #     img1 = MIMEImage(f.read())
    #     img1.add_header('Content-ID', '<{name}>'.format(name=image))
    #     img1.add_header('Content-Disposition', 'inline', filename=image)
    # email.attach(img1)
    return email.send(fail_silently=False)


def monthly_successful(email):
    context = {
        'email': email,
    }

    email_subject = f"Wise-X Activation Payment Successful"
    email_body = render_to_string('monthly_successful.html', context)

    email = EmailMultiAlternatives(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    email.content_subtype = "html"
    # email.mixed_subtype = 'related'
    # img_dir = 'static'
    # logo = 'images/LOGO.png'
    # file_path = os.path.join(os.path.dirname(__file__), logo)
    # with open(file_path, 'r') as f:
    #     img = MIMEImage(f.read())
    #     img.add_header('Content-ID', '<{name}>'.format(name=logo))
    #     img.add_header('Content-Disposition', 'inline', filename=logo)
    # email.attach(img)
    # image = 'images/check-icon.png'
    # file_path = os.path.join(os.path.dirname(__file__), image)
    # with open(file_path, 'r') as f:
    #     img1 = MIMEImage(f.read())
    #     img1.add_header('Content-ID', '<{name}>'.format(name=image))
    #     img1.add_header('Content-Disposition', 'inline', filename=image)
    # email.attach(img1)
    return email.send(fail_silently=False)


def monthly_failed(email):
    context = {
        'email': email,
    }

    email_subject = f"Wise-X Activation Payment Failed"
    email_body = render_to_string('monthly_failed.html', context)

    email = EmailMultiAlternatives(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    email.content_subtype = "html"
    # email.mixed_subtype = 'related'
    # img_dir = 'static'
    # logo = 'images/LOGO.png'
    # file_path = os.path.join(os.path.dirname(__file__), logo)
    # with open(file_path, 'r') as f:
    #     img = MIMEImage(f.read())
    #     img.add_header('Content-ID', '<{name}>'.format(name=logo))
    #     img.add_header('Content-Disposition', 'inline', filename=logo)
    # email.attach(img)
    # image = 'images/x.png'
    # file_path = os.path.join(os.path.dirname(__file__), image)
    # with open(file_path, 'r') as f:
    #     img1 = MIMEImage(f.read())
    #     img1.add_header('Content-ID', '<{name}>'.format(name=image))
    #     img1.add_header('Content-Disposition', 'inline', filename=image)
    # email.attach(img1)
    return email.send(fail_silently=False)


def balance_low(email):
    context = {
        'email': email,
    }

    email_subject = f"Wise-X Balance Running Low"
    email_body = render_to_string('balance_low.html', context)

    email = EmailMultiAlternatives(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    email.content_subtype = "html"
    # email.mixed_subtype = 'related'
    # img_dir = 'static'
    # logo = 'images/LOGO.png'
    # file_path = os.path.join(os.path.dirname(__file__), logo)
    # with open(file_path, 'r') as f:
    #     img = MIMEImage(f.read())
    #     img.add_header('Content-ID', '<{name}>'.format(name=logo))
    #     img.add_header('Content-Disposition', 'inline', filename=logo)
    # email.attach(img)
    # image = 'images/ex.png'
    # file_path = os.path.join(os.path.dirname(__file__), image)
    # with open(file_path, 'r') as f:
    #     img1 = MIMEImage(f.read())
    #     img1.add_header('Content-ID', '<{name}>'.format(name=image))
    #     img1.add_header('Content-Disposition', 'inline', filename=image)
    # email.attach(img1)
    return email.send(fail_silently=False)


def forgot_password_email(username, email, token):
    context = {
        'username': username.title,
        'email': email,
        'token': token,
        'BASE_URL': BASE_URL,
    }

    email_subject = f"Wise-X Reset Password"
    email_body = render_to_string('reset_password.html', context)

    email = EmailMultiAlternatives(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    email.content_subtype = "html"
    # email.mixed_subtype = 'related'
    # img_dir = 'static'
    # logo = 'images/LOGO.png'
    # file_path = os.path.join(os.path.dirname(__file__), logo)
    # with open(file_path, 'r') as f:
    #     img = MIMEImage(f.read())
    #     img.add_header('Content-ID', '<{name}>'.format(name=logo))
    #     img.add_header('Content-Disposition', 'inline', filename=logo)
    # email.attach(img)
    return email.send(fail_silently=False)
