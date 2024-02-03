# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:53:54 2023

@author: Mounika
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pmdarima import auto_arima
from matplotlib.ticker import FixedFormatter
data = pd.read_csv("C:\\Users\\Eswar\\Documents\\Latha\\sprin2023\\assignments\\AIT580\\FInalprojec\\Final\\Influenza_Surveillance_Weekly.csv")
data.columns = data.columns.str.lower()
data.head()
data.isna().sum()
data["week_start"] = pd.to_datetime(data["week_start"])
data["week_end"] = pd.to_datetime(data["week_end"])
#data.set_index(data["week_start"], inplace = True)
#data = data.asfreq('W')
data.columns

data.dtypes
data.head()
df = data[["week_start","week_end", "hosp_flu_icu_weekly","flu_risk_level", "influenza_season",
      "lab_flu_tested","lab_flu_positive","lab_flu_pct_positive", "lab_tot_a_positive",
      "lab_tot_b_positive", "lab_tot_h1n1_positive", "lab_tot_h3n2_positive", "hosp_flu_icu_cumulative"]]
df.head()
df["week_start"] = pd.to_datetime(df["week_start"])
df["year"] = df["week_start"].dt.year
df.columns
df['week_cumulative'] = df['hosp_flu_icu_weekly'].cumsum()
df["week_start"] = pd.to_datetime(df["week_start"])
df.set_index(df["week_start"], inplace = True)
df.drop('week_start', axis=1, inplace=True)
df.head()
df = df.asfreq('W')
df['icu_cumulative_weekly'] = df['hosp_flu_icu_weekly'].cumsum()
df2 = df["icu_cumulative_weekly"]
df2 = df2.asfreq('W')
df2
df2.bfill(inplace=True)
decomposition = sm.tsa.seasonal_decompose(df2, model= "additive")
trend = decomposition.trend
seasonal = decomposition.seasonal
residual =decomposition.resid

# Visualize decomposition components
trend.plot(figsize=(10, 4), title='Trend Component')
plt.show()
seasonal.plot(figsize=(10, 4), title='Seasonal Component')
plt.show()
residual.plot(figsize=(10, 4), title='Residual Component')
plt.show()
model = auto_arima(df2, start_p= 0, max_p=10, max_d=2, start_q=0, max_q=10,seasonal=False,
                    trace =True, enforce_stationarity =False, enforce_invertibility =False,
                    error_action ="ignore", suppress_warnings =True,
                    stepwise =True)
model.summary()
results = model.fit(df2)
forecast,conf_int = results.predict(30,return_conf_int=True,alpha=0.05)
print(type(forecast), type(conf_int))
type(forecast)
fcast = pd.DataFrame()
fcast["forecast"] = forecast
fcast.index
con_df = pd.DataFrame(conf_int, columns=("low", "high"))
con_df.set_index(fcast.index, inplace = True)
result = pd.concat([fcast,con_df], axis=1)
import matplotlib
def plot_forecast(dataframe):
    plt.figure(figsize=(10,7))
    plt.plot(dataframe["forecast"], "-", color = "#1f77b4", label = "forecast")
    plt.plot(dataframe["low"],color ="grey", linewidth =0.5,label = "_")
    plt.plot(dataframe["high"],color ="grey", linewidth =0.5,label = "_")
    lower_bound = dataframe["low"]
    upper_bound =dataframe["high"]
    plt.fill_between(dataframe.index, lower_bound, upper_bound, facecolor='grey', alpha=0.5,
                label="95% confidence interval")
    plt.plot(df2, color = "red", label= 'Actual data')
    plt.title(df2,  fontsize = 12, fontweight ="bold")
    plt.legend(loc ="upper left", fontsize = 17)
    plt.xticks( fontsize = 12,fontweight ="bold",rotation = 35)
    plt.yticks( fontsize = 12,fontweight ="bold")
    xx, locs = plt.yticks()
    ll = ['%.0f' % a for a in xx]
    plt.gca().yaxis.set_major_formatter(FixedFormatter(ll))
    plt.gca().yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
    return plt.show()
plot_forecast(result)