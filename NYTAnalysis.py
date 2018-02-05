import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from Workspace import *

# wcVdate=load_obj('wcVdate')
# fullDict=load_obj('WC_DATE_NAME_PAGE')

def get_year(NYT_date):
    try:
        return int(NYT_date[0:4])
    except TypeError:
        return 0

def get_month(NYT_date):
    try:
        return int(NYT_date[5:7])
    except TypeError:
        return 0

def get_day(NYT_date):
    try:
        return int(NYT_date[8:10])
    except TypeError:
        return 0

def date_to_days(NYT_date):
    YEAR=get_year(NYT_date)
    MONTH=get_month(NYT_date)
    DAY=get_day(NYT_date)
    return YEAR*365+(MONTH-1)*30+DAY

def grab_idx_of_date(DATES,DAY,MONTH):
    idxs=[]
    for idx in xrange(0,len(DATES)):
        if (get_month(DATES[idx])==MONTH) & (get_day(DATES[idx])==DAY):
            idxs.append(idx)
    return idxs

def grab_idx_of_year(DATES,YEAR):
    idxs=[]
    for idx in xrange(0,len(DATES)):
        if (get_year(DATES[idx])==YEAR):
            idxs.append(idx)
    return idxs

def avg_wc_by_year(DATES,WCS,Y0=1853,Y1=2018):
    years=range(Y0,Y1)
    average=[]
    WCS=np.array(WCS,dtype=np.float)
    for year in years:
        year_idxs=grab_idx_of_year(DATES,year)
        average.append(np.nanmean(WCS[year_idxs]))
    return (years,average)

def std_wc_by_year(DATES,WCS,Y0=1853,Y1=2018):
    years=range(Y0,Y1)
    average=[]
    # WCS=np.array(WCS,dtype=np.float)
    for year in years:
        year_idxs=grab_idx_of_year(DATES,year)
        average.append(np.nanstd(WCS[year_idxs]))
    return (years,average)

# def clean_nones(alist):
#     newlist=[]
#     for el in alist:
#         if el is not None:
#             newlist.append(el)
#     return newlist
#
# def clean_nones_dict(adict):
#     keys=
#     newlist=[]
#     for el in alist:
#         if el is not None:
#             newlist.append(el)
#     return newlist
