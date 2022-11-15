from datetime import date, datetime, timedelta
from django.db.models import Avg, Count, Min, Sum
from django.core.exceptions import *
from django.shortcuts import redirect
from .models import *
from decimal import *


def compute_total_credit(account_pk, reference_date = datetime.datetime.today())->Decimal:
    account = Account.objects.get(pk = account_pk)

    account_credits = Credit.objects.filter(account=account).filter(date_of_disposal__lte = reference_date)
    credit_list = [(a.credit * a.disposed_percentage / Decimal(100.00)) for a in account_credits]
    total_credit = sum(credit_list)
    return  total_credit


def compute_initial_credit(account_pk, reference_date = datetime.datetime.today()):
    account = Account.objects.get(pk = account_pk)
    account_initial_credit = Decimal(0.0)

    try:
        account_initial_credit = Credit.objects.filter(account=account).filter(date_of_disposal__lte = reference_date).get(credit_reform='ΕΓΚΕΚΡΙΜΕΝΗ').credit
    except (MultipleObjectsReturned, ObjectDoesNotExist):
        pass
    
    if account_initial_credit is None:
        account_initial_credit = Decimal(0.0)
    else:
        account_initial_credit = Decimal(account_initial_credit)
        # print(account_initial_credit)
    return  account_initial_credit


def compute_reformed_credit(account_pk, reference_date = datetime.datetime.today()):
    account = Account.objects.get(pk = account_pk)
    account_initial_credit = Decimal(0.0)
    try:
        account_initial_credit = Credit.objects.filter(account=account).filter(date_of_disposal__lte = reference_date).filter(credit_reform='ΑΝΑΜΟΡΦΩΣΗ').aggregate(Sum('credit'))['credit__sum']
    except (MultipleObjectsReturned, ObjectDoesNotExist):
        pass

    print(reference_date, account_initial_credit)
    if account_initial_credit is None:
        account_initial_credit = Decimal(0.0)
    else:
        account_initial_credit = Decimal(account_initial_credit)
    
    print(account_initial_credit)
    return  account_initial_credit


def compute_disposed_percentage(account_pk, reference_date = datetime.datetime.today()):
    account = Account.objects.get(pk = account_pk)
    undiscounted_credit = Credit.objects.filter(account=account).filter(date_of_disposal__lte = reference_date).aggregate(Sum('credit'))['credit__sum']
    if undiscounted_credit is None:
        undiscounted_credit = Decimal(0.0)
    
    undiscounted_credit = Decimal(undiscounted_credit)

    account_credits = Credit.objects.filter(account=account).filter(date_of_disposal__lte = reference_date)
    credit_list = [(a.credit * a.disposed_percentage / Decimal(100.00)) for a in account_credits]

    if undiscounted_credit > 0.0:
        disposed_percentage = Decimal(100.0)*Decimal(sum(credit_list))/undiscounted_credit 
    else:
        disposed_percentage = Decimal(0)

    return  disposed_percentage


def compute_total_debit(account_pk, reference_date = datetime.datetime.today()):
    account = Account.objects.get(pk = account_pk)
    total_debit = Debit.objects.filter(account=account).filter(debit_date__lte = reference_date).aggregate(Sum('debit'))['debit__sum']
    if total_debit is None:
        total_debit = Decimal(0.0)
    return  total_debit


def compute_total_recall(account_pk, reference_date = datetime.datetime.today()):
    account = Account.objects.get(pk = account_pk)
    amount_to_recall = Recall.objects.filter(account=account).filter(recall_date__lte = reference_date).aggregate(Sum('recall'))['recall__sum']
    if amount_to_recall is None:
        amount_to_recall = Decimal(0.0)
    return amount_to_recall


def compute_total_invoice_amount(account_pk, reference_date = datetime.datetime.today()):
    account = Account.objects.get(pk = account_pk)
    account_debits = Debit.objects.filter(account = account).filter(debit_date__lte = reference_date)
    account_invoices__total_amount = RequestForPaymentOrInvoice.objects.filter(debit__in = list(account_debits)).filter(invoice_date__lte = reference_date).aggregate(Sum('invoice_charge_amount'))['invoice_charge_amount__sum']
    invoice_queryset = RequestForPaymentOrInvoice.objects.filter(debit__in = list(account_debits)).filter(invoice_date__lte = reference_date)
    account_invoices_with_canceled_payments__total_amount = Payment.objects.filter(invoice__in = list(invoice_queryset)).filter(payment_type_choice__in =['ΑΚΥΡΩΣΗ','ΑΠΟΡΡΙΨΗ']).aggregate(Sum('payment_amount'))['payment_amount__sum']
    if account_invoices__total_amount is None:
        account_invoices__total_amount = Decimal(0.00)
    if account_invoices_with_canceled_payments__total_amount is None:
        account_invoices_with_canceled_payments__total_amount = Decimal(0.00)
    
    return account_invoices__total_amount - account_invoices_with_canceled_payments__total_amount


