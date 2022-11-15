from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse

from .validators import *
import datetime


BUDGET_TYPE_CHOICES = [
    ('ΚΡΑΤΙΚΟΣ_ΠΡΟΫΠΟΛΟΓΙΣΜΟΣ','ΚΡΑΤΙΚΟΣ ΠΡΟΫΠΟΛΟΓΙΣΜΟΣ'),
    ('ΠΡΟΓΡΑΜΜΑ ΔΗΜΟΣΙΩΝ ΕΠΕΝΔΥΣΕΩΝ','ΠΡΟΓΡΑΜΜΑ ΔΗΜΟΣΙΩΝ ΕΠΕΝΔΥΣΕΩΝ'),
    ]


# Create your models here.
class ExpenditureRegister(models.Model):
    class Meta:
        unique_together = (('budget_type', 'year'),)

    budget_type = models.CharField(max_length = 32, choices=BUDGET_TYPE_CHOICES, default='ΚΡΑΤΙΚΟΣ_ΠΡΟΫΠΟΛΟΓΙΣΜΟΣ', verbose_name= _('Τύπος προϋπολογισμού'))
    year = models.PositiveSmallIntegerField(default = timezone.now().year, verbose_name = _('Οικονομικό Έτος'))
    organization = models.CharField(max_length = 20, default='1019', verbose_name= _('Φορέας'))
    special_organization = models.CharField(max_length = 20, default='206-9922000', verbose_name= _('Ειδικός Φορέας'))

    def __str__ (self):
        return str(self.year) # + " " + self.budget_type

    def get_absolute_url(self):
        return reverse('home') #reverse('register-detail', kwargs={'pk': self.pk})

account_CATEGORIES_TYPE_CHOICES = [
    ('ΙΔΙΩΤΕΣ','ΙΔΙΩΤΕΣ'),
    ('ΥΠΕΡΩΡΙΕΣ ΔΙΟΙΚΗΤΙΚΩΝ','ΥΠΕΡΩΡΙΕΣ ΔΙΟΙΚΗΤΙΚΩΝ'),
    ('ΜΗ ΛΗΨΗ ΑΔΕΙΑΣ','ΜΗ ΛΗΨΗ ΑΔΕΙΑΣ'),
    ('ΑΠΟΖΗΜΙΩΣΗ ΣΑΒΒΑΤΑ-ΚΥΡΙΑΚΕΣ','ΑΠΟΖΗΜΙΩΣΗ ΣΑΒΒΑΤΑ-ΚΥΡΙΑΚΕΣ'),
    ('ΑΠΟΖΗΜΙΩΣΗ ΣΑΒΒΑΤΑ-ΚΥΡΙΑΚΕΣ (ΙΔΟΧ)','ΑΠΟΖΗΜΙΩΣΗ ΣΑΒΒΑΤΑ-ΚΥΡΙΑΚΕΣ (ΙΔΟΧ)'),
    ('ΥΠΕΡΩΡΙΕΣ','ΥΠΕΡΩΡΙΕΣ'),
    ('ΩΡΟΜΙΣΘΙΟΙ','ΩΡΟΜΙΣΘΙΟΙ'),
    ('ΥΠΕΡΩΡΙΕΣ ΣΕ ΒΟΥΛΕΥΤΙΚΑ, ΠΟΛΙΤΙΚΑ ΓΡΑΦΕΙΑ','ΥΠΕΡΩΡΙΕΣ ΣΕ ΒΟΥΛΕΥΤΙΚΑ, ΠΟΛΙΤΙΚΑ ΓΡΑΦΕΙΑ'),
    ('ΟΔΟΙΠΟΡΙΚΑ','ΟΔΟΙΠΟΡΙΚΑ'),
    ('ΕΞΟΔΑ ΜΕΤΑΚΙΝΗΣΗΣ ΜΑΘΗΤΩΝ','ΕΞΟΔΑ ΜΕΤΑΚΙΝΗΣΗΣ ΜΑΘΗΤΩΝ'),
    ('ΗΜΕΡΗΣΙΑ ΑΠΟΖΗΜΙΩΣΗ','ΗΜΕΡΗΣΙΑ ΑΠΟΖΗΜΙΩΣΗ'),
    ('ΕΠΙΤΡΟΠΕΣ ΙΔΟΧ','ΕΠΙΤΡΟΠΕΣ ΙΔΟΧ'),
    ('ΕΠΙΤΡΟΠΕΣ','ΕΠΙΤΡΟΠΕΣ'),
    ('ΤΟΚΟΙ ΑΠΌ ΕΚΤΕΛΕΣΗ ΔΙΚΑΣΤΙΚΩΝ ΑΠΟΦΆΣΕΩΝ','ΤΟΚΟΙ ΑΠΌ ΕΚΤΕΛΕΣΗ ΔΙΚΑΣΤΙΚΩΝ ΑΠΟΦΆΣΕΩΝ'),
    ('ΛΟΙΠΕΣ ΑΠΟΖΗΜΙΩΣΕΙΣ ΣΕ ΕΚΤΕΛΕΣΗ ΔΙΚΑΣΤΙΚΩΝ ΑΠΟΦΑΣΕΩΝ','ΛΟΙΠΕΣ ΑΠΟΖΗΜΙΩΣΕΙΣ ΣΕ ΕΚΤΕΛΕΣΗ ΔΙΚΑΣΤΙΚΩΝ ΑΠΟΦΑΣΕΩΝ'),
    ('ΔΙΚΑΣΤΙΚΑ','ΔΙΚΑΣΤΙΚΑ'),
    ('ΞΕΝΟΓΛΩΣΣΑ','ΞΕΝΟΓΛΩΣΣΑ'),
    ('ΕΞΟΔΑ ΔΙΑΝΥΚΤΕΡΕΥΣΗΣ','ΕΞΟΔΑ ΔΙΑΝΥΚΤΕΡΕΥΣΗΣ'),
    ]


