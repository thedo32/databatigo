import streamlit as st
import altair as alt
from requests.exceptions import ChunkedEncodingError
import pandas as pd
import plotly.express as px
import fungsiumum as fu
from datetime import datetime

from itables.streamlit import interactive_table


st.set_page_config(
    page_title="Batigo Data Analisis",
    page_icon="fishtail.png",
    layout="wide",
    menu_items={"About": """##### Batigo Data Analisis. 
            Author: Database Outlet
Email: databaseoutlet@gmail.com
            """}
)

fu.users_csv("users.csv")
fu.hits_csv("hits.csv")

dfu = fu.load_users('users.csv')
dfh = fu.load_users('hits.csv')
dfh["hit_time"] = pd.to_datetime(dfh["hit_time"], errors="coerce")

# Inject CSS for styling
st.markdown(
    """
    <style>
    .column {
        border: 1px solid #cccccc;
        padding: 10px;
        border-radius: 5px;
        background-color: #000000;
        color: #ffffff;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display metrics: Total, Logged-In, and Guest visitors
col1, col2, col3 = st.columns(3)

# Total visitors
with col1:
    total_count = dfh["id"].count()
    st.markdown(f'<div class="column">Jumlah Pengunjung<br><strong>{total_count}</strong></div>', unsafe_allow_html=True)

# Logged-in users
with col2:
    non_zero_count = dfh[dfh["user_id"] > 0]["id"].count()
    st.markdown(f'<div class="column">Jumlah Pengunjung Login<br><strong>{non_zero_count}</strong></div>', unsafe_allow_html=True)

# Guest users
with col3:
    zero_count = dfh[dfh["user_id"] == 0]["id"].count()
    st.markdown(f'<div class="column">Jumlah Pengunjung Guest<br><strong>{zero_count}</strong></div>', unsafe_allow_html=True)

# Metrics for current and previous year
col4, col5, col6 = st.columns(3)

current_year = datetime.now().year
previous_year = current_year - 1

# Filter data for current and previous year
dfh_now = dfh[dfh["hit_time"].dt.year == current_year]
dfh_prev = dfh[dfh["hit_time"].dt.year == previous_year]

with col4:
    total_count = dfh_now["id"].count()
    total_prev = dfh_prev["id"].count()
    delta = ((total_count - total_prev) / total_prev * 100) if total_prev != 0 else 0
    st.markdown(f'<div class="column">Jumlah Pengunjung (Tahun Ini)<br><strong>{total_count}</strong><br><small>Delta: {delta:.2f}%</small></div>', unsafe_allow_html=True)

with col5:
    non_zero_count = dfh_now[dfh_now["user_id"] > 0]["id"].count()
    non_prev_count = dfh_prev[dfh_prev["user_id"] > 0]["id"].count()
    delta = ((non_zero_count - non_prev_count) / non_prev_count * 100) if non_prev_count != 0 else 0
    st.markdown(f'<div class="column">Jumlah Pengunjung Login (Tahun Ini)<br><strong>{non_zero_count}</strong><br><small>Delta: {delta:.2f}%</small></div>', unsafe_allow_html=True)

with col6:
    zero_count = dfh_now[dfh_now["user_id"] == 0]["id"].count()
    zero_prev = dfh_prev[dfh_prev["user_id"] == 0]["id"].count()
    delta = ((zero_count - zero_prev) / zero_prev * 100) if zero_prev != 0 else 0
    st.markdown(f'<div class="column">Jumlah Pengunjung Guest (Tahun Ini)<br><strong>{zero_count}</strong><br><small>Delta: {delta:.2f}%</small></div>', unsafe_allow_html=True)

# Metrics for current and previous month
col7, col8, col9 = st.columns(3)

now = datetime.now()
current_month = now.month
previous_month = current_month - 1 if current_month > 1 else 12
current_year = now.year
previous_year = current_year if previous_month != 12 else current_year - 1

# Filter data for current and previous month
dfh_current_month = dfh[(dfh["hit_time"].dt.month == current_month) & (dfh["hit_time"].dt.year == current_year)]
dfh_previous_month = dfh[(dfh["hit_time"].dt.month == previous_month) & (dfh["hit_time"].dt.year == previous_year)]

with col7:
    total_count = dfh_current_month["id"].count()
    total_prev = dfh_previous_month["id"].count()
    delta = ((total_count - total_prev) / total_prev * 100) if total_prev != 0 else 0
    st.markdown(f'<div class="column">Jumlah Pengunjung (Bulan Ini)<br><strong>{total_count}</strong><br><small>Delta: {delta:.2f}%</small></div>', unsafe_allow_html=True)

with col8:
    non_zero_count = dfh_current_month[dfh_current_month["user_id"] > 0]["id"].count()
    non_prev_count = dfh_previous_month[dfh_previous_month["user_id"] > 0]["id"].count()
    delta = ((non_zero_count - non_prev_count) / non_prev_count * 100) if non_prev_count != 0 else 0
    st.markdown(f'<div class="column">Jumlah Pengunjung Login (Bulan Ini)<br><strong>{non_zero_count}</strong><br><small>Delta: {delta:.2f}%</small></div>', unsafe_allow_html=True)

with col9:
    zero_count = dfh_current_month[dfh_current_month["user_id"] == 0]["id"].count()
    zero_prev = dfh_previous_month[dfh_previous_month["user_id"] == 0]["id"].count()
    delta = ((zero_count - zero_prev) / zero_prev * 100) if zero_prev != 0 else 0
    st.markdown(f'<div class="column">Jumlah Pengunjung Guest (Bulan Ini)<br><strong>{zero_count}</strong><br><small>Delta: {delta:.2f}%</small></div>', unsafe_allow_html=True)

st.divider()

tab1, tab2 = st.tabs(["Pengguna Terdaftar", "Jumlah Kunjungan Ke Website"])
with tab1:

    interactive_table(dfu,
                      caption='Users',
                      select=False,
                      buttons=['copyHtml5', 'csvHtml5', 'excelHtml5', 'colvis'])

with (tab2):
    # Altair Chart

    # filter other or unknown
    df = dfh[~dfh['city'].isin(["Other", "Unknown"])]

    all_countries = df['country'].unique().tolist()

    selection = alt.selection_point(fields=['country'], bind='legend')

    bars = alt.Chart(df).mark_bar(size=6).encode(
        x=alt.X(
            "city:N",
            title="Nama Kota",
            axis=alt.Axis(labelAngle=90),
            sort=alt.EncodingSortField(field="id", op="count", order="descending")
        ),
        y=alt.Y("count(id):Q", title="Jumlah Kunjungan"),  # Count occurrences by city
        xOffset=alt.X("country:N", title="Country"),  # Group by country
        color=alt.Color(
            "country:N",
            title="Negara",
            scale=alt.Scale(domain=all_countries),  # Explicitly set domain
            legend=alt.Legend(title="Pilih Negara")
        ),  # Different colors for each country
        tooltip=["country", "city", "count(id)"]  # Add tooltips for interactivity
    ).add_params(selection).transform_filter(selection).properties(
        height=800,
        width=1200
    ).interactive(bind_x=True, bind_y=True)

    st.altair_chart(bars)

    st.divider()


    df['trunc_city'] = df['city'].apply(lambda x: x if len(x) <= 10 else x[:10] + '...')

    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown("<h3 style='text-align: center;'>Top 10 Kota</h3>", unsafe_allow_html=True)


        # Select the top 10 cities (you can define criteria, e.g., most frequent)
        top_10_cities = df['city'].value_counts().head(10).index.tolist()

        # Filter the DataFrame to include only these top 10 cities
        filtered_df = df[df['city'].isin(top_10_cities)]

        bars = alt.Chart(filtered_df).mark_bar(size=30).encode(
            x=alt.X(
                "trunc_city:N",
                title=("Top 10 Kota"),
                axis=alt.Axis(labelAngle=90),
                sort=alt.EncodingSortField(field="id", op="count", order="descending")
            ),
            y=alt.Y("count(id):Q", title="Jumlah Kunjungan"),  # Count occurrences by city
            # Different colors for each country
            tooltip=["city", "count(id)"]  # Add tooltips for interactivity
        ).properties(
            height=400,
            width=400
        ).interactive(bind_x=True, bind_y=True)

        st.altair_chart(bars)


    with colB:
        st.markdown("<h3 style='text-align: center;'>Top 10 Kota Indonesia</h3>", unsafe_allow_html=True)

        # Filter rows where the country is "Indonesia"
        indonesia_cities = df[df['country'] == 'Indonesia']

        # Select the top 10 cities (you can define criteria, e.g., most frequent)
        top_10_cities = indonesia_cities['city'].value_counts().head(10).index.tolist()

        # Filter the DataFrame to include only these top 10 cities
        filtered_df = indonesia_cities[indonesia_cities['city'].isin(top_10_cities)]

        bars = alt.Chart(filtered_df).mark_bar(size=30).encode(
            x=alt.X(
                "trunc_city:N",
                title="Nama Kota",
                axis=alt.Axis(labelAngle=90),
                sort=alt.EncodingSortField(field="id", op="count", order="descending")
            ),
            y=alt.Y("count(id):Q", title="Jumlah Kunjungan"),  # Count occurrences by city
            # Different colors for each country
            tooltip=[ "city", "count(id)"]  # Add tooltips for interactivity
        ).properties(
            height=400,
            width=400
        ).interactive(bind_x=True, bind_y=True)

        st.altair_chart(bars)

    with colC:
        st.markdown("<h3 style='text-align: center;'>Top 10 Kota Luar Negeri</h3>", unsafe_allow_html=True)

        # Filter rows where the country is outside "Indonesia"
        abroad_cities = df[df['country'] != 'Indonesia']

        # Select the top 10 cities (you can define criteria, e.g., most frequent)
        top_10_cities = abroad_cities['city'].value_counts().head(10).index.tolist()

        # Filter the DataFrame to include only these top 10 cities
        filtered_df = abroad_cities[abroad_cities['city'].isin(top_10_cities)]

        bars = alt.Chart(filtered_df).mark_bar(size=30).encode(
            x=alt.X(
                "trunc_city:N",
                title="Nama Kota",
                axis=alt.Axis(labelAngle=90),
                sort=alt.EncodingSortField(field="id", op="count", order="descending")
            ),
            y=alt.Y("count(id):Q", title="Jumlah Kunjungan"),  # Count occurrences by city
            # Different colors for each country
            tooltip=["city", "count(id)"]  # Add tooltips for interactivity
        ).properties(
            height=400,
            width=400
        ).interactive(bind_x=True, bind_y=True)

        st.altair_chart(bars)