def compute_total_prepaid_invoice_amount(account_pk, reference_date = datetime.datetime.today()):
    account = Account.objects.get(pk = account_pk)
    account_debits = Debit.objects.filter(account=account).filter(debit_date__lte = reference_date)
    #invoice_list = [i.invoice_charge_amount for d in account_debits for i in list(RequestForPaymentOrInvoice.objects.filter(debit = d.pk))]
    # invoice_queryset = RequestForPaymentOrInvoice.objects.filter(debit__in = list(account_debits))
    invoice_payment_in_advance = RequestForPaymentOrInvoice.objects.filter(debit__in = list(account_debits)).filter(invoice_date__lte = reference_date).filter(payment_in_advance = True).aggregate(Sum('invoice_charge_amount'))['invoice_charge_amount__sum']
    
    if invoice_payment_in_advance is None:
        invoice_payment_in_advance = Decimal(0.0)
    # print(invoice_payment_in_advance)
    return  invoice_payment_in_advance #payments


def compute_total_invoice_amount_owned_to_entity_within_time_frame(account_pk, owned_to_entity:str, reference_date:datetime.datetime, duration_lower_bound:datetime.timedelta, duration_upper_bound:datetime.timedelta) -> Decimal:
    account = Account.objects.get(pk = account_pk)
    account_debits = Debit.objects.filter(account=account)

    # print(f'Durations: {duration_lower_bound} {duration_upper_bound}, Today: {datetime.date.today()}, Lower Date: {datetime.date.today() - duration_lower_bound} Upper Date: {datetime.date.today() - duration_upper_bound}')
    # invoices_owned_to_entity = RequestForPaymentOrInvoice.objects.filter(debit__in = list(account_debits)).filter(owned_to = owned_to_entity).exclude(payment_in_advance = True).filter(computed_maturation_start_date__lte = datetime.date.today() - duration_lower_bound).filter(obligation_creation_date__gte = datetime.date.today() - duration_upper_bound)
    invoices_owned_to_entity = RequestForPaymentOrInvoice.objects.filter(debit__in = list(account_debits)).filter(owned_to = owned_to_entity).exclude(payment_in_advance = True).filter(computed_maturation_start_date__lte = reference_date - duration_lower_bound).filter(obligation_creation_date__gte = reference_date - duration_upper_bound)

    # Handling payments that have been canceled or turned down occurs automatically as long as the turned down or canceled payment amount equals the invoice amount.
    invoice_amount_owned_to_entity = invoices_owned_to_entity.aggregate(Sum('invoice_charge_amount'))['invoice_charge_amount__sum']
    payment_amount_owned_to_entity = Payment.objects.filter(invoice__in = list(invoices_owned_to_entity)).aggregate(Sum('payment_amount'))['payment_amount__sum']
    
    if invoice_amount_owned_to_entity is None:
        invoice_amount_owned_to_entity = Decimal(0.0)

    if payment_amount_owned_to_entity is None:
        payment_amount_owned_to_entity = Decimal(0.0)
    
    return  invoice_amount_owned_to_entity - payment_amount_owned_to_entity 


