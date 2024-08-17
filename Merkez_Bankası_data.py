import streamlit as st
import pandas as pd 
import numpy as np 
from evds import evdsAPI
import altair as alt
import matplotlib.pyplot as plt
import plotly.graph_objects as go

#API ayarlanması
evds = evdsAPI("W80RoZnn8U")

#Ana kategorileri çekilmesi
main_categories_df = evds.main_categories



st.title("EVDS PROJECT")


try:
    #ana kategorideki başlıklardan birinin kullanı tarafından seçilmesi
    selected_main_title = st.selectbox("Konu başlığını seçin", main_categories_df.iloc[:,1], index= None)
    
    if selected_main_title:
        #category_id değeri seçilen konu başlığınıa göre alınır.
        category_id = main_categories_df.loc[main_categories_df["TOPIC_TITLE_TR"] == selected_main_title, "CATEGORY_ID"].values[0]
        category_id = int(category_id)
    
        #category_id değeri ile sub categori değerleri belirlenir.
        sub_category_df = evds.get_sub_categories(category_id)
        #sub category değeri kullanıcıya seçtirtilir.
        selected_sub_category = st.selectbox("Konu başlığını seçin", sub_category_df.iloc[:,2],index=None)
    
        if selected_sub_category:
            #Seçilen sub category değeri ile group code belirlenir
            selected_group_code = sub_category_df.loc[sub_category_df["DATAGROUP_NAME"] == selected_sub_category, "DATAGROUP_CODE"].values[0]
            #Belirlenen group code değeri ile series değerleri belirlenir.
            series_values_df = evds.get_series(selected_group_code)
            #Belirlenen series değerleri kullanıcıya seçtirtilir.
            selected_series = st.selectbox("seriyi seçin", series_values_df.iloc[:,1], index=None)

            if selected_series:

                #seçilen series'in serie code'u belirlenir.
                serie_code = series_values_df.loc[series_values_df["SERIE_NAME"] == selected_series , "SERIE_CODE"].values[0]
                if serie_code:
                    #Başlangıç tarihinin alınması
                    start_date = series_values_df.loc[series_values_df["SERIE_NAME"] == selected_series, "START_DATE"].values[0]
                    st.write(start_date) 
                    #Belirlenen series code ile df tanımlanır.
                    df = evds.get_data([serie_code], startdate=f"{start_date}", enddate="06-08-2024")
                    #df = evds.get_data([serie_code], startdate="01-01-2023", enddate="06-08-2024")
                    #data_name = df.columns[1]
                    
                    # Sort the data by date
                    #df = df.sort_values(by='Tarih')
                    
                    col_name = df.columns[1]
                    if df.isna().values.any():
                        df[col_name] = df[col_name].fillna(method='ffill')

                    #df'i tablo olarak gösterme
                    df_table = df.set_index('Tarih')
                    st.dataframe(df_table.T)

                    #date time
                    df["Tarih"] = pd.to_datetime(df["Tarih"], format="mixed")
                    df = df.sort_values(by="Tarih")
                    st.line_chart(df.set_index('Tarih'))
                    
            
except Exception as e:
    st.write("Hata Ayrıntısı:", e) 















