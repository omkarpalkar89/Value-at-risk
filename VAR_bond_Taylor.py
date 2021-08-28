# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 12:28:10 2021

@author: Admin
"""
import os
import pandas as pd
import numpy as np



initial_spotRates = [7.59, 7.305,7.24,7.21,7.22]
coupon = 0.07


def pvcalc(spotRates):
    pv_list=[]
    a =  coupon*100/(1+spotRates[0]/100)
    b =coupon*100/(1+spotRates[1]/100)**2 
    c =coupon*100/(1+spotRates[2]/100)**3
    d =coupon*100/(1+spotRates[3]/100)**4 
    e =(coupon*100+100)/(1+spotRates[4]/100)**5
    
    pv_list=[a,b,c,d,e]
    
    return pv_list


pv_base = pvcalc(initial_spotRates)
pv_base = np.array(pv_base)


spot_01bp = [x + 0.01 for x in initial_spotRates]
pv_1bp = pvcalc(spot_01bp)
pv_1bp = np.array(pv_1bp)



spot_minus01bp = [x - 0.01 for x in initial_spotRates]
pv_minus1bp = pvcalc(spot_minus01bp)
pv_minus1bp = np.array(pv_minus1bp)


spot_02bp = [x + 0.02 for x in initial_spotRates]
pv_2bp = pvcalc(spot_02bp)
pv_2bp = np.array(pv_2bp)


spot_minus02bp = [x - 0.02 for x in initial_spotRates]
pv_minus2bp = pvcalc(spot_minus02bp)
pv_minus2bp = np.array(pv_minus2bp)


PV01 = pv_base - pv_1bp
PV01_1bp =  pv_1bp - pv_2bp
PV01_minus1bp =   pv_minus2bp - pv_minus1bp

convexity_1bp = PV01 - PV01_1bp
convexity_minus1bp =  PV01_minus1bp - PV01

avg_convexity = 0.5*(convexity_1bp+convexity_minus1bp)


os.chdir(r'E:\Work')
spotdata= pd.read_excel('Spot_rates_hist_data1y.xlsx',index_col=('date'))

spotdata.sort_index(inplace=True)

spotdata_ts=spotdata.diff().dropna()

base_move = spotdata_ts.copy()
base_move.sort_index(ascending=False,inplace=True)


base_move['PV01pnl_1y'] =  PV01[0]*base_move['1Y']*(-100)
base_move['PV01pnl_2y'] =  PV01[1]*base_move['2Y']*(-100)
base_move['PV01pnl_3y'] =  PV01[2]*base_move['3Y']*(-100)
base_move['PV01pnl_4y'] =  PV01[3]*base_move['4Y']*(-100)
base_move['PV01pnl_5y'] =  PV01[4]*base_move['5Y']*(-100)

base_move['PV01_pnl'] = base_move['PV01pnl_1y']+base_move['PV01pnl_2y']+\
                        base_move['PV01pnl_3y']+base_move['PV01pnl_4y']+base_move['PV01pnl_5y']
                        

base_move['convexitypnl_1y'] = 0.5*avg_convexity[0]*(base_move['1Y']**2)*10000
base_move['convexitypnl_2y'] = 0.5*avg_convexity[1]*(base_move['2Y']**2)*10000
base_move['convexitypnl_3y'] = 0.5*avg_convexity[2]*(base_move['3Y']**2)*10000
base_move['convexitypnl_4y'] = 0.5*avg_convexity[3]*(base_move['4Y']**2)*10000
base_move['convexitypnl_5y'] = 0.5*avg_convexity[4]*(base_move['5Y']**2)*10000

base_move['convexitypnl'] = base_move['convexitypnl_1y']+base_move['convexitypnl_2y']+\
                        base_move['convexitypnl_3y'] + base_move['convexitypnl_4y']+base_move['convexitypnl_5y']

base_move['Total_pnl'] = base_move['PV01_pnl'] + base_move['convexitypnl']

partialreval_90=base_move['Total_pnl'].quantile(0.10)
partialreval_95=base_move['Total_pnl'].quantile(0.05)
partialreval_99=base_move['Total_pnl'].quantile(0.01)                            