# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 21:02:37 2021

@author: Admin
"""



import os
import pandas as pd


coupon = 0.07


def pricer(spotRates):
    pv_list=[]
    a =  coupon*100/(1+spotRates[0]/100)
    b =coupon*100/(1+spotRates[1]/100)**2 
    c =coupon*100/(1+spotRates[2]/100)**3
    d =coupon*100/(1+spotRates[3]/100)**4 
    e =(coupon*100+100)/(1+spotRates[4]/100)**5
    
    pv_list=[a,b,c,d,e]
    
    return sum(pv_list)



initial_spotRates = [7.59, 7.305,7.24,7.21,7.22]
initial_price = pricer(initial_spotRates)


os.chdir(r'E:\Work')
spotdata= pd.read_excel('Spot_rates_hist_data1y.xlsx',index_col=('date'))

spotdata.sort_index(inplace=True)

spotdata_ts=spotdata.diff().dropna()
base_move = spotdata_ts.copy()
base_move['1y_spot']=initial_spotRates[0]
base_move['2y_spot']=initial_spotRates[1]
base_move['3y_spot']=initial_spotRates[2]
base_move['4y_spot']=initial_spotRates[3]
base_move['5y_spot']=initial_spotRates[4]

base_move['1y_final']= base_move['1Y']+base_move['1y_spot']
base_move['2y_final']= base_move['2Y']+base_move['2y_spot']
base_move['3y_final']= base_move['3Y']+base_move['3y_spot']
base_move['4y_final']= base_move['4Y']+base_move['4y_spot']
base_move['5y_final']= base_move['5Y']+base_move['5y_spot']

base_move.sort_index(ascending=False,inplace=True)


pv_final=[]

for i in range(0,len(base_move)):
    spotlist_ = base_move.iloc[i:i+1, 10:15]
    spotlist =spotlist_.values.flatten().tolist()
    pv = pricer(spotlist)
    pv_final.append(pv)
    

pv_df = pd.DataFrame(pv_final,columns=['PV'])
pv_df['PNL']= pv_df['PV']-initial_price

fullreval_90=pv_df['PNL'].quantile(0.10)
fullreval_95=pv_df['PNL'].quantile(0.05)
fullreval_99=pv_df['PNL'].quantile(0.01)