class Account(models.Model):
    number = models.IntegerField(verbose_name = _("ΑΛΕ"))
    # balance = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00, verbose_name= _('Διαθέσιμο Υπόλοιπο (€)'))
    category = models.CharField(max_length = 50, default='ΑΓΟΡΕΣ ΑΓΑΘΩΝ ΚΑΙ ΥΠΗΡΕΣΙΩΝ', verbose_name= _('Κατηγορία'))
    subcategory = models.CharField(max_length = 100,  choices=account_CATEGORIES_TYPE_CHOICES, verbose_name= _('Υποκατηγορία'))
    description = models.TextField(blank=True, verbose_name= _('Περιγραφή'))
    expenditure_register = models.ForeignKey(ExpenditureRegister, on_delete=models.CASCADE, verbose_name = _('Μητρώο Δεσμεύσεων'))

    def __str__(self):
        return str(self.number)

CREDIT_AUTHORIZATION_TYPE_CHOICES = [
    ('ΕΓΚΕΚΡΙΜΕΝΗ','ΕΓΚΕΚΡΙΜΕΝΗ'),
    ('ΑΝΑΜΟΡΦΩΣΗ','ΑΝΑΜΟΡΦΩΣΗ'),
    ]

# todo: dont allow the deletion of Credits unless the balance covers the sum of debits.
class Credit(models.Model):
    credit_reform = models.CharField(max_length = 100, default='ΑΝΑΜΟΡΦΩΣΗ', choices = CREDIT_AUTHORIZATION_TYPE_CHOICES, verbose_name= _('Τύπος Πίστωσης') )
    credit =  models.DecimalField(max_digits=20, decimal_places=2,  verbose_name = _('Ποσό Πίστωσης'))
    disposed_percentage =  models.DecimalField(max_digits=5, decimal_places=2, verbose_name = _('Ποσοστό Διάθεσης'))
    date_of_disposal = models.DateField(default = timezone.now, verbose_name = _('Ημερομηνία Πίστωσης'))
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name = _('ΑΛΕ'))
    
    
class Debit(models.Model):
    debit = models.DecimalField(max_digits=20, decimal_places=2, verbose_name = _('Ποσό Δέσμευσης'))
    debit_protocol_number = models.CharField(max_length = 10, verbose_name= _('Αριθμός πρωτ. απόφασης ανάληψης υποχρέωσης'))
    debit_date = models.DateField(default = timezone.now, verbose_name = _('Ημερομηνία Ανάληψης Υποχρέωσης'))
    diavgeia_string = models.CharField(max_length = 100, verbose_name= _('ΑΔΑ'))
    diavgeia_date = models.DateField(default = timezone.now, verbose_name = _('Ημερομηνία Ανάρτησης στη Διαύγεια'))
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name = _('ΑΛΕ'))

    def __str__(self):
        return self.debit_protocol_number


