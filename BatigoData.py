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


col1, col2, col3 = st.columns(3)

# Overall metric
with col1:
    total_count = dfh["id"].count()  # Replace "count(id)" with appropriate syntax
    st.markdown('<div class="column">', unsafe_allow_html=True)
    st.metric(label="Jumlah Pengunjung", value=total_count)
    st.markdown('</div>', unsafe_allow_html=True)

# Metric for user_id > 0/login
with col2:
    dfh_non_zero = dfh[dfh["user_id"] > 0]  # Create a filtered DataFrame
    non_zero_count = dfh_non_zero["id"].count()
    st.markdown('<div class="column">', unsafe_allow_html=True)
    st.metric(label="Jumlah Pengunjung Login", value=non_zero_count)
    st.markdown('</div>', unsafe_allow_html=True)

# Metric for user_id == 0 /guest
with col3:
    dfh_zero = dfh[dfh["user_id"] == 0]  # Create a filtered DataFrame
    zero_count = dfh_zero["id"].count()
    st.markdown('<div class="column">', unsafe_allow_html=True)
    st.metric(label="Jumlah Pengunjung Guest", value=zero_count)
    st.markdown('</div>', unsafe_allow_html=True)


col4, col5, col6 = st.columns(3,border=True)
# Filter once for current and previous year
current_year = datetime.now().year
previous_year = current_year - 1

dfh_now = dfh[dfh["hit_time"].dt.year == current_year]  # Current year data
dfh_prev = dfh[dfh["hit_time"].dt.year == previous_year]  # Previous year data

with col4:
    # Calculate total visitor counts
    total_count = dfh_now["id"].count()
    total_prev = dfh_prev["id"].count()

    # Avoid division by zero
    delta = ((total_count - total_prev) / total_prev * 100) if total_prev != 0 else 0
    st.markdown('<div class="column">', unsafe_allow_html=True)
    st.metric(label="Jumlah Pengunjung (Tahun Ini)", value=total_count, delta=f"{delta:.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    # Filter for logged-in users (user_id > 0)
    non_zero_count = dfh_now[dfh_now["user_id"] > 0]["id"].count()
    non_prev_count = dfh_prev[dfh_prev["user_id"] > 0]["id"].count()

    # Avoid division by zero
    delta = ((non_zero_count - non_prev_count) / non_prev_count * 100) if non_prev_count != 0 else 0
    st.markdown('<div class="column">', unsafe_allow_html=True)
    st.metric(label="Jumlah Pengunjung Login (Tahun Ini)", value=non_zero_count, delta=f"{delta:.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    # Filter for guest users (user_id == 0)
    zero_count = dfh_now[dfh_now["user_id"] == 0]["id"].count()
    zero_prev = dfh_prev[dfh_prev["user_id"] == 0]["id"].count()

    # Avoid division by zero
    delta = ((zero_count - zero_prev) / zero_prev * 100) if zero_prev != 0 else 0
    st.markdown('<div class="column">', unsafe_allow_html=True)
    st.metric(label="Jumlah Pengunjung Guest (Tahun Ini)", value=zero_count, delta=f"{delta:.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)

col7, col8, col9 = st.columns(3,border=True)
# Get the current date
now = datetime.now()

# Current and previous month
current_month = now.month
previous_month = current_month - 1
current_year = now.year
previous_year = current_year if previous_month > 0 else current_year - 1
if previous_month == 0:
    previous_month = 12

# Filter the DataFrame for the current month
dfh_current_month = dfh[
    (dfh["hit_time"].dt.month == current_month) & (dfh["hit_time"].dt.year == current_year)
]

# Filter the DataFrame for the previous month
dfh_previous_month = dfh[
    (dfh["hit_time"].dt.month == previous_month) & (dfh["hit_time"].dt.year == previous_year)
]

with col7:
    # Calculate total visitors
    total_count = dfh_current_month["id"].count()
    total_prev = dfh_previous_month["id"].count()

    # Avoid division by zero
    delta = ((total_count - total_prev) / total_prev * 100) if total_prev != 0 else 0
    st.markdown('<div class="column">', unsafe_allow_html=True)
    st.metric(label="Jumlah Pengunjung (Bulan Ini)", value=total_count, delta=f"{delta:.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col8:
    # Filter for logged-in users (user_id > 0)
    non_zero_count = dfh_current_month[dfh_current_month["user_id"] > 0]["id"].count()
    non_prev_count = dfh_previous_month[dfh_previous_month["user_id"] > 0]["id"].count()

    # Avoid division by zero
    delta = ((non_zero_count - non_prev_count) / non_prev_count * 100) if non_prev_count != 0 else 0
    st.markdown('<div class="column">', unsafe_allow_html=True)
    st.metric(label="Jumlah Pengunjung Login (Bulan Ini)", value=non_zero_count, delta=f"{delta:.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col9:
    # Filter for guest users (user_id == 0)
    zero_count = dfh_current_month[dfh_current_month["user_id"] == 0]["id"].count()
    zero_prev = dfh_previous_month[dfh_previous_month["user_id"] == 0]["id"].count()

    # Avoid division by zero
    delta = ((zero_count - zero_prev) / zero_prev * 100) if zero_prev != 0 else 0
    st.markdown('<div class="column">', unsafe_allow_html=True)
    st.metric(label="Jumlah Pengunjung Guest (Bulan Ini)", value=zero_count, delta=f"{delta:.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)

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