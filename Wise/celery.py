from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Wise.settings')

app = Celery('Wise')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task(bind=True)
def make_payments(self, user, txid, x, num_of_months=0):
    from wiseapp import Cryptopayments
    from decimal import Decimal
    from Wise import settings
    from django.contrib.auth.models import User
    from wiseapp.models import Profile, Code, TransactionHistory
    from wiseapp.email import transaction_created_email, transaction_successful_email, transaction_timeout_email, verification_email
    import time

    client = Cryptopayments.CryptoPayments(settings.COINPAYMENTS_API_KEY, settings.COINPAYMENTS_API_SECRET, '')
    user = User.objects.get(username=user)
    profile = Profile.objects.get(user=user)
    post_params1 = {
        'txid' : txid,
    }
    transactionInfo = client.getTransactionInfo(post_params1)
    # transaction_created_email(user.username, user.email, txid, transactionInfo['amountf'], transactionInfo['payment_address'] )

    while True:
        print('qqqq')
        time.sleep(60)
        transactionInfo = client.getTransactionInfo(post_params1)
        if x == 'activate':
            if transactionInfo['status'] == 100:
                profile.paid_month = True
                profile.status_code = 100
                profile.num_of_months = num_of_months
                profile.save()
                return transaction_successful_email(user.username, user.email, txid, transactionInfo['amountf'], transactionInfo['payment_address'] )
            elif transactionInfo['status'] == -1:
                profile.TransactionID = ''
                profile.status_code = -1
                profile.paid_month = False
                profile.save()
                return transaction_timeout_email(user.username, user.email, txid, transactionInfo['amountf'], transactionInfo['payment_address'] )
        elif x == 'add':
            th = TransactionHistory.objects.get(user=user, TransactionID=txid)
            if transactionInfo['status'] == 100:
                profile.wallet += Decimal(str(th.amount))
                th.status = True
                th.status_code = 100
                th.save()
                profile.save()
                return transaction_successful_email(user.username, user.email, txid, transactionInfo['amountf'], transactionInfo['payment_address'] )
            elif transactionInfo['status'] == -1:
                th.status_code = -1
                th.save()
                return transaction_timeout_email(user.username, user.email, txid, transactionInfo['amountf'], transactionInfo['payment_address'] )


@app.task(bind=True)
def referral_and_wallet_update(self):
    from decimal import Decimal
    from django.contrib.auth.models import User
    from wiseapp.email import monthly_reminder_mail, monthly_successful, monthly_failed, balance_low
    from wiseapp.models import Profile
    # add profits
    profiles = Profile.objects.filter(profit_flag=True)
    # print(profiles)
    for profile in profiles:
        if profile.profit_flag:
            system_profit = abs((Decimal(profile.profit_value)) * 2)/10
            profile.wallet -= system_profit
            profile.profit_value = ''
            profile.profit_flag = False
            profile.save()
            if profile.wallet < 4.0:
                balance_low(User.objects.get(username=profile.user).email)
                # send email
            # multilevel referral
            if profile.recommended_by:
                step1 = Profile.objects.get(user=profile.recommended_by)
                # step1.wallet += Decimal(step1.referral_commission/100) * system_profit
                step1.referral_earned += Decimal(step1.referral_commission/100) * system_profit
                step1.save()
                print('done')
    #             # if step1.recommended_by:
    #             #     step2 = Profile.objects.get(user=step1.recommended_by)
    #             #     step2.wallet += Decimal(0.05)*system_profit
    #             #     step2.save()
    #             #     if step2.recommended_by:
    #             #         step3 = Profile.objects.get(user=step2.recommended_by)
    #             #         step3.wallet += Decimal(0.04)*system_profit
    #             #         step3.save()
    #             #         if step3.recommended_by:
    #             #             step4 = Profile.objects.get(user=step3.recommended_by)
    #             #             step4.wallet += Decimal(0.03)*system_profit
    #             #             step4.save()
    #         if profile.wallet < 2.0:
    #             if profile.wallet <= 0.0:
    #                 profile.run_flag = False
    #             user = User.objects.get(username=profile.user)
    #             balance_low(user.email)


