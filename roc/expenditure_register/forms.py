from logging import PlaceHolder
from webbrowser import get
from django import forms
from django.forms import Form, ModelForm, Textarea, Select, HiddenInput, NumberInput, TextInput, CheckboxInput
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from .models import Account, Credit, Debit, Recall, RequestForPaymentOrInvoice, Payment
from django.utils.translation import gettext_lazy as _
from decimal import *
from .utils import compute_total_recall, compute_total_credit, compute_total_invoice_amount
from datetime import date
# from .views import get_account_balance

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = '__all__'  #('school_name', 'assignment_decision_protocol', 'ada_of_assignment_decision_protocol', 'assignment_start_date','assignment_end_date', 'hours_per_week', 'professor_contract')
        
        widgets = {
            'balance': NumberInput(attrs = {'readonly': 'readonly'}),
            'expenditure_register': HiddenInput(attrs = {'readonly': 'readonly'}),
        }


class CreditForm(ModelForm):
    class Meta:
        model = Credit
        fields = '__all__'  #('school_name', 'assignment_decision_protocol', 'ada_of_assignment_decision_protocol', 'assignment_start_date','assignment_end_date', 'hours_per_week', 'professor_contract')
        
        widgets = {
            'account': HiddenInput(), #attrs={'cols': 10, 'rows': 1, 'is_hidden' : True, 'readonly': True}
            # 'account':NumberInput(attrs = {'readonly': 'readonly'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        disposed_percentage = cleaned_data.get('disposed_percentage')
        # print(disposed_percentage)
        initial_credit = self.initial['initial_credit']
        initial_total_credit = self.initial['total_credit']
        initial_total_debit = self.initial['total_debit']
        credit = cleaned_data.get('credit')
        date = cleaned_data.get('date_of_disposal')
        # print(f'{initial_total_credit} {credit} {initial_credit} {initial_total_debit}')

        # if not self.instance.pk:
        #     total_amount_to_recall = total_credit - total_invoice - total_recall
        # else:
        #     total_amount_to_recall = total_credit - total_invoice - total_recall + self.initial['recall']
        if date > date.today():
            raise ValidationError(_('Η πίστωση δεν μπορεί να αφορά μελλοντικό χρόνο.'))
        if disposed_percentage is None:
            raise ValidationError(_('Μη έγκυρο ποσοστό διάθεσης!'))
        if not (disposed_percentage >= 0.00 and disposed_percentage <= 100.00 ) :
            raise ValidationError(_('Μη έγκυρο ποσοστό διάθεσης (%(disposed_percentage)s%%)'), params={'disposed_percentage': disposed_percentage,})
        if initial_total_credit + credit - initial_credit < initial_total_debit:
            raise ValidationError(_(f'Οι συνολικές δεσμεύσεις ξεπερνούν τη συνολική πίστωση μετά την μεταβολή {initial_credit}€ σε {credit}€'))


class DebitForm(ModelForm):
    class Meta:
        model = Debit
        fields = '__all__'  
        
        widgets = {
            'account': HiddenInput(attrs={'cols': 10, 'rows': 1, 'is_hidden' : True, 'readonly': True}),
            # 'account':NumberInput(attrs = {'readonly': 'readonly'}),
        }
 
    def clean(self):
        account = self.initial['account']
        cleaned_data = super().clean()
        debit = Decimal(cleaned_data.get('debit'))
        total_credit = self.initial['total_credit']
        initial_total_debit = self.initial["total_debit"]
        initial_debit_value = self.initial['initial_debit_value']
        invoices_charged_on_debit = self.initial['invoices_charged_on_debit']

        debit_date = cleaned_data.get('debit_date')
        diavgeia_date = cleaned_data.get('diavgeia_date')
        if debit_date > date.today():
            raise ValidationError(_('Η ημερομηνία της δέσμευσης δεν μπορεί να αφορά μελλοντικό χρόνο.'))
        if diavgeia_date > date.today():
            raise ValidationError(_('Η ημερομηνία ανάρτησης στη διαύγεια δεν μπορεί να αφορά σε μελλοντικό χρόνο.'))
        if debit_date > diavgeia_date:
            raise ValidationError(_('Η ημερομηνία της ανάρτησης στη διαύγεια δεν μπορεί προηγείται της ημερομηνίας της δέσμευσης.'))
        if debit < .0 :
            raise ValidationError(_('Καταχωρείστε το ποσό δέσμευσης ως θετικό αριθμό! (%(debit)s)'), params={'debit': debit,})
        elif debit > total_credit - initial_total_debit + initial_debit_value:
            raise ValidationError(_('Η διαθέσιμη πίστωση δεν επαρκεί για την δέσμευση %(debit).2f€!'), params={'debit': debit})
        elif debit < invoices_charged_on_debit:
            raise ValidationError(_("Το νέο ποσό της δέσμευσης είναι μικρότερο από το σύνολο των καταστάσεων πληρωμής ή τιμολογίων που έχουν χρεωθεί επ' αυτής."))
        else:
            pass


class RecallForm(ModelForm):
    class Meta:
        model = Recall
        fields = '__all__'  
        
        widgets = {
            'account': HiddenInput(attrs={'cols': 10, 'rows': 1, 'is_hidden' : True, 'readonly': True}),
            # 'account':NumberInput(attrs = {'readonly': 'readonly'}),
        }
 
    def clean(self):
        # print(self.initial)
        account = self.initial['account']
        cleaned_data = super().clean()
        recall = Decimal(cleaned_data.get('recall'))

        total_credit = compute_total_credit(self.initial['account_pk'])
        total_recall = compute_total_recall(self.initial['account_pk'])
        total_invoice = compute_total_invoice_amount(self.initial['account_pk'])
        if not self.instance.pk:
            total_amount_to_recall = total_credit - total_invoice - total_recall
        else:
            total_amount_to_recall = total_credit - total_invoice - total_recall + self.initial['recall']

        if recall < 0.0 :
            raise ValidationError(_('Καταχωρείστε το ποσό ανάκλησης ως θετικό αριθμό! (%(recall)s)'), params={'recall': recall,})
        elif recall > total_amount_to_recall:
            raise ValidationError(_(f'Το ποσό ανάκλησης {recall:0.2f}€ είναι μεγαλύτερο του ανακλήσιμου ποσού {total_amount_to_recall:0.2f}€!'))


class RequestForPaymentOrInvoiceForm(ModelForm):
    
    class Meta:
        model = RequestForPaymentOrInvoice
        fields = '__all__' 
        widgets = {
            'debit': HiddenInput(attrs={'cols': 10, 'rows': 1, 'is_hidden' : True, 'readonly': True}),
            #'debit':NumberInput(attrs = {'readonly': 'readonly'}),
            'transaction_is_commercial': CheckboxInput(attrs={'onclick':'js_is_commercial()'}),
            'invoice_created_by_us': CheckboxInput(attrs={'onclick':'js_invoice_created_by_us()'}),
            'service_reception_date': TextInput(attrs={'readonly':'readonly', 'placeholder':'dd/mm/yyyy'}),
            'service_acceptance_verification_date': TextInput(attrs={'readonly':'readonly', 'placeholder':'dd/mm/yyyy'}),
            'computed_payment_due_date': TextInput(attrs={'readonly':'readonly', 'placeholder':'dd/mm/yyyy'}),
            'obligation_creation_date': TextInput(attrs={'onclick':'js_suggest_obligation_date()'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        invoice_pk = cleaned_data.get("invoice_charge_amount")
        # initial_charge_ammount = self.initial["invoice_charge_amount"]
        # initial_debit = self.initial['debit']
        invoice_payment = self.initial['invoice_payment']
        initial_invoice_charge_amount = self.initial['invoice_charge_amount']
        total_invoice_amount_charged_on_debit = self.initial['invoices_charged_on_debit'] 
        new_invoice_charge_amount = cleaned_data.get("invoice_charge_amount")
        debit = cleaned_data.get("debit")
        residual_debit = (debit.debit - total_invoice_amount_charged_on_debit + initial_invoice_charge_amount)
        # if new_invoice_charge_amount < 0.0:
        #     raise ValidationError(_('Καταχωρείστε το ποσό του τιμολογίου ως θετικό αριθμό! (%(debit)s)'), params={'debit': debit,})
        # print(type(new_invoice_charge_amount))
        if new_invoice_charge_amount > residual_debit:
            raise ValidationError(_(f'Το διαθέσιμο ποσό από την τρέχουσα δέσμευση είναι {residual_debit} € ενώ η τρέχουσα δαπάνη απαιτεί: {round(new_invoice_charge_amount,2)} €')) #, params={'invoice_charge_amount':total_invoice_amount_charged_on_debit - initial_invoice_charge_amount, })))#
        elif new_invoice_charge_amount != initial_invoice_charge_amount and invoice_payment > Decimal(0.0) and invoice_payment == initial_invoice_charge_amount:
            raise ValidationError(_(f'Δεν μπορεί να ολοκληρωθεί η μεταβολή γιατί η παρούσα κατάσταση πληρωμής ή το παρόν τιμολόγιο έχει εξοφληθεί έναντι ποσού {invoice_payment} €.')) #, params={'invoice_charge_amount':total_invoice_amount_charged_on_debit - initial_invoice_charge_amount, })))#
        else:
            pass
        
        transaction_is_commercial = cleaned_data.get("transaction_is_commercial")
        # print(transaction_is_commercial)
        # if transaction_is_commercial == True:
        #     if invoice_reception_date 


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'  #('school_name', 'assignment_decision_protocol', 'ada_of_assignment_decision_protocol', 'assignment_start_date','assignment_end_date', 'hours_per_week', 'professor_contract')
        
        widgets = {
            'invoice': HiddenInput(attrs={'cols': 10, 'rows': 1, 'is_hidden' : True, 'readonly': True}),
            # 'invoice':NumberInput(attrs = {'readonly': 'readonly'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        invoice_pk = cleaned_data.get("invoice").pk
        invoice_charge_amount = RequestForPaymentOrInvoice.objects.get(pk = invoice_pk).invoice_charge_amount
        payment_amount = cleaned_data.get("payment_amount")
        # print(payment_amount, invoice_charge_amount)
        if payment_amount > 0 and payment_amount != invoice_charge_amount :
            raise ValidationError(_('Το ποσό του χρηματικού εντάλματος δεν αντιστοιχεί στο ποσό του τιμολόγιου ή του ισοδύναμου εγγράφου.'))


class RecallRequestToPdfForm(Form):
    recipients = forms.CharField(widget=forms.Textarea, required=True) #['1ο Γυμνάσιο Ηρακλείου', '2ο Γυμνάσιο Ηρακλείου', 'Παπαδάκης Νίκος', 'Παπαδάκης Μιχάλης']
    amount_in_text = forms.CharField(required=True) #'δέκα ευρώ και πενηντατρία λεπτά'
    amount = forms.DecimalField(required=True, decimal_places=2) #'10,53'
    protocol_number = forms.CharField(required=True) #'12324/ΔΕ/2ΣΦ'
    protocol_date = forms.DateField(required=True) # datetime.datetime.today().strftime("%d/%m/%Y")
    year = forms.CharField(max_length=4, required=True) #'2022'
    account = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        recipients = cleaned_data.get("recipients")
        amount_in_text = cleaned_data.get("amount_in_text")
        amount = cleaned_data.get("amount")
        protocol_number = cleaned_data.get("protocol_number")
        protocol_date = cleaned_data.get("protocol_date")
        year = cleaned_data.get("year")
        account = cleaned_data.get("account")
        print(recipients)

        # if payment_amount > 0 and payment_amount != invoice_charge_amount :
        #     raise ValidationError(_('Το ποσό του χρηματικού εντάλματος δεν αντιστοιχεί στο ποσό του τιμολόγιου ή του ισοδύναμου εγγράφου.'))