import rncryptor
from django.http import HttpResponse
from django.utils.timezone import is_aware
import time
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Profile, Code
# from .models import MultiReferral
import uuid
from .models import TransactionHistory
from .email import transaction_created_email
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from wiseapp import Cryptopayments
from Wise import settings
from Wise.settings import BASE_URL, BINANCE_API_SECRET
from Wise.celery import make_payments, send_otp, otp_change, forgot_password, referral_and_wallet_update


def landing(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(referral_code=code)
        request.session['ref_profile'] = profile.id
        # print(profile.id)
    except:
        pass
    return render(request, 'page-landing.html')


# register page
def register(request):  # sign up
    # use = User.objects.get(id=16)
    # sample, boolcreated = Profile.objects.update_or_create(user=use)
    # print(sample, boolcreated)
    # try:
    #     x = 0
        # referral_id = request.session.get('ref_profile')
        # if referral_id is not None:
        #     referred_by = Profile.objects.get(id=referral_id)
        #     print(referred_by.user)
        #     x = 1
        # parent2_profile = Profile.objects.get(user=referred_by.user)
        # print(parent2_profile.recommended_by)
        # parent3_profile = Profile.objects.get(user=parent2_profile.recommended_by)
        # print(parent3_profile.recommended_by)
        # parent4_profile = Profile.objects.get(user=parent3_profile.recommended_by)
        # print(parent4_profile.recommended_by)

        # print(request.sess)
        # if not request.user.is_authenticated:
        #     messages.info(request, 'Please Login or Register')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        terms = request.POST.getlist('terms[]')
        if 'accepted' in terms:
            if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():
                messages.error(request, f"{username} and {email} already exist")
            elif User.objects.filter(username=username).exists():
                messages.error(request, f"{username} already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, f"{email} already exists")
            else:
                if password1 == password2:
                    user = User.objects.create_user(username, email, password1)
                    user.save()
                    user = authenticate(request, username=username, password=password1)
                    if user is not None:
                        login(request, user)
                        # referral_id = request.session.get('ref_profile')
                        # if referral_id is not None:
                        #     referred_by = Profile.objects.get(id=referral_id)
                        #     registered_profile = Profile.objects.get(user=request.user)
                        #     registered_profile.recommended_by = referred_by.user  # direct referral - step 1
                        #     registered_profile.save()

                        # if x == 1:
                        #     registered_profile = Profile.objects.get(user=request.user)
                        #     registered_profile.recommended_by = referred_by.user  # direct referral - step 1
                        #     registered_profile.save()
                            # multiref = MultiReferral.objects.get(user=request.user)
                            # parent2_profile = Profile.objects.get(user=referred_by.user)
                            # # print(parent2_profile.recommended_by)
                            # # parent2_profile = Profile.objects.get(user=referred_by.user)
                            # # print(parent2_profile.recommended_by)
                            # parent3_profile = Profile.objects.get(user=parent2_profile.recommended_by)
                            # # print(parent3_profile.recommended_by)
                            # parent4_profile = Profile.objects.get(user=parent3_profile.recommended_by)
                            # # print(parent4_profile.recommended_by)
                            # parent5_profile = Profile.objects.get(user=parent4_profile.recommended_by)
                            # # print(parent5_profile.recommended_by)
                            # multiref = MultiReferral.objects.get(user=request.user)
                            # multiref.parent2 = parent2_profile.recommended_by  # referral of direct referral - step 2
                            # multiref.parent3 = parent3_profile.recommended_by  # referral of referral of direct referral - step 3
                            # multiref.parent4 = parent4_profile.recommended_by  # referral of referral of direct referral - step 4
                            # multiref.parent5 = parent5_profile.recommended_by  # referral of referral of direct referral - step 5
                            # multiref.save()
                        return redirect('profile_page')
                else:
                    messages.error(request, f"Passwords do not match")
                    return redirect('register')
        else:
            messages.error(request, 'You have to accept our terms before signing up')
    # except:
    #     messages.error(request, 'Error!')
    #     return redirect('register')
    return render(request, 'pages-register.html')


# login page
def loginpage(request):  # login
    # try:
    if request.user.is_authenticated:
        return redirect('profile_page')  # come back to settings
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            request.session['forgotuser'] = username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile_page')
            # request.session['pk'] = user.pk
            # otp_model = Code.objects.get(user=user)
            # code = otp_model.number
            # send_otp(user.username, user.email, code)
            # send_otp.delay(user.username, user.email, code)
            # otp_change.apply_async((user.pk,), countdown=600)
            # messages.info(request, 'Your OTP has been sent to your email')
            # return redirect('verification_page')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    # except:
    #     return redirect('login')
    return render(request, "pages-login.html")


# OTP CHANGE
def verify(request):
    try:
        pk = request.session.get('pk')
        if pk:
            user = User.objects.get(pk=pk)
            print(user)
            otp_model = Code.objects.get(user=user)
            print(f'user: {otp_model.user}')
            print(f'pk: {user.username}')
            code = otp_model.number
            if request.POST:
                num = request.POST.get('OTP')
                if str(code) == str(num):
                    otp_model.save()
                    login(request, user)
                    return redirect('profile_page')
                else:
                    messages.error(request, 'Invalid OTP')
                    return render(request, 'verification.html')
            # messages.error(request, 'OTP Incorrect!')
            # return redirect('verification_page')
    except:
        return redirect('verification_page')

    return render(request, 'verification.html')


# forgot page
def forgotpage(request):  # forgot password
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            # password = request.POST.get('password')
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'No User found')
                return redirect('forgot-password')

            reset_user = User.objects.get(username=username)
            token = str(uuid.uuid4())
            print(token)
            reset_user_profile = Profile.objects.get(user=reset_user.id)
            reset_user_profile.forgot_password_token = token
            reset_user_profile.save()
            forgot_password.delay(username, reset_user.email, token)
            messages.success(request, 'An email has been sent')
    except:
        return redirect('forgot-password')
    return render(request, "forgot_password.html")


# forgot change page
def forgot_change_page(request, *args, **kwargs):  # change password
    token = str(kwargs.get('forgot_token'))
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('forgot-password')
        change_user_password_profile = Profile.objects.get(forgot_password_token=token)
        change_user_password = User.objects.get(username=change_user_password_profile.user)
        change_user_password.set_password(password1)
        change_user_password.save()
        login(request, change_user_password)
        return redirect('profile_page')
    return render(request, "change-password.html")


# profile page
@login_required()
def profile_page(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.paid_month:
        if len(profile.TransactionID) == 0:
            context = {
                'profile': profile,
                'trans_id': '',
                'receiver_add': '',
                'remainder': '',
                'error': 'Please click on button to generate payment information',
            }
        else:
            post_params1 = {
                'txid': profile.TransactionID,
            }
            client = Cryptopayments.CryptoPayments(settings.COINPAYMENTS_API_KEY, settings.COINPAYMENTS_API_SECRET, settings.IPN_URL)
            transactionInfo = client.getTransactionInfo(post_params1)
            context = {
                'month': False,
                'profile': profile,
                'trans_id': profile.TransactionID,
                'receiver_add': transactionInfo['payment_address'],
                'remainder': float(transactionInfo['amountf']) - float(transactionInfo['receivedf']),
                'error': 'NOT FULLY PAID or Transaction Pending....'
            }
    else:
        try:
            thprofile = TransactionHistory.objects.filter(user=request.user).last()
        except Exception as e:
            thprofile = None
        if thprofile is None:
            context = {
                'profile': profile,
                'trans_id': '',
                'receiver_add': '',
                'remainder': '',
                'error': 'Please click on button to generate payment information',
            }
        else:
            if thprofile.status_code == 0:
                post_params1 = {
                    'txid': thprofile.TransactionID,
                }
                client = Cryptopayments.CryptoPayments(settings.COINPAYMENTS_API_KEY, settings.COINPAYMENTS_API_SECRET, settings.IPN_URL)
                latesttransactionInfo = client.getTransactionInfo(post_params1)
                context = {
                    'profile': profile,
                    'thprofile': thprofile,
                    'trans_id': thprofile.TransactionID,
                    'receiver_add': latesttransactionInfo['payment_address'],
                    'remainder': float(latesttransactionInfo['amountf']) - float(latesttransactionInfo['receivedf']),
                }
            else:
                context = {
                    'profile': profile,
                    'trans_id': '',
                    'receiver_add': '',
                    'remainder': '',
                    'error': 'Please click on button to generate payment information',
                }

    return render(request, "profile.html", context)


# @login_required()
# def transactionpage(request):
#     profile = Profile.objects.get(user=request.user)
#     client = Cryptopayments.CryptoPayments(settings.COINPAYMENTS_API_KEY, settings.COINPAYMENTS_API_SECRET, settings.IPN_URL)
#     payment = request.POST.get('payment')
#     if payment == 'activate':
#         deposit = 50
#         if len(profile.TransactionID) == 0:
#             create_transaction_params = {
#                 'amount': deposit,
#                 'currency': 'USDT.TRC20',
#                 'buyer_email': request.user.email
#             }
#             transaction = client.createTransaction(create_transaction_params)
#             # time.sleep(2)
#             # print(transaction)
#             profile.TransactionID = transaction['txn_id']  # save transactionid in profile
#             # profile.transaction_type = 'activate'
#             profile.save()
#             post_params1 = {
#                 'txid' : transaction['txn_id'],
#             }
#             transactionInfo = client.getTransactionInfo(post_params1) #call coinpayments API using instance
#             # print(transactionInfo)
#             make_payments.delay(request.user.username, transaction['txn_id'], 'activate')
#             if transactionInfo['error'] == 'ok': #check error status 'ok' means the API returned with desired result
#                 context = {
#                     'amount': deposit,
#                     'trans_id': profile.TransactionID,
#                     'receiver_add': transactionInfo['payment_address'],
#                     'remainder': float(transactionInfo['amountf']) - float(transactionInfo['receivedf']),
#                 }
#             else:
#                 return redirect('transaction_page')
#         else:
#             post_params1 = {
#                 'txid' : profile.TransactionID,
#             }
#
#             transactionInfo = client.getTransactionInfo(post_params1) #call coinpayments API using instance
#
#             if transactionInfo['error'] == 'ok': #check error status 'ok' means the API returned with desired result
#                 context = {
#                     'amount': deposit,
#                     'trans_id': profile.TransactionID,
#                     'receiver_add': transactionInfo['payment_address'],
#                     'remainder': float(transactionInfo['amountf']) - float(transactionInfo['receivedf']),
#                 }
#     elif payment == 'add':
#         amount = request.POST.get('depamt')
#         create_transaction_params = {
#             'amount' : amount,
#             'currency' : 'USDT.TRC20',
#             'buyer_email' : request.user.email
#         }
#         transaction = client.createTransaction(create_transaction_params)
#         th = TransactionHistory()
#         th.user = request.user
#         th.TransactionID = transaction['txn_id']  # save transactionid in profile
#         th.amount = amount
#         th.save()
#         # th.TransactionCreated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         # make_payments.delay(request.user.username, transaction['txn_id'], 'add')
#         profile.transaction_type = 'add'
#         profile.save()
#
#         post_params1 = {
#             'txid' : th.TransactionID,
#         }
#
#         transactionInfo = client.getTransactionInfo(post_params1)  # call coinpayments API using instance
#         # th.status = transactionInfo['status']
#
#         # if transactionInfo['status'] == 100:  # add amount to wallet
#         #     profile.wallet += round(amount, 3)
#         #     profile.save()
#
#         context = {
#             'amount' : amount,
#             # 'profile': profile,
#             'trans_id': th.TransactionID,
#             'receiver_add': transactionInfo['payment_address'],
#             'remainder': float(transactionInfo['amountf']) - float(transactionInfo['receivedf']),
#         }
#         # right now whenever the page is loaded a new transaction is created so add the functionality to check for open transactions
#         # context = {}
#     # return render(request, "transaction.html")
#     # context = {
#     #     'amount': '',
#     #     'trans_id': '',
#     #     'receiver_add': '',
#     #     'remainder': '',
#     # }
#     return render(request, "transaction.html", context)


# HTMx functions
def check_username(request):
    username = request.POST.get('username')
    if User.objects.filter(username=username).exists():
        return HttpResponse('<div class="alert" style="background-color: red;"><span class="closebtn">&times;</span>Username is not Available.</div>')
    else:
        return HttpResponse('')


def check_email(request):
    email = request.POST.get('email')
    if User.objects.filter(email=email).exists():
        return HttpResponse('<div class="alert" style="background-color: red;"><span class="closebtn">&times;</span>Email is not Available.</div>')
    else:
        return HttpResponse('')


def check_password1(request):
    request.session['password1'] = request.POST.get('password1')
    return HttpResponse(status=204)


def check_password2(request):
    password2 = request.POST.get('password2')
    if password2 != request.session.get('password1'):
        request.session['password1'] = ''
        return HttpResponse('<div class="alert" style="background-color: red;"><span class="closebtn">&times;</span>Passwords do not match.</div>')
    else:
        return HttpResponse('')


def generate_transaction(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=request.user)
    client = Cryptopayments.CryptoPayments(settings.COINPAYMENTS_API_KEY, settings.COINPAYMENTS_API_SECRET, settings.IPN_URL)
    payment = request.POST.get('payment')
    num_of_months = 1
    context={}
    if payment == 'activate':
        request.session['payment'] = 'activate'
        deposit = 10
        if len(profile.TransactionID) == 0:
            create_transaction_params = {
                'amount': deposit,
                'currency1': 'USDT.TRC20',
                'currency2': 'USDT.TRC20',
                'buyer_email': request.user.email
            }
            transaction = client.createTransaction(create_transaction_params)
            # time.sleep(2)
            # print(transaction)
            print(transaction)


            post_params1 = {
                'txid' : transaction['txn_id'],
            }
            transactionInfo = client.getTransactionInfo(post_params1) #call coinpayments API using instance
            print(transactionInfo)

            if transactionInfo['error'] == 'ok': #check error status 'ok' means the API returned with desired result
                profile.TransactionID = transaction['txn_id']  # save transactionid in profile
                # profile.transaction_type = 'activate'
                profile.save()
                make_payments.delay(request.user.username, transaction['txn_id'], 'activate', num_of_months)
                # print('saved to db')
                context = {
                    'amount': deposit,
                    'trans_id': profile.TransactionID,
                    'receiver_add': transactionInfo['payment_address'],
                    'remainder': float(transactionInfo['amountf']) - float(transactionInfo['receivedf']),
                }
                transaction_created_email(user.username, user.email, profile.TransactionID, transactionInfo['amountf'], transactionInfo['payment_address'] )
                return render(request, 'generate-details.html', context)
            else:
                return redirect('profile_page')
        else:
            post_params1 = {
                'txid' : profile.TransactionID,
            }

            transactionInfo = client.getTransactionInfo(post_params1) #call coinpayments API using instance

            if transactionInfo['error'] == 'ok': #check error status 'ok' means the API returned with desired result
                context = {
                    'amount': deposit,
                    'trans_id': profile.TransactionID,
                    'receiver_add': transactionInfo['payment_address'],
                    'remainder': float(transactionInfo['amountf']) - float(transactionInfo['receivedf']),
                }
    elif payment == 'add':
        request.session['payment'] = 'add'
        amount = abs(Decimal(request.POST.get('depamt')))
        create_transaction_params = {
            'amount': amount,
            'currency1': 'USDT.TRC20',
            'currency2': 'USDT.TRC20',
            'buyer_email': request.user.email
        }
        transaction = client.createTransaction(create_transaction_params)
        th = TransactionHistory()
        th.user = request.user

        make_payments.delay(request.user.username, transaction['txn_id'], 'add')
        # profile.transaction_type = 'add'
        # profile.save()

        post_params1 = {
            'txid' : transaction['txn_id'],
        }

        transactionInfo = client.getTransactionInfo(post_params1)  # call coinpayments API using instance
        # th.status = transactionInfo['status']

        if transactionInfo['error'] == 'ok': #check error status 'ok' means the API returned with desired result
            th.TransactionID = transaction['txn_id']  # save transactionid in profile
            th.amount = amount
            th.save()
            context = {
                'amount': amount,
                'profile': profile,
                'trans_id': th.TransactionID,
                'receiver_add': transactionInfo['payment_address'],
                'remainder': float(transactionInfo['amountf']) - float(transactionInfo['receivedf']),
            }
            transaction_created_email(user.username, user.email, th.TransactionID, transactionInfo['amountf'], transactionInfo['payment_address'] )
            return render(request, 'generate-details.html', context)
        else:
            return redirect('profile_page')

    return render(request, 'generate-details.html', context)


# view to show if customer hasn't paid after an hour'
def load_check(request):
    print('xxxxx')
    profile = Profile.objects.get(user=request.user)
    if request.session.get('payment') == 'activate':
        if (profile.TransactionID == '' and not profile.paid_month) or (profile.TransactionID != '' and profile.paid_month):
            return render(request, 'make-deposit.html', {'profile': profile})
    elif request.session.get('payment') == 'add':
        thprofile = TransactionHistory.objects.filter(user=request.user).latest()
        if thprofile.status_code == 100 or thprofile.status_code == -1:
            return render(request, 'make-deposit.html', {'profile': profile})
    return HttpResponse(status=204)


def profile_change_password(request):
    curr = request.POST.get('password')
    new = request.POST.get('newpassword')
    confirm = request.POST.get('renewpassword')
    if confirm == new:
        user = User.objects.get(username=request.user.username)
        username = request.user.username
        if user.check_password(curr):
            user.set_password(new)
            user.save()
            # messages.info('Password changed Successfully!')
            context = {
                'message': 'Password changed Successfully!',
            }
            login(request, user)
        else:
            context = {
                'message': 'Password Incorrect'
            }
            # messages.info(request, )
    else:
        context = {
            'message': 'Passwords do not match'
        }
        # messages.info(request, )

    return render(request, 'profile-password.html', context)


def profile_change_API(request):
    try:
        profile = Profile.objects.get(user=request.user)
        API_KEY = request.POST.get('API_KEY')
        profile.API_KEY = API_KEY
        API_SECRET = request.POST.get('API_SECRET')
        encrypted_api_secret = rncryptor.encrypt(API_SECRET, BINANCE_API_SECRET)
        profile.API_SECRET = encrypted_api_secret
        profile.save()
        # messages.info(request, )
        context = {
            'message': f'API Key: {API_KEY[:5]}...... Set!'
        }
    except:
        context = {
            'message': 'Incorrect details'
        }
        # messages.error(request, 'Incorrect details')

    return render(request, 'profile-api.html', context)


def profile_change_settings(request):
    profile = Profile.objects.get(user=request.user)
    risk_profile = request.POST.get('riskprofile')
    message = ''
    print(risk_profile)
    if risk_profile != '':
        if risk_profile == 'low':
            profile.risk_profile = 'low'
            message = 'Low'
        if risk_profile == 'high':
            profile.risk_profile = 'high'
            message = 'High'
        if risk_profile == 'vhigh':
            profile.risk_profile = 'vhigh'
            message = 'Very High'
        if risk_profile == 'vlow':
            profile.risk_profile = 'vlow'
            message = 'Very Low'
        if risk_profile == 'medium':
            profile.risk_profile = 'medium'
            message = 'Medium'
        profile.settings_flag = True
        full_message = f'{message} Risk Profile set!'
    else:
        full_message = 'Error'
    profile.save()
    # messages.info(request, 'Settings Updated!')
    return render(request, 'profile-settings.html', context={'profile': profile, 'message': full_message})


def page404(request, exception):
    return render(request, '404.html', {'context': '404 Page not found'})


def binance_tutorial(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile': profile
    }
    return render(request, 'binapitutorial.html', context)


def referral_page(request):
    profile = Profile.objects.get(user=request.user)
    # commission = profile.referral_earned
    context = {
        'profile': profile,
        'BASE_URL': BASE_URL
        # 'commission': commission
    }
    return render(request, 'referrals.html', context)


def service(request):
    return render(request, 'service-agreement.html')


def privacy(request):
    return render(request, 'privacy.html')


def start_bot(request):
    profile = Profile.objects.get(user=request.user)
    profile.run_profile_button_flag = True
    profile.save()
    return render(request, 'startstop.html')


def stop_bot(request):
    profile = Profile.objects.get(user=request.user)
    profile.run_profile_button_flag = False
    profile.save()
    return render(request, 'startstop.html')


def walletbalance(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'walletbalance.html', {'profile': profile})


def error404(request, exception):
    return render(request, '404.html')


def error403(request, exception):
    return render(request, '403.html')


def error408(request, exception):
    return render(request, '408.html')


def error500(request, exception):
    return render(request, '500.html', status=500)


def activecheck(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'activecheck.html', {'profile': profile})


def fuelcheck(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'fuelcheck.html', {'profile': profile})


def checkbot(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'checkbot.html', {'profile': profile})


def transferwallet(request):
    amount = abs(Decimal(request.POST.get('withdrawalamt')))
    profile = Profile.objects.get(user=request.user)
    if profile.referral_earned >= amount:
        profile.referral_earned -= amount
        profile.wallet += amount
        profile.save()
        message = 'Transfer successful'
        th = TransactionHistory()
        th.user = request.user
        th.amount = amount
        th.type = 'transfer'
        th.status_code = 100
        th.status = True
        th.save()
    else:
        th = TransactionHistory()
        th.user = request.user
        th.amount = amount
        th.type = 'transfer'
        th.status_code = -1
        th.status = False
        th.save()
        message = 'Insufficient balance'
    return render(request, 'transferwallet.html', {'message': message, 'profile': profile})


def withdrawal(request):
    amount = abs(Decimal(request.POST.get('withdrawalamt')))
    address = request.POST.get('walletadr')
    profile = Profile.objects.get(user=request.user)
    if profile.referral_earned >= amount:
        client = Cryptopayments.CryptoPayments(settings.COINPAYMENTS_API_KEY, settings.COINPAYMENTS_API_SECRET, settings.IPN_URL)
        withdrawal_params = {
            'amount': amount,
            'currency': 'USDT.TRC20',
            'address': address,
            'auto_confirm': 1,
        }
        try:
            client_withdrawal = client.createWithdrawal(withdrawal_params)
            if client_withdrawal['status'] == 1:
                profile.referral_earned -= amount
                profile.save()
                message = 'Withdrawal successful'
                th = TransactionHistory()
                th.user = request.user
                th.amount = amount
                th.type = 'withdrawal'
                th.status_code = 100
                th.status = True
                th.save()
            else:
                th = TransactionHistory()
                th.user = request.user
                th.amount = amount
                th.type = 'withdrawal'
                th.status_code = -1
                th.status = False
                th.save()
                message = 'Please try again later'
        except:
            th = TransactionHistory()
            th.user = request.user
            th.amount = amount
            th.type = 'withdrawal'
            th.status_code = -1
            th.status = False
            th.save()
            message = 'Please try again later'
    else:
        th = TransactionHistory()
        th.user = request.user
        th.amount = amount
        th.type = 'withdrawal'
        th.status_code = -1
        th.status = False
        th.save()
        message = 'Insufficient balance'
    return render(request, 'withdrawal.html', {'message': message, 'profile': profile})


def transactions(request):
    thprofile = TransactionHistory.objects.filter(user=request.user)[::-1]
    return render(request, 'transactionhistory.html', {'thprofile': thprofile})