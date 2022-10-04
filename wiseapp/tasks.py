from __future__ import absolute_import, unicode_literals
from datetime import datetime
from datetime import timezone
from celery import shared_task
from wiseapp import Cryptopayments
from Wise import settings
from celery import Celery
from wiseapp.models import TransactionHistory
from django.contrib.auth.models import User
from .models import Profile, Code
from decimal import Decimal
from .email import transaction_created_email, transaction_successful_email, transaction_timeout_email, verification_email
from .email import monthly_reminder_mail, monthly_successful, monthly_failed, balance_low, forgot_password_email
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import secrets
import string
import time
from celery.utils.log import get_task_logger
celery = Celery(__name__)
logger = get_task_logger(__name__)
client = Cryptopayments.CryptoPayments(settings.COINPAYMENTS_API_KEY, settings.COINPAYMENTS_API_SECRET, '')


'''
gets triggered to update the database when there  is a successful transaction or timeout
gets triggered by transaction_type field, default will be an empty field so when the transaction is either successful or timedout it should be initialised to an empty string
possible values of the field
activate - to activate the bot
add - to add to the wallet
add checks for the latest record of a particular user in the TransactionHistory table and checks the status of the transaction id
'''
# @shared_task(bind=True)
# def make_payments(self, user, txid, x):
#     user = User.objects.get(username=user)
#     profile = Profile.objects.get(user=user)
#     post_params1 = {
#         'txid' : txid,
#     }
#     transactionInfo = client.getTransactionInfo(post_params1)
#     # transaction_created_email(user.username, user.email, txid, transactionInfo['amountf'], transactionInfo['payment_address'] )
#
#     while True:
#         time.sleep(60)
#         transactionInfo = client.getTransactionInfo(post_params1)
#         logger.info('Transaction pending....')
#         if x == 'activate':
#             if transactionInfo['status'] == 100:
#                 profile.paid_month = True
#                 profile.status_code = 100
#                 profile.save()
#                 return transaction_successful_email(user.username, user.email, txid, transactionInfo['amountf'], transactionInfo['payment_address'] )
#             elif transactionInfo['status'] == -1:
#                 profile.TransactionID = ''
#                 profile.status_code = -1
#                 profile.paid_month = False
#                 profile.save()
#                 return transaction_timeout_email(user.username, user.email, txid, transactionInfo['amountf'], transactionInfo['payment_address'] )
#         elif x == 'add':
#             th = TransactionHistory.objects.get(user=user, TransactionID=txid)
#             if transactionInfo['status'] == 100:
#                 profile.wallet += Decimal(str(th.amount))
#                 th.status = True
#                 th.status_code = 100
#                 th.save()
#                 profile.save()
#                 return transaction_successful_email(user.username, user.email, txid, transactionInfo['amountf'], transactionInfo['payment_address'] )
#             elif transactionInfo['status'] == -1:
#                 th.status_code = -1
#                 th.save()
#                 return transaction_timeout_email(user.username, user.email, txid, transactionInfo['amountf'], transactionInfo['payment_address'] )


