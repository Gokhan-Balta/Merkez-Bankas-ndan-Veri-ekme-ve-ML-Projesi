import streamlit as st
import pandas as pd
from evds import evdsAPI
from data_function import select_and_process_data

# API ayarlanması
evds = evdsAPI("********")

# Ana kategorileri çekilmesi
main_categories_df = evds.main_categories

st.title("EVDS PROJECT")


try:
    page = st.sidebar.selectbox("Seçiniz:", ["Veri Analizi", "Zaman Serisi Çalışması"], index=None)

    if page == "Veri Analizi":
        # Fonksiyonu çağırarak veri seçimi ve işleme
        df_page_1, serie_code_update = select_and_process_data(main_categories_df, evds)

        if df_page_1 is not None and serie_code_update is not None:
            # df'i tablo olarak gösterme
            st.dataframe(df_page_1.T, height=100)
            
            # Grafiğini çizdirme
            st.line_chart(df_page_1[serie_code_update])

            # Tanımlayıcı istatistikleri hesaplayıp yazdırma
            mean = df_page_1[serie_code_update].mean()
            std = df_page_1[serie_code_update].std()
            variance = df_page_1[serie_code_update].var()
            results_stat = pd.DataFrame({
                "stats": ["mean", "standart deviation", "variance"],
                "value": [mean, std, variance]
            })
            results_stat["value"] = results_stat["value"].apply(lambda x: round(x, 2))
            st.dataframe(results_stat.T)

    elif page == "Zaman Serisi Çalışması":
        st.write("Zaman Serisi Çalışması sayfası :)")
        # Zaman Serisi Çalışması için fonksiyonu kullanma
        df_page_2, serie_code_update = select_and_process_data(main_categories_df, evds)



        

except Exception as e:
    st.write("Hata Ayrıntısı:", e)