def compute_total_invoice_amount_owned_to_creditors_from_abroad(account_pk, owned_to_entity:str, reference_date:datetime.datetime, duration_lower_bound:datetime.timedelta, duration_upper_bound:datetime.timedelta) -> Decimal:
    account = Account.objects.get(pk = account_pk)
    account_debits = Debit.objects.filter(account=account)

    # print(f'Durations: {duration_lower_bound} {duration_upper_bound}, Today: {datetime.date.today()}, Lower Date: {datetime.date.today() - duration_lower_bound} Upper Date: {datetime.date.today() - duration_upper_bound}')
    invoices_owned_to_entity = RequestForPaymentOrInvoice.objects.filter(debit__in = list(account_debits)).filter(creditor_is_abroad = True).filter(owned_to = owned_to_entity).exclude(payment_in_advance = True).filter(computed_maturation_start_date__lte = reference_date - duration_lower_bound).filter(obligation_creation_date__gte = reference_date - duration_upper_bound)

    # Handling payments that have been canceled or turned down occurs automatically as long as the turned down or canceled payment amount equals the invoice amount.
    invoice_amount_owned_to_entity = invoices_owned_to_entity.aggregate(Sum('invoice_charge_amount'))['invoice_charge_amount__sum']
    payment_amount_owned_to_entity = Payment.objects.filter(invoice__in = list(invoices_owned_to_entity)).aggregate(Sum('payment_amount'))['payment_amount__sum']
    
    if invoice_amount_owned_to_entity is None:
        invoice_amount_owned_to_entity = Decimal(0.0)

    if payment_amount_owned_to_entity is None:
        payment_amount_owned_to_entity = Decimal(0.0)

    return  invoice_amount_owned_to_entity - payment_amount_owned_to_entity 


def compute_total_invoice_amount_charged_on_debit(account_pk, debit_pk, reference_date = datetime.datetime.today()):
    account = Account.objects.get(pk = account_pk)
    account_debits = Debit.objects.filter(pk=debit_pk).filter(debit_date__lte = reference_date)
    invoice_queryset = RequestForPaymentOrInvoice.objects.filter(debit__in = list(account_debits)).filter(invoice_date__lte = reference_date)
    debit_invoices__total_amount = RequestForPaymentOrInvoice.objects.filter(debit__in = list(account_debits)).filter(invoice_date__lte = reference_date).aggregate(Sum('invoice_charge_amount'))['invoice_charge_amount__sum']
    debit_invoices_with_canceled_payments__total_amount = Payment.objects.filter(invoice__in = list(invoice_queryset)).filter(payment_type_choice__in =['ΑΚΥΡΩΣΗ','ΑΠΟΡΡΙΨΗ']).aggregate(Sum('payment_amount'))['payment_amount__sum']
    if debit_invoices__total_amount is None:
        debit_invoices__total_amount = Decimal(0.0)
    if debit_invoices_with_canceled_payments__total_amount is None:
        debit_invoices_with_canceled_payments__total_amount = Decimal(0.0)
    total_invoice = debit_invoices__total_amount - debit_invoices_with_canceled_payments__total_amount
    return  total_invoice


def compute_total_payment_amount(account_pk, reference_date = datetime.datetime.today()):
    account = Account.objects.get(pk = account_pk)
    account_debits = Debit.objects.filter(account=account).filter(debit_date__lte = reference_date)
    #invoice_list = [i.invoice_charge_amount for d in account_debits for i in list(RequestForPaymentOrInvoice.objects.filter(debit = d.pk))]
    invoice_queryset = RequestForPaymentOrInvoice.objects.filter(debit__in = list(account_debits)).filter(invoice_date__lte = reference_date)
    payments__non_canceled = Payment.objects.filter(invoice__in = list(invoice_queryset)).exclude(payment_type_choice__in =['ΑΚΥΡΩΣΗ','ΑΠΟΡΡΙΨΗ']).aggregate(Sum('payment_amount'))['payment_amount__sum']
    if payments__non_canceled is None:
        payments__non_canceled = Decimal(0.0)
    return  payments__non_canceled #payments


def compute_total_90days_delayed_payment_to_third_parties_list(account_pk, reference_date = datetime.datetime.today()):
    account = Account.objects.get(pk = account_pk)
    account_debits = Debit.objects.filter(account=account).filter(debit_date__lte = reference_date)
    #invoice_list = [i.invoice_charge_amount for d in account_debits for i in list(RequestForPaymentOrInvoice.objects.filter(debit = d.pk))]
    invoice_queryset = RequestForPaymentOrInvoice.objects.filter(debit__in = list(account_debits)).filter(invoice_date__lte = reference_date)
    delayed_payments_to_third_parties__non_canceled = Payment.objects.filter(invoice__in = list(invoice_queryset)).exclude(payment_type_choice__in =['ΑΚΥΡΩΣΗ','ΑΠΟΡΡΙΨΗ']).aggregate(Sum('payment_amount_to_third_persons'))['payment_amount_to_third_persons__sum']
    
    if delayed_payments_to_third_parties__non_canceled is None:
        delayed_payments_to_third_parties__non_canceled = Decimal(0.0)
    return  delayed_payments_to_third_parties__non_canceled #payments


