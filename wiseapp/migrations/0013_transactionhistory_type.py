# Generated by Django 3.2.13 on 2022-07-05 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiseapp', '0012_alter_profile_risk_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionhistory',
            name='type',
            field=models.CharField(choices=[('deposit', 'deposit'), ('withdrawal', 'withdrawal')], default='deposit', max_length=12),
        ),
    ]
