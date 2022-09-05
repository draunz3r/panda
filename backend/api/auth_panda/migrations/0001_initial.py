# Generated by Django 4.1 on 2022-08-27 19:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthEmployeeRegisterModel',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.UUIDField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(help_text='First name of the employee', max_length=100, verbose_name='First name')),
                ('last_name', models.CharField(help_text='Last name of the employee', max_length=100, verbose_name='Last name')),
                ('email_address', models.EmailField(help_text='Email address of the employee', max_length=250, verbose_name='Email address')),
                ('user_name', models.CharField(help_text='Username of employee', max_length=100, unique=True, verbose_name='Username')),
                ('password', models.CharField(help_text='Password of the account', max_length=100, validators=[django.core.validators.MinLengthValidator(8)], verbose_name='Password')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('last_logged_in', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]