# runs every minute to check if the bot has made profits on any account
'''
a scheduled task to be ran every minute to check the profit flag and add commissions for referrers  
'''
# @shared_task(bind=True)
# def wallet_update(self):
#     profiles = Profile.objects.filter(profit_flag=True)
#     print(profiles)
#
#     for profile in profiles:
#         if profile.profit_flag:
#             system_profit = abs((Decimal(profile.profit_value)) * 2)/10
#             profile.wallet -= system_profit
#             profile.profit_value = ''
#             profile.profit_flag = False
#             profile.save()
#             if profile.wallet < 4.0:
#                 balance_low(User.objects.get(username=profile.user).email)
#                 # send email
#             # multilevel referral
#             if profile.recommended_by:
#                 step1 = Profile.objects.get(user=profile.recommended_by)
#                 step1.wallet += step1.referral_commission/100 * system_profit
#                 step1.referral_earned += step1.referral_commission/100 * system_profit
#                 # step1.wallet += Decimal(0.1)*system_profit
#                 step1.save()
#                 print('done')
#     #             # if step1.recommended_by:
#     #             #     step2 = Profile.objects.get(user=step1.recommended_by)
#     #             #     step2.wallet += Decimal(0.05)*system_profit
#     #             #     step2.save()
#     #             #     if step2.recommended_by:
#     #             #         step3 = Profile.objects.get(user=step2.recommended_by)
#     #             #         step3.wallet += Decimal(0.04)*system_profit
#     #             #         step3.save()
#     #             #         if step3.recommended_by:
#     #             #             step4 = Profile.objects.get(user=step3.recommended_by)
#     #             #             step4.wallet += Decimal(0.03)*system_profit
#     #             #             step4.save()
#     #         if profile.wallet < 2.0:
#     #             if profile.wallet <= 0.0:
#     #                 profile.run_flag = False
#     #             user = User.objects.get(username=profile.user)
#     #             balance_low(user.email)
#
#
# # send OTP password
# @shared_task(bind=True)
# def send_otp(self, username, email, code):
#     return verification_email(username, email, code)
#
#
# # reset password
# @shared_task(bind=True)
# def forgot_password(self, username, email, token):
#     return forgot_password_email(username, email, token)
#
#
# # runs everyday to remind customers whose subscription will expire soon
# '''
# To be ran at the beginning of every day to check for users whose subscription will come to an end very soon this is to send a reminder
# '''
# @shared_task(bind=True)
# def monthly_reminder(self):
#     users = User.objects.all()
#     emails = []
#     for user in users:
#         profile = Profile.objects.get(user=user)
#         delta = datetime.now(timezone.utc) - profile.date_activated
#         if delta.days == 178:
#             emails.append(user.email)
#     # emails = [user.email for user in users]
#     some_par = ''
#     with ThreadPoolExecutor() as executor:
#         fn = partial(monthly_reminder_mail, some_par)
#         executor.map(fn, emails)
#
#
# # runs everyday to deduct from customers whose subscription has expired
# '''
# To be ran at the beginning of every day to check for users whose subscription will come to an end very soon this is to deduct and cancel those who havent paid
# '''
# @shared_task(bind=True)
# def monthly_deduction(self):
#     profiles = Profile.objects.all()
#     for profile in profiles:
#         if profile.date_activated is not None:
#             user = User.objects.get(username=profile.user)
#             delta = datetime.now(timezone.utc) - profile.date_activated
#             print(delta.days)
#             if (delta.days == 180) or (delta.days == 182) or (delta.days == 186):
#                 if profile.wallet > 50.0:
#                     profile.wallet -= Decimal(50.0)
#                     profile.paid_month = True
#                     profile.save()
#                     monthly_successful(user.email)
#                     if profile.wallet <= 2.0:
#                         # profile.run_flag = False
#                         # profile.save()
#                         balance_low(user.email)
#                 else:
#                     profile.TransactionID = ''
#                     profile.status_code = 0
#                     profile.paid_month = False
#                     # profile.run_flag = False
#                     profile.save()
#                     monthly_failed(user.email)
#
#
# # change OTP code after 1 hour
# @shared_task(bind=True)
# def otp_change(self, pk):
#     # print(user)
#     user = User.objects.get(pk=pk)
#     user = Code.objects.get(user=user)
#     # print(user)
#     alphabet = string.ascii_letters + string.digits
#     user.number = str(''.join(secrets.choice(alphabet) for i in range(7)))
#     user.save()
#
#
# # runs every minute to check for new referrals
# '''
# this to be ran every minute to update the number of active members paid_month must be set to true for their referees, can be set to daily or any time frame
# '''
# @shared_task(bind=True)
# def check_active_referrals(self):
#     profiles = Profile.objects.all()
#     for profile in profiles:
#         if profile.get_recommended_profiles() < 101:
#             profile.referral_level = 0
#             profile.referral_commission = 5
#         elif 100 < self.get_recommended_profiles() < 201:
#             profile.referral_level = 1
#             profile.referral_commission = 7
#         elif 200 < self.get_recommended_profiles() < 301:
#             profile.referral_level = 2
#             profile.referral_commission = 10
#         elif 300 < self.get_recommended_profiles() < 401:
#             profile.referral_level = 3
#             profile.referral_commission = 14
#         elif 400 < self.get_recommended_profiles() < 501:
#             profile.referral_level = 4
#             profile.referral_commission = 19
#         elif self.get_recommended_profiles() > 500:
#             profile.referral_level = 5
#             profile.referral_commission = 25
#         profile.save()
#
#
# '''
# EMAIL SETUP IS IN THE .env file I'll send to you
# '''
#