# send OTP password
@app.task(bind=True)
def send_otp(self, username, email, code):
    from wiseapp.email import transaction_created_email, transaction_successful_email, transaction_timeout_email, verification_email
    return verification_email(username, email, code)


# reset password
@app.task(bind=True)
def forgot_password(self, username, email, token):
    from wiseapp.email import monthly_reminder_mail, monthly_successful, monthly_failed, balance_low, forgot_password_email
    return forgot_password_email(username, email, token)


# runs everyday to remind customers whose subscription will expire soon
@app.task(bind=True)
def subscription_reminder(self):
    from django.contrib.auth.models import User
    from wiseapp.models import Profile
    from wiseapp.email import monthly_reminder_mail
    from concurrent.futures import ThreadPoolExecutor
    from functools import partial
    from dateutil.relativedelta import relativedelta
    from datetime import datetime
    from django.utils import timezone
    users = User.objects.all()
    emails = []
    for user in users:
        profile = Profile.objects.get(user=user)
        warning_date = profile.date_activated + relativedelta(months=profile.num_of_months, days=-2)
        # delta = datetime.now(timezone.utc) - profile.date_activated
        # if delta.days == 178:
        if timezone.make_aware(datetime.now()) == warning_date:
            emails.append(user.email)
    # emails = [user.email for user in users]
    some_par = ''
    with ThreadPoolExecutor() as executor:
        fn = partial(monthly_reminder_mail, some_par)
        executor.map(fn, emails)


# runs everyday to deduct from customers whose subscription has expired
@app.task(bind=True)
def subscription_deduction(self):
    from decimal import Decimal
    from dateutil.relativedelta import relativedelta
    from django.contrib.auth.models import User
    from wiseapp.models import Profile
    from wiseapp.email import monthly_reminder_mail, monthly_successful, monthly_failed, balance_low
    from datetime import datetime
    from django.utils import timezone
    profiles = Profile.objects.all()
    for profile in profiles:
        if profile.date_activated is not None:
            user = User.objects.get(username=profile.user)
            expiry_date = profile.date_activated + relativedelta(months=profile.num_of_months)
            # delta = datetime.now(timezone.utc) - profile.date_activated
            print(expiry_date)
            # if (delta.days == 180) or (delta.days == 182) or (delta.days == 186):
            if timezone.make_aware(datetime.now()) == expiry_date:
                if profile.wallet > 50.0:
                    profile.wallet -= Decimal(50.0)
                    profile.paid_month = True
                    profile.save()
                    monthly_successful(user.email)
                    if profile.wallet <= 2.0:
                        # profile.run_flag = False
                        # profile.save()
                        balance_low(user.email)
                else:
                    profile.TransactionID = ''
                    profile.status_code = 0
                    profile.paid_month = False
                    profile.save()
                    monthly_failed(user.email)


# change OTP code after 1 hour
@app.task(bind=True)
def otp_change(self, pk):
    from django.contrib.auth.models import User
    from wiseapp.models import Profile, Code
    import secrets
    import string
    # print(user)
    user = User.objects.get(pk=pk)
    user = Code.objects.get(user=user)
    # print(user)
    alphabet = string.ascii_letters + string.digits
    user.number = str(''.join(secrets.choice(alphabet) for i in range(7)))
    user.save()


# runs every minute to check for new referrals
@app.task(bind=True)
def check_active_referrals(self):
    from wiseapp.models import Profile
    profiles = Profile.objects.all()
    for profile in profiles:
        if profile.get_recommended_profiles() < 101:
            profile.referral_level = 0
            profile.referral_commission = 5
        elif 100 < self.get_recommended_profiles() < 201:
            profile.referral_level = 1
            profile.referral_commission = 7
        elif 200 < self.get_recommended_profiles() < 301:
            profile.referral_level = 2
            profile.referral_commission = 10
        elif 300 < self.get_recommended_profiles() < 401:
            profile.referral_level = 3
            profile.referral_commission = 14
        elif 400 < self.get_recommended_profiles() < 501:
            profile.referral_level = 4
            profile.referral_commission = 19
        elif self.get_recommended_profiles() > 500:
            profile.referral_level = 5
            profile.referral_commission = 25
        profile.save()
