import streamlit as st
import pandas as pd
from evds import evdsAPI


def select_and_process_data(main_categories_df, evds):
    # Kullanıcıdan ana başlığı seçmesini iste
    selected_main_title = st.selectbox("Konu başlığını seçin", main_categories_df.iloc[:, 1], index=None)

    if selected_main_title:
        # Seçilen ana başlığa göre category_id alınır
        category_id = main_categories_df.loc[main_categories_df["TOPIC_TITLE_TR"] == selected_main_title, "CATEGORY_ID"].values[0]
        category_id = int(category_id)

        # category_id ile sub kategori değerleri alınır
        sub_category_df = evds.get_sub_categories(category_id)
        selected_sub_category = st.selectbox("Konu başlığını seçin", sub_category_df.iloc[:, 2], index=None)

        if selected_sub_category:
            # Seçilen sub kategori ile group code alınır
            selected_group_code = sub_category_df.loc[sub_category_df["DATAGROUP_NAME"] == selected_sub_category, "DATAGROUP_CODE"].values[0]
            series_values_df = evds.get_series(selected_group_code)
            selected_series = st.selectbox("Seriyi seçin", series_values_df.iloc[:, 1], index=None)

            if selected_series:
                # Seçilen serinin kodu alınır
                serie_code = series_values_df.loc[series_values_df["SERIE_NAME"] == selected_series, "SERIE_CODE"].values[0]

                if serie_code:
                    # DataFrame tanımlanır
                    serie_code_update = serie_code.replace(".", "_")
                    df = evds.get_data([serie_code], startdate="01-01-2020", enddate="20-08-2024")

                    # Veri setini işle
                    df["Tarih"] = pd.to_datetime(df["Tarih"], dayfirst=True)
                    df.set_index("Tarih", inplace=True)

                    # NaN değerleri doldurma
                    if df.isna().values.any():
                        df = df.ffill()
                    df = df.dropna()

                    return df, serie_code_update  # Döndürülen değerler

    return None, None  # Hiçbir değer seçilmezse
