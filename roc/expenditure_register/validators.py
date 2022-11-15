from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from .input_validation_definitions import *
import datetime

def validate_afm(afm):
    is_valid = _validate_afm(afm)
    if not is_valid:
        raise ValidationError(_('%(afm)s δεν είναι έγκυρο!'), params={'afm': afm}, )

def _validate_afm(afm):
    is_valid = False

    if len(afm) == 9 and afm.isdigit():
        chcknumbers = [0, 2, 4, 8, 16, 32, 64, 128, 256]
        lchcknumbers = len(chcknumbers) - 1
        sum = 0
        for i in range(9):
            sum += (int(afm[i]) * chcknumbers[lchcknumbers - i])
        ch_digit = int(afm[8])
        ypoloipo = sum % 11

        if ypoloipo == 10:
            ypoloipo = 0

        if (ypoloipo == ch_digit):
            is_valid = True
    
    return is_valid

# def validate_school_year(school_year):
#     is_valid = False
#     if (school_year, school_year) in SCHOOL_YEAR_CHOICES:
#         is_valid = True
#     return is_valid

# def validate_surname(surname):
#     is_valid = False
#     if isinstance(surname, str)  and len(surname) <= 100:
#         is_valid = True

#     return is_valid

# def validate_name(name):
#     is_valid = False
#     if isinstance(name, str) and len(name) <= 100:
#         is_valid = True
#     return is_valid

# def validate_patronym(patronym):
#     is_valid = False
#     if isinstance(patronym, str) and len(patronym) <= 100:
#         is_valid = True
#     return is_valid

# def validate_teaching_specialty(teaching_specialty):
#     is_valid = False
#     if (teaching_specialty, teaching_specialty) in TEACHING_SPECIALTY_CHOICES:
#         is_valid = True
#     return is_valid

# def validate_teaching_specialty_verbose_name(teaching_specialty_verbose_name):
#     is_valid = False
#     if (teaching_specialty_verbose_name, teaching_specialty_verbose_name) in TEACHING_SPECIALTY_VERBOSE_NAME:
#         is_valid = True
#     return is_valid

# def validate_funding_program(funding_program):
#     is_valid = False
#     if (funding_program, funding_program)  in FUNDING_PROGRAM:
#         is_valid = True
#     return is_valid
    
# def validate_ministerial_hiring_decision(ministerial_hiring_decision):
#     is_valid = False
#     if isinstance(ministerial_hiring_decision, str) and len(ministerial_hiring_decision) <= 100:
#         is_valid = True
#     return is_valid

# def validate_ada_ministerial_hiring_decision(ada_ministerial_hiring_decision):
#     is_valid = False
#     if isinstance(ada_ministerial_hiring_decision, str) and len(ada_ministerial_hiring_decision) <= 100:
#         is_valid = True
#     return is_valid

# def validate_type_of_contract(type_of_contract):
#     is_valid = False
#     if (type_of_contract, type_of_contract)  in CONTRACT_TYPE_CHOICES:
#         is_valid = True
#     return is_valid

# def validate_nominal_first_appearance_date(nominal_first_appearance_date):
#     is_valid = False
#     if isinstance(nominal_first_appearance_date, datetime.datetime):
#         is_valid = True
#     return is_valid

# def validate_nominal_last_appearance_date(nominal_last_appearance_date):
#     is_valid = False
#     if isinstance(nominal_last_appearance_date, datetime.datetime):
#         is_valid = True
#     return is_valid

# def validate_service_undertake_date(service_undertake_date):
#     is_valid = False
#     if isinstance(service_undertake_date, datetime.datetime):
#         is_valid = True
#     return is_valid

# def validate_decision_of_dismissal(decision_of_dismissal):
#     is_valid = False
#     if isinstance(decision_of_dismissal, str) and len(decision_of_dismissal) <= 100:
#         is_valid = True
#     return is_valid


# def validate_date_of_dismissal(date_of_dismissal):
#     is_valid = False
#     if isinstance(date_of_dismissal, datetime.datetime):
#         is_valid = True
#     return is_valid

# def validate_cause_of_dismissal(cause_of_dismissal):
#     is_valid = False
#     if (cause_of_dismissal, cause_of_dismissal)  in CAUSE_OF_DISMISSAL:
#         is_valid = True
#     return is_valid


# def validate_nominal_hours_per_week(nominal_hours_per_week):
#     is_valid = False
#     if (int(nominal_hours_per_week), int(nominal_hours_per_week))  in NOMINAL_HOURS_PER_WEEK:
#         is_valid = True
#     return is_valid

# def validate_hours_per_week(hours_per_week):
#     is_valid = False
#     if (int(hours_per_week), int(hours_per_week)) in NOMINAL_HOURS_PER_WEEK:
#         is_valid = True
#     return is_valid   

