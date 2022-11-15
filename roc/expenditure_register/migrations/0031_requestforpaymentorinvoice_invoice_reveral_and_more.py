# Generated by Django 4.0.5 on 2022-09-27 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expenditure_register', '0030_alter_payment_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestforpaymentorinvoice',
            name='invoice_reveral',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='expenditure_register.requestforpaymentorinvoice', verbose_name='Τιμολόγιο για αντιλογισμό.'),
        ),
        migrations.AddField(
            model_name='requestforpaymentorinvoice',
            name='is_payment_reversal',
            field=models.BooleanField(default=False, verbose_name='Αντιλογισμός'),
        ),
    ]
