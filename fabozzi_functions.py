#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 12:14:38 2019

@author: konstantinos.falangi
"""

import numpy as np
import pandas as pd
import datetime
from datetime import timedelta
from dateutil import relativedelta
from dateutil.rrule import * 
from dateutil.parser import *




def is_business_day(date):
    """Function to test if a date is a business day """
    return bool(len(pd.bdate_range(date, date)))


def loan_payment(LB=200000, i=7.5, n=30):
    """Function to calculate monthly loan payment for a loan
    with original balance LB, interest rate i and duration 
    n years. """
    
    #adjust rate to monthly
    monthly_rate = (i * 0.01) / 12
    
    #terms in number of months
    dur = n * 12
    
    #calculate the discount factor
    discount_factor = ((1 + monthly_rate) ** dur) - 1
    
    #get loan payment
    LP = LB * ((monthly_rate * (1 + monthly_rate) ** dur) / discount_factor)
    return(LP)


def remaining_balance(LB=200000, i=7.5, n=30, t=12):
    """Function to calculate remaining balance at the end
    of month t, for a loan with original balance LB, 
    interest rate i and duration n years. """
    
    #adjust rate to monthly
    monthly_rate = (i * 0.01) / 12
    
    #terms in number of months
    dur = n * 12
    
    #calculate the discount factor
    discount_factor = ((1 + monthly_rate) ** dur) - 1
    
    #find remaining balance
    LB_t = LB * (((1 + monthly_rate) ** dur - (1 + monthly_rate)**t) / discount_factor)
    return(LB_t)


def scheduled_principal(LB=200000, i=7.5, n=30, t=12):
    """Function to calculate the scheduled principal for month
    t, of a loan with original balance LB, annual interest rate i
    and duration n years. """
    
    #adjust rate to monthly
    monthly_rate = (i * 0.01) / 12
    
    #terms in number of months
    dur = n * 12
    
    #calculate the discount factor
    discount_factor = ((1 + monthly_rate) ** dur) - 1
    
    #find scheduled principal
    SP_t = LB * ((monthly_rate * ((1 + monthly_rate) ** (t - 1)))) / discount_factor
    return(SP_t)
    


def amortisation_schedule(LB=200000, i=7.5, n=30, t=12, pay_date = '2019-02-01', 
                          closing_date = datetime.date.today()):
    """Function that produces the amortisation schedule for a loan 
    with original balance LB, interest rate i, and duration of n years.
    Pay date refers to the monthly due date and closing date is the date the loan
    was originated. If closing date is different to the first pay date then
    first installment incldues the extra interest. """
    
    #calculate the monthly installment
    loan_installment = round(loan_payment(LB, i, n), 2)
    
    #create a list with the balance due
    beginning_balance = []
    for k in np.arange(n * 12):
        LB_t = remaining_balance(LB, i, n, t=k)
        beginning_balance.append(LB_t) 
    
    #create a list with the scheduled principal
    principal_repayment = []
    for k in np.arange(1, (n * 12) + 1):
        LB_t = scheduled_principal(LB, i, n, t=k)
        principal_repayment.append(LB_t) 
    
    #create a list with the monthly interest amount
    interest_amount = []
    for k in np.arange(n * 12):
        i_t = beginning_balance[k] * ((i * 0.01) / 12)
        interest_amount.append(i_t)
    
    #create a list with ending balance
    ending_balance = []
    for s in np.arange(n * 12):
        EB_t = np.array(beginning_balance[s]) - np.array(principal_repayment[s])
        ending_balance.append(EB_t)
    
    #create a series of due dates
    pay_dates = []
    for l in np.arange(1,361):
        nextmonth = datetime.date.today() + relativedelta.relativedelta(months=l)
        if is_business_day(nextmonth):
            nextmonth = nextmonth
        elif is_business_day(nextmonth + timedelta(days=1)):
            nextmonth = nextmonth + timedelta(days=1)
        else:
            nextmonth = nextmonth + timedelta(days=2)
        pay_dates.append(str(nextmonth))
        
    #create list with the monthly payments
    due_payments = []
    for f in np.arange(1,361):
        due_payments.append(loan_installment)
    
    #adjust interest amount if closing date is different to first due date
    if pay_date != closing_date:
        end_of_month = list(rrule(MONTHLY, bymonthday=-1, count=1, dtstart=(closing_date)))
        delta =  end_of_month[0].date() - closing_date
        interest_t0 = LB * (i * 0.01) * (delta.days) / 365
        interest_amount[0] += interest_t0
        due_payments[0] = interest_t0 + loan_installment
    
    
    #create amortisation table
    amortisation_schedule = pd.DataFrame({'Beginning Balance': beginning_balance,
                                          'Interest': interest_amount,
                                          'Principal Payment': principal_repayment,
                                          'Ending Balance': ending_balance, 
                                          'Due Payment': due_payments}, index = pay_dates)
    
    amortisation_schedule.index.name = 'Due Date'
    
    print('The monthly payment for a loan with original balance of ' + str(LB) + ', an interest rate of ' + 
          str(i) + '%' + ' and duration of ' + str(n) + ' years is: ' + str(loan_installment))
    print()
    return(amortisation_schedule)





    
    
    