def compute_90days_delayed_setoff_payment_to_third_parties_list(account_pk, reference_date = datetime.datetime.today()):
    account = Account.objects.get(pk = account_pk)
    account_debits = Debit.objects.filter(account=account).filter(debit_date__lte = reference_date)
    #invoice_list = [i.invoice_charge_amount for d in account_debits for i in list(RequestForPaymentOrInvoice.objects.filter(debit = d.pk))]
    invoice_queryset = RequestForPaymentOrInvoice.objects.filter(debit__in = list(account_debits)).filter(invoice_date__lte = reference_date)
    delayed_setoff_payments_to_third_parties__non_canceled = Payment.objects.filter(invoice__in = list(invoice_queryset)).exclude(payment_type_choice__in =['ΑΚΥΡΩΣΗ','ΑΠΟΡΡΙΨΗ']).aggregate(Sum('setoff_payment_amount'))['setoff_payment_amount__sum']
    
    if delayed_setoff_payments_to_third_parties__non_canceled is None:
        delayed_setoff_payments_to_third_parties__non_canceled = Decimal(0.0)
    return  delayed_setoff_payments_to_third_parties__non_canceled #payments


def compute_report_data(register_pk, reference_date = datetime.datetime.today()):
    accounts = Account.objects.filter(expenditure_register = register_pk)
    # balance_list = [get_account_balance(account.pk) for account in accounts]
    initial_credit_list = [compute_initial_credit(account.pk, reference_date) for account in accounts]
    # print(type(initial_credit_list[0]))
    reformed_credit_list = [compute_reformed_credit(account.pk, reference_date) for account in accounts]
    print(reformed_credit_list)
    # print(type(reformed_credit_list[0]))
    total_credit_list = [i_c + r_c for i_c, r_c in zip(initial_credit_list, reformed_credit_list)]
    disposed_percentage_list = [compute_disposed_percentage(account.pk, reference_date) for account in accounts]
    total_debit_list = [compute_total_debit(account.pk, reference_date) for account in accounts]
    total_residual_credit_list = [c*p/Decimal(100.0) - d for c, p, d in zip(total_credit_list, disposed_percentage_list, total_debit_list)] 
    total_recall_list = [compute_total_recall(account.pk, reference_date) for account in accounts]
    total_invoice_list = [compute_total_invoice_amount(account.pk, reference_date) for account in accounts]
    total_payment_list = [compute_total_payment_amount(account.pk, reference_date) for account in accounts]
    total_90days_delayed_payment_to_third_parties_list = [compute_total_90days_delayed_payment_to_third_parties_list(account.pk) for account in accounts]
    total_90days_delayed_setoff_payment_to_third_parties_list = [compute_90days_delayed_setoff_payment_to_third_parties_list(account.pk) for account in accounts]
    total_pending_debits_list = [d - p for d, p in zip(total_debit_list, total_payment_list)]
    # total_amount_to_recall = [c - i - r for c, i, r in zip(total_credit_list, total_invoice_list, total_recall_list)] 
    total_prepaid_invoice_list = [compute_total_prepaid_invoice_amount(account.pk, reference_date) for account in accounts]
    total_pending_payments_list = [i - p - prepaid_i for i, p, prepaid_i in zip(total_invoice_list, total_payment_list, total_prepaid_invoice_list)]
    
    duration_low_bound = timedelta(days=1)
    duration_upper_bound = timedelta(days=365)
    invoice_amount_owned_to_general_goverment_list = [compute_total_invoice_amount_owned_to_entity_within_time_frame(account.pk,'ΓΕΝΙΚΗ ΚΥΒΕΡΝΗΣΗ', reference_date, duration_low_bound, duration_upper_bound) for account in accounts]
    total_invoice_amount_owned_to_third_parties_list = [compute_total_invoice_amount_owned_to_entity_within_time_frame(account.pk, 'ΤΡΙΤΟΥΣ', reference_date, duration_low_bound, duration_upper_bound) for account in accounts]
    
    duration_low_bound = timedelta(days=1)
    duration_upper_bound = timedelta(days=30)
    owned_to_goverment_1_to_30_days = [compute_total_invoice_amount_owned_to_entity_within_time_frame(account.pk,'ΓΕΝΙΚΗ ΚΥΒΕΡΝΗΣΗ', reference_date, duration_low_bound, duration_upper_bound) for account in accounts]
    owned_to_third_party_1_to_30_days = [compute_total_invoice_amount_owned_to_entity_within_time_frame(account.pk, 'ΤΡΙΤΟΥΣ', reference_date, duration_low_bound, duration_upper_bound) for account in accounts]

    duration_low_bound = timedelta(days=31)
    duration_upper_bound = timedelta(days=60)
    owned_to_goverment_31_to_60_days = [compute_total_invoice_amount_owned_to_entity_within_time_frame(account.pk,'ΓΕΝΙΚΗ ΚΥΒΕΡΝΗΣΗ', reference_date, duration_low_bound, duration_upper_bound) for account in accounts]
    owned_to_third_party_31_to_60_days = [compute_total_invoice_amount_owned_to_entity_within_time_frame(account.pk, 'ΤΡΙΤΟΥΣ', reference_date, duration_low_bound, duration_upper_bound) for account in accounts]

    duration_low_bound = timedelta(days=61)
    duration_upper_bound = timedelta(days=90)
    owned_to_goverment_61_to_90_days = [compute_total_invoice_amount_owned_to_entity_within_time_frame(account.pk,'ΓΕΝΙΚΗ ΚΥΒΕΡΝΗΣΗ', reference_date, duration_low_bound, duration_upper_bound) for account in accounts]
    owned_to_third_party_61_to_90_days = [compute_total_invoice_amount_owned_to_entity_within_time_frame(account.pk, 'ΤΡΙΤΟΥΣ', reference_date, duration_low_bound, duration_upper_bound) for account in accounts]

    duration_low_bound = timedelta(days=91)
    duration_upper_bound = timedelta(days=365)
    owned_to_goverment_91_to_end_days = [compute_total_invoice_amount_owned_to_entity_within_time_frame(account.pk,'ΓΕΝΙΚΗ ΚΥΒΕΡΝΗΣΗ', reference_date, duration_low_bound, duration_upper_bound) for account in accounts]
    owned_to_third_party_91_to_end_days = [compute_total_invoice_amount_owned_to_entity_within_time_frame(account.pk, 'ΤΡΙΤΟΥΣ', reference_date, duration_low_bound, duration_upper_bound) for account in accounts]

    duration_low_bound = timedelta(days=91)
    duration_upper_bound = timedelta(days=365)
    owned_to_third_party_from_abroad_91_to_end_days = [compute_total_invoice_amount_owned_to_creditors_from_abroad(account.pk, 'ΤΡΙΤΟΥΣ', reference_date, duration_low_bound, duration_upper_bound) for account in accounts]

    #return initial_credit_list, reformed_credit_list, total_credit_list, disposed_percentage_list, total_debit_list, total_residual_credit_list, total_invoice_list, total_payment_list, total_90days_delayed_payment_to_third_parties_list, total_90days_delayed_setoff_payment_to_third_parties_list, total_pending_debits_list, total_pending_payments_list, invoice_amount_owned_to_general_goverment_list, total_invoice_amount_owned_to_third_parties_list, owned_to_goverment_1_to_30_days, owned_to_third_party_1_to_30_days, owned_to_goverment_31_to_60_days, owned_to_third_party_31_to_60_days, owned_to_goverment_61_to_90_days, owned_to_third_party_61_to_90_days, owned_to_goverment_91_to_end_days, owned_to_third_party_91_to_end_days, owned_to_third_party_from_abroad_91_to_end_days
    return zip(list(accounts), initial_credit_list, reformed_credit_list, total_credit_list, disposed_percentage_list, total_debit_list, total_residual_credit_list, total_invoice_list, total_payment_list, total_90days_delayed_payment_to_third_parties_list, total_90days_delayed_setoff_payment_to_third_parties_list, total_pending_debits_list, total_pending_payments_list, invoice_amount_owned_to_general_goverment_list, total_invoice_amount_owned_to_third_parties_list, owned_to_goverment_1_to_30_days, owned_to_third_party_1_to_30_days, owned_to_goverment_31_to_60_days, owned_to_third_party_31_to_60_days, owned_to_goverment_61_to_90_days, owned_to_third_party_61_to_90_days, owned_to_goverment_91_to_end_days, owned_to_third_party_91_to_end_days, owned_to_third_party_from_abroad_91_to_end_days)