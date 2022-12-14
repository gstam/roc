# Generated by Django 4.0.5 on 2022-07-06 10:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('expenditure_register', '0012_rename_exitaccount_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestforpaymentorinvoice',
            name='computed_maturation_start_date',
            field=models.DateField(default=datetime.datetime(2022, 7, 7, 10, 28, 57, 600096, tzinfo=utc), verbose_name='Ημερομηνία έναρξης ωρίμανσης'),
        ),
        migrations.AlterField(
            model_name='requestforpaymentorinvoice',
            name='computed_payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 7, 7, 10, 28, 57, 600111, tzinfo=utc), verbose_name='Ημερομηνία δημιουργίας υποχρέωσης'),
        ),
        migrations.AlterField(
            model_name='requestforpaymentorinvoice',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 8, 5, 10, 28, 57, 600057, tzinfo=utc), verbose_name='Ημερομηνία παραλαβής αγαθών, υπηρεσιών ή εργασιών'),
        ),
    ]
