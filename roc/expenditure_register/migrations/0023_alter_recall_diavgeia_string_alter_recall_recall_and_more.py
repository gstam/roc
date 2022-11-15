# Generated by Django 4.0.5 on 2022-09-27 06:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('expenditure_register', '0022_remove_account_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recall',
            name='diavgeia_string',
            field=models.CharField(max_length=100, verbose_name='ΑΔΑ Ανάκλησης'),
        ),
        migrations.AlterField(
            model_name='recall',
            name='recall',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ποσό Ανάκλησης'),
        ),
        migrations.AlterField(
            model_name='recall',
            name='recall_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Ημερομηνία Ανάκλησης'),
        ),
        migrations.AlterField(
            model_name='recall',
            name='recall_protocol_number',
            field=models.CharField(max_length=10, verbose_name='Αριθμός πρωτ. απόφασης ανάκλησης δέσμευσης'),
        ),
        migrations.AlterField(
            model_name='requestforpaymentorinvoice',
            name='computed_maturation_start_date',
            field=models.DateField(verbose_name='Ημερομηνία έναρξης ωρίμανσης'),
        ),
        migrations.AlterField(
            model_name='requestforpaymentorinvoice',
            name='computed_payment_due_date',
            field=models.DateField(blank=True, verbose_name='Ημερομηνία λήξης προθεσμίας υποχρέωσης (Μόνο για εμπορικές συναλλαγές)'),
        ),
        migrations.AlterField(
            model_name='requestforpaymentorinvoice',
            name='invoice_reception_date',
            field=models.DateField(verbose_name='Ημερομηνία παραλαβής τιμολογίου ή ισοδύναμου εγγράφου'),
        ),
        migrations.AlterField(
            model_name='requestforpaymentorinvoice',
            name='invoice_series',
            field=models.CharField(blank=True, max_length=10, verbose_name='Σειρά τιμολογίου ή άλλου φορολογικού στοιχείου'),
        ),
        migrations.AlterField(
            model_name='requestforpaymentorinvoice',
            name='obligation_creation_date',
            field=models.DateField(verbose_name='Ημερομηνία δημιουργίας υποχρέωσης'),
        ),
        migrations.AlterField(
            model_name='requestforpaymentorinvoice',
            name='payment_due_date',
            field=models.DateField(verbose_name='Συμβατικός χρόνος πληρωμής'),
        ),
        migrations.AlterField(
            model_name='requestforpaymentorinvoice',
            name='service_acceptance_verification_date',
            field=models.DateField(blank=True, verbose_name='Ημερομηνία έγκρισης παραλαβής αγαθών, υπηρεσιών ή εργασιών (Μόνο για εμπορικές συναλλαγές)'),
        ),
        migrations.AlterField(
            model_name='requestforpaymentorinvoice',
            name='service_reception_date',
            field=models.DateField(blank=True, verbose_name='Ημερομηνία παραλαβής αγαθών, υπηρεσιών ή εργασιών (Μόνο για εμπορικές συναλλαγές)'),
        ),
    ]