# def validate_educational_service_type(educational_service_type):
#     is_valid = False
#     if (educational_service_type, educational_service_type)  in EDUCATIONAL_SERVICE_TYPE:
#         is_valid = True
#     return is_valid   

# def validate_excess_leave_days(excess_leave_days):
#     is_valid = False
#     if excess_leave_days.isdigit():
#         is_valid = True
#     return is_valid

# def validate_professor_contract_entry(professor_contract):
#     is_valid_school_year = validate_school_year(professor_contract.school_year)
#     is_valid_afm = _validate_afm(professor_contract.afm)
#     is_valid_surname = validate_surname(professor_contract.surname)
#     is_valid_name = validate_name(professor_contract.name)
#     is_valid_patronym = validate_patronym(professor_contract.patronym)
#     is_valid_teaching_specialty = validate_teaching_specialty(professor_contract.teaching_specialty)
#     is_valid_teaching_specialty_verbose_name = validate_teaching_specialty_verbose_name(professor_contract.teaching_specialty_verbose_name)
#     is_valid_funding_program = validate_funding_program(professor_contract.funding_program)
#     is_valid_ministerial_hiring_decision = validate_ministerial_hiring_decision(professor_contract.ministerial_hiring_decision)
#     is_valid_ada_ministerial_hiring_decision = validate_ada_ministerial_hiring_decision(professor_contract.ada_ministerial_hiring_decision)
#     is_valid_type_of_contract = validate_type_of_contract(professor_contract.type_of_contract)
#     is_valid_nominal_first_appearance_date = validate_nominal_first_appearance_date(professor_contract.nominal_first_appearance_date)
#     # is_valid_nominal_last_appearance_date = validate_nominal_last_appearance_date(professor_contract.nominal_last_appearance_date)
#     is_valid_service_undertake_date = validate_service_undertake_date(professor_contract.service_undertake_date)
#     is_valid_decision_of_dismissal = validate_decision_of_dismissal(professor_contract.decision_of_dismissal)
#     is_valid_date_of_dismissal = validate_date_of_dismissal(professor_contract.date_of_dismissal)
#     is_valid_cause_of_dismissal = validate_cause_of_dismissal(professor_contract.cause_of_dismissal)
#     is_valid_nominal_hours_per_week = validate_nominal_hours_per_week(professor_contract.nominal_hours_per_week)
#     is_valid_hours_per_week = validate_hours_per_week(professor_contract.hours_per_week)
#     is_valid_educational_service_type = validate_educational_service_type(professor_contract.educational_service_type)
#     is_valid_excess_leave_days = validate_excess_leave_days(professor_contract.excess_leave_days)        

#     is_valid = (is_valid_school_year and
#                 is_valid_afm and 
#                 is_valid_surname and 
#                 is_valid_name and 
#                 is_valid_patronym and 
#                 is_valid_teaching_specialty and 
#                 is_valid_teaching_specialty_verbose_name and 
#                 is_valid_funding_program and 
#                 is_valid_ministerial_hiring_decision and 
#                 is_valid_ada_ministerial_hiring_decision and 
#                 is_valid_type_of_contract and 
#                 is_valid_nominal_first_appearance_date and 
#                 # is_valid_nominal_last_appearance_date and 
#                 is_valid_service_undertake_date and 
#                 is_valid_decision_of_dismissal and 
#                 is_valid_date_of_dismissal and
#                 is_valid_cause_of_dismissal and 
#                 is_valid_nominal_hours_per_week and 
#                 is_valid_hours_per_week and 
#                 is_valid_educational_service_type and 
#                 is_valid_excess_leave_days)
    
#     validation_tuple = (is_valid_school_year,
#                 is_valid_afm,  
#                 is_valid_surname,  
#                 is_valid_name,  
#                 is_valid_patronym,  
#                 is_valid_teaching_specialty,  
#                 is_valid_teaching_specialty_verbose_name,  
#                 is_valid_funding_program,  
#                 is_valid_ministerial_hiring_decision,  
#                 is_valid_ada_ministerial_hiring_decision,  
#                 is_valid_type_of_contract,  
#                 is_valid_nominal_first_appearance_date,  
#                 # is_valid_nominal_last_appearance_date,  
#                 is_valid_service_undertake_date,  
#                 is_valid_decision_of_dismissal,  
#                 is_valid_date_of_dismissal, 
#                 is_valid_cause_of_dismissal,  
#                 is_valid_nominal_hours_per_week,  
#                 is_valid_hours_per_week,  
#                 is_valid_educational_service_type,  
#                 is_valid_excess_leave_days)

#     # print(f'Validating entry: {professor_contract} Result: {is_valid} Individual Validators: {validation_tuple}')
#     # print(f'Result: {is_valid} Individual Validators: {validation_tuple}')
#     return is_valid, validation_tuple
