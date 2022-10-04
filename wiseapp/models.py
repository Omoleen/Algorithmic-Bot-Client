from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
import random
import secrets
import string
from .utils import generate_ref_code
# Create your models here.
from .email import balance_low


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    risk_profile = models.CharField(max_length=12, default='medium', choices=(('vlow', 'vLow'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('vhigh', 'vHigh')))
    API_KEY = models.CharField(max_length=200, blank=True, default='')
    API_SECRET = models.BinaryField(blank=True,)
    TransactionID = models.CharField(max_length=200, blank=True, default='')
    wallet = models.DecimalField(max_digits=20, decimal_places=3, default=0.000)  # account balance
    paid_month = models.BooleanField(default=False)
    num_of_months = models.IntegerField(default=0)
    profit_value = models.CharField(max_length=200, blank=True, default='')
    profit_flag = models.BooleanField(default=False)
    run_flag = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='ref_by')
    forgot_password_token = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    date_activated = models.DateTimeField(editable=False, blank=True, null=True)
    settings_flag = models.BooleanField(default=True)
    run_profile_button_flag = models.BooleanField(default=False)
    wallet_activate_flag = models.BooleanField(default=False)
    status_code = models.IntegerField(default=0, choices=((-1, -1), (100, 100), (0, 0)))
    referral_level = models.IntegerField(default=0, choices=((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))
    referral_commission = models.IntegerField(default=5, choices=((5, 5), (7, 7), (10, 10), (14, 14), (19, 19), (25, 25)))
    referral_earned = models.DecimalField(max_digits=20, decimal_places=5, default=0.000)

    def __str__(self):
        return f"{self.user.username} Profile"

    def get_recommended_profiles(self):
        qs = Profile.objects.all()
        my_recs = [p for p in qs if p.recommended_by == self.user and p.paid_month]
        return len(my_recs)

    def update_referrals(self):
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

    def save(self, *args, **kwargs):
        if self.referral_code == "":
            code = generate_ref_code()
            self.referral_code = code
        if self.date_activated is None:
            if self.paid_month:
                self.date_activated = timezone.make_aware(datetime.now())
        if not self.paid_month:
            self.date_activated = None
        if self.wallet >= 3 and self.date_activated:
            self.wallet_activate_flag = True
        else:
            self.wallet_activate_flag = False
        if self.wallet_activate_flag and self.run_profile_button_flag:
            self.run_flag = True
        else:
            self.run_flag = False
        if not self.paid_month:
            self.num_of_months = 0
        self.update_referrals()
        super().save(*args, **kwargs)


# class MultiReferral(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     parent2 = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='ref2_by')
#     parent3 = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='ref3_by')
#     parent4 = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='ref4_by')
#     parent5 = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='ref5_by')
#
#     def __str__(self):
#         return f"{self.user.username} Parent Referrals"


class Code(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=7, blank=True)

    def __str__(self):
        return f"{self.user.username} OTP"

    def save(self, *args, **kwargs):
        alphabet = string.ascii_letters + string.digits
        code_string = ''.join(secrets.choice(alphabet) for i in range(7))
        # print(code_string)
        self.number = str(code_string)
        super().save(*args, **kwargs)


class TransactionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    TransactionID = models.CharField(max_length=200, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)
    TransactionCreated = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.BooleanField(default=False)  # to check if deposit has been added to wallet balance
    status_code = models.IntegerField(default=0, choices=((-1, -1), (100, 100), (0, 0)))  # for frontend update
    type = models.CharField(max_length=12, default='deposit', choices=(('deposit', 'deposit'), ('withdrawal', 'withdrawal'), ('transfer', 'transfer')))

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        if self.TransactionID == '':
            number = TransactionHistory.objects.filter(user=self.user)
            if number == None:
                number = '0001'
            else:
                number = len(number) + 1
                if number < 10:
                    number = f'000{number}'
                else:
                    if number < 100:
                        number = f'00{number}'
                    else:
                        if number < 1000:
                            number = f'0{number}'
            if self.type == 'transfer':
                self.TransactionID = f'Transfer{number}'
            elif self.type == 'withdrawal':
                self.TransactionID = f'Withdrawal{number}'
        super().save(*args, **kwargs)


class BotErrors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Error = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username}"