class Recall(models.Model):
    recall = models.DecimalField(max_digits=20, decimal_places=2, verbose_name = _('Ποσό Ανάκλησης'))
    recall_protocol_number = models.CharField(max_length = 10, verbose_name= _('Αριθμός πρωτ. απόφασης ανάκλησης δέσμευσης'))
    recall_date = models.DateField(default = timezone.now, verbose_name = _('Ημερομηνία Ανάκλησης'))
    diavgeia_string = models.CharField(max_length = 100, verbose_name= _('ΑΔΑ Ανάκλησης'))
    diavgeia_date = models.DateField(default = timezone.now, verbose_name = _('Ημερομηνία Ανάρτησης στη Διαύγεια'))
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name = _('ΑΛΕ'))

    def __str__(self):
        return self.recall_protocol_number

class Contract(models.Model):
    debit = models.ForeignKey(Debit, on_delete=models.CASCADE, verbose_name = _('Αριθμός απόφασης ανάληψης υποχρέωσης'))
    protocol_number = models.CharField(max_length = 10, verbose_name= _('Αριθμός σύμβασης'))
    date = models.DateField(default = timezone.now, verbose_name = _('Ημερομηνία Ανάρτησης στη Διαύγεια'))
    diavgeia_string = models.CharField(max_length = 100, verbose_name= _('ΑΔΑ'))
    diavgeia_date = models.DateField(default = timezone.now, verbose_name = _('Ημερομηνία Ανάρτησης στη Διαύγεια'))


OWNED_TO_TYPE_CHOICES = [
    ('ΤΡΙΤΟΥΣ','ΤΡΙΤΟΥΣ'),
    ('ΓΕΝΙΚΗ ΚΥΒΕΡΝΗΣΗ','ΓΕΝΙΚΗ ΚΥΒΕΡΝΗΣΗ'),
    ]


class RequestForPaymentOrInvoice(models.Model):
    owned_to = models.CharField(max_length = 100, default='ΤΡΙΤΟΥΣ', choices=OWNED_TO_TYPE_CHOICES, verbose_name= _('Υποχρέωση προς') )
    debit = models.ForeignKey(Debit, on_delete=models.CASCADE, verbose_name = _('Αριθμός απόφασης ανάληψης υποχρέωσης'))
    afm = models.CharField(max_length = 9, verbose_name= _('Α.Φ.Μ.'), validators = [validate_afm])
    creditor_is_abroad = models.BooleanField(default=False, verbose_name = _("Πιστωτής μόνιμα εγκατεστημένος στην αλλοδαπή"))
    transaction_is_commercial = models.BooleanField(default=False,verbose_name = _("Εμπορική Συναλλαγή"))
    invoice_series =  models.CharField(max_length = 10, null = True, blank = True, verbose_name= _('Σειρά τιμολογίου ή άλλου φορολογικού στοιχείου'))
    invoice_number =  models.CharField(max_length = 10, verbose_name= _('Αριθμός Τιμολογίου ή άλλου ισοδύναμου εγγράφου'))
    invoice_date = models.DateField(default = timezone.now, verbose_name = _('Ημερομηνία έκδοσης τιμολογίου ή ισοδύναμου εγγράφου'))
    invoice_created_by_us = models.BooleanField(default=False,verbose_name = _("Αυτόματη συμπλήρωση υπόλοιπων ημερομηνιών (Μόνο αν το τιμολόγιο εκδόθηκε από το φορέα μας. Ελέγξτε τα αποτελέσματα!)"))
    invoice_charge_amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name = _('Ποσό τιμολογίου ή ισοδύναμου εγγράφου'))
    invoice_reception_date = models.DateField(verbose_name = _('Ημερομηνία παραλαβής τιμολογίου ή ισοδύναμου εγγράφου'))
    service_reception_date = models.DateField(null = True, blank=True, verbose_name = _('Ημερομηνία παραλαβής αγαθών, υπηρεσιών ή εργασιών (Μόνο για εμπορικές συναλλαγές)'))
    service_acceptance_verification_date = models.DateField(null = True, blank=True, verbose_name = _('Ημερομηνία έγκρισης παραλαβής αγαθών, υπηρεσιών ή εργασιών (Μόνο για εμπορικές συναλλαγές)'))
    payment_due_date = models.DateField(verbose_name = _('Συμβατικός χρόνος πληρωμής'))
    obligation_creation_date = models.DateField(verbose_name = _('Ημερομηνία δημιουργίας υποχρέωσης')) # Is derived from the previous date fields
    computed_maturation_start_date = models.DateField(verbose_name = _('Ημερομηνία έναρξης ωρίμανσης')) # Is derived from previous date fields.
    computed_payment_due_date = models.DateField(null = True, blank = True, verbose_name = _('Ημερομηνία λήξης προθεσμίας υποχρέωσης (Μόνο για εμπορικές συναλλαγές)')) # Is derived from previous date fields.
    payment_in_advance = models.BooleanField(default = False, verbose_name = _("Πληρωμή μέσω Πάγιας Προκαταβολής ή Χρηματικού Εντάλματος Προπληρωμής"))

    def __str__(self):
        return str(self.debit.debit_protocol_number)

    @property
    def invoice_charge_amount_display(self):
        return  f'{self.invoice_charge_amount} €' 

PAYMENT_TYPE_CHOICES = [
    ('ΕΞΟΦΛΗΣΗ','ΕΞΟΦΛΗΣΗ'),
    ('ΑΠΟΡΡΙΨΗ','ΑΠΟΡΡΙΨΗ'),
    ('ΑΚΥΡΩΣΗ','ΑΚΥΡΩΣΗ'),
    ]

DOCUMENT_TYPE_CHOICES = [
    ('ΤΑΚΤΙΚΟ ΧΡΗΜΑΤΙΚΟ ΕΝΤΑΛΜΑ','ΤΑΚΤΙΚΟ ΧΡΗΜΑΤΙΚΟ ΕΝΤΑΛΜΑ'),
    ('ΧΡΗΜΑΤΙΚΟ ΕΝΤΑΛΜΑ ΠΡΟΠΛΗΡΩΜΗΣ','ΧΡΗΜΑΤΙΚΟ ΕΝΤΑΛΜΑ ΠΡΟΠΛΗΡΩΜΗΣ'),
    ('ΕΝΤΟΛΗ ΜΕΤΑΦΟΡΑΣ','ΕΝΤΟΛΗ ΜΕΤΑΦΟΡΑΣ'),
    ('ΣΥΜΨΗΦΙΣΤΙΚΟ ΕΝΤΑΛΜΑ','ΣΥΜΨΗΦΙΣΤΙΚΟ ΕΝΤΑΛΜΑ'),
    ('ΣΥΜΨΗΦΙΣΤΙΚΟ ΕΝΤΑΛΜΑ ΣΥΝΕΠΕΙΑ ΚΑΤΑΣΧΕΣΕΩΝ','ΣΥΜΨΗΦΙΣΤΙΚΟ ΕΝΤΑΛΜΑ ΣΥΝΕΠΕΙΑ ΚΑΤΑΣΧΕΣΕΩΝ'),
    ('ΑΚΥΡΩΤΙΚΟ ΕΝΤΑΛΜΑ','ΑΚΥΡΩΤΙΚΟ ΕΝΤΑΛΜΑ'),
    ] 

class Payment(models.Model):
    invoice = models.OneToOneField(RequestForPaymentOrInvoice, on_delete=models.CASCADE, verbose_name = _('Τιμολόγιο'))
    payment_type_choice = models.CharField(max_length = 100, choices=PAYMENT_TYPE_CHOICES, default='ΑΠΟΔΟΧΗ', verbose_name= _('Διαχείριση πληρωμής τιμολογίου ή ισοδύναμου εγγράφου'))
    number = models.CharField(max_length = 10, verbose_name= _('Αριθμός παραστατικού'))
    document_type = models.CharField(max_length = 100, choices= DOCUMENT_TYPE_CHOICES, default='', verbose_name= _('Είδος παραστατικού'))
    date = models.DateField(default = timezone.now, verbose_name = _('Ημερομηνία παραστατικού (Απόρριψη/Ακύρωση/Εξόφληση)'))
    payment_amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name = _('Συνολικό ποσό πληρωμής'))
    payment_amount_to_third_persons = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name = _('Συνολικό ποσό πληρωμής ληξιπρόθεσμων οφειλών > 90 ημερών προς τρίτους'))
    setoff_payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name = _('Εκ του οποίου συμψηφισμοί/παρακράτηση υπέρ Δημοσίου ή ΟΚΑ'))
