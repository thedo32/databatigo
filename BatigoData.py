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

# Inject CSS for column styling
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
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Overall metric
# Assume dfh is already loaded and preprocessed
dfh['hit_time'] = pd.to_datetime(dfh['hit_time'], errors='coerce')
#dfh['hit_day'] = dfh['hit_time'].dt.date  # Extract the date part for grouping

st.markdown("## Data Jumlah Pengunjung")
# Main columns for metrics
col1, col2, col3 = st.columns(3, border=True)

# Total unique visitors

with col1:
    dfh_non_zero = dfh[dfh["user_id"] > 0]
    unique_logged_in_visitors = dfh_non_zero.groupby(['user_id', 'ip_address']).ngroups
    zero_count = dfh[dfh["user_id"] == 0]["id"].count()

    total_unique_visitors = unique_logged_in_visitors + zero_count
    st.metric(label="Jumlah Pengunjung", value=total_unique_visitors)

# Logged-in visitors (user_id > 0)
with col2:
    dfh_non_zero = dfh[dfh["user_id"] > 0]
    unique_logged_in_visitors = dfh_non_zero.groupby(['user_id', 'ip_address']).ngroups
    st.metric(label="Jumlah Pengunjung Login", value=unique_logged_in_visitors)

# Guest visitors (user_id == 0)
with col3:
    #dfh_zero = dfh[dfh["user_id"] == 0]
    #unique_guest_visitors = dfh_zero.groupby(['user_id', 'ip_address']).ngroups
    #st.metric(label="Jumlah Pengunjung Guest", value=unique_guest_visitors)

    # Count all hits for guest users without applying uniqueness
    zero_count = dfh[dfh["user_id"] == 0]["id"].count()
    st.metric(label="Jumlah Pengunjung Guest", value=zero_count)

# Yearly metrics
col4, col5, col6 = st.columns(3, border=True)
current_year = datetime.now().year
previous_year = current_year - 1

dfh_now = dfh[dfh["hit_time"].dt.year == current_year]
dfh_prev = dfh[dfh["hit_time"].dt.year == previous_year]

with col4:
    non_zero_count = dfh_now[dfh_now["user_id"] > 0].groupby(['user_id', 'ip_address']).ngroups
    non_prev_count = dfh_prev[dfh_prev["user_id"] > 0].groupby(['user_id', 'ip_address']).ngroups
    zero_count = dfh_now[dfh_now["user_id"] == 0]["id"].count()
    zero_prev = dfh_prev[dfh_prev["user_id"] == 0]["id"].count()

    total_count = non_zero_count + zero_count
    total_prev = non_prev_count + zero_prev
    delta = ((total_count - total_prev) / total_prev * 100) if total_prev != 0 else 0
    st.metric(label="Jumlah Pengunjung (Tahun Ini)", value=total_count, delta=f"{delta:.2f}%")

with col5:
    non_zero_count = dfh_now[dfh_now["user_id"] > 0].groupby(['user_id', 'ip_address']).ngroups
    non_prev_count = dfh_prev[dfh_prev["user_id"] > 0].groupby(['user_id', 'ip_address']).ngroups
    delta = ((non_zero_count - non_prev_count) / non_prev_count * 100) if non_prev_count != 0 else 0
    st.metric(label="Jumlah Pengunjung Login (Tahun Ini)", value=non_zero_count, delta=f"{delta:.2f}%")

with col6:
    #zero_count = dfh_now[dfh_now["user_id"] == 0].groupby(['user_id', 'ip_address']).ngroups
    #zero_prev = dfh_prev[dfh_prev["user_id"] == 0].groupby(['user_id', 'ip_address']).ngroups

    #count the guest witout uniqueness
    zero_count = dfh_now[dfh_now["user_id"] == 0]["id"].count()
    zero_prev = dfh_prev[dfh_prev["user_id"] == 0]["id"].count()

    delta = ((zero_count - zero_prev) / zero_prev * 100) if zero_prev != 0 else 0
    st.metric(label="Jumlah Pengunjung Guest (Tahun Ini)", value=zero_count, delta=f"{delta:.2f}%")

# Monthly metrics
col7, col8, col9 = st.columns(3, border=True)
now = datetime.now()
current_month = now.month
previous_month = current_month - 1
current_year = now.year
previous_year = current_year if previous_month > 0 else current_year - 1
if previous_month == 0:
    previous_month = 12

dfh_current_month = dfh[
    (dfh["hit_time"].dt.month == current_month) & (dfh["hit_time"].dt.year == current_year)
]
dfh_previous_month = dfh[
    (dfh["hit_time"].dt.month == previous_month) & (dfh["hit_time"].dt.year == previous_year)
]

with col7:
    non_zero_count = dfh_current_month[dfh_current_month["user_id"] > 0].groupby(
        ['user_id', 'ip_address']).ngroups
    non_prev_count = dfh_previous_month[dfh_previous_month["user_id"] > 0].groupby(
        ['user_id', 'ip_address']).ngroups

    zero_count = dfh_current_month[dfh_current_month["user_id"] == 0]["id"].count()
    zero_prev = dfh_previous_month[dfh_previous_month["user_id"] == 0]["id"].count()

    total_count = non_zero_count + zero_count
    total_prev = non_prev_count + zero_prev
    delta = ((total_count - total_prev) / total_prev * 100) if total_prev != 0 else 0
    st.metric(label="Jumlah Pengunjung (Bulan Ini)", value=total_count, delta=f"{delta:.2f}%")

with col8:
    non_zero_count = dfh_current_month[dfh_current_month["user_id"] > 0].groupby(['user_id', 'ip_address']).ngroups
    non_prev_count = dfh_previous_month[dfh_previous_month["user_id"] > 0].groupby(['user_id', 'ip_address']).ngroups
    delta = ((non_zero_count - non_prev_count) / non_prev_count * 100) if non_prev_count != 0 else 0
    st.metric(label="Jumlah Pengunjung Login (Bulan Ini)", value=non_zero_count, delta=f"{delta:.2f}%")

with col9:
    #zero_count = dfh_current_month[dfh_current_month["user_id"] == 0].groupby(['user_id', 'ip_address']).ngroups
    #zero_prev = dfh_previous_month[dfh_previous_month["user_id"] == 0].groupby(['user_id', 'ip_address']).ngroups
    #delta = ((zero_count - zero_prev) / zero_prev * 100) if zero_prev != 0 else 0
    #st.metric(label="Jumlah Pengunjung Guest (Bulan Ini)", value=zero_count, delta=f"{delta:.2f}%")

    #count guest without uniqueness
    zero_count = dfh_current_month[dfh_current_month["user_id"] == 0]["id"].count()
    zero_prev = dfh_previous_month[dfh_previous_month["user_id"] == 0]["id"].count()

    # Avoid division by zero
    delta = ((zero_count - zero_prev) / zero_prev * 100) if zero_prev != 0 else 0
    st.metric(label="Jumlah Pengunjung Guest (Bulan Ini)", value=zero_count, delta=f"{delta:.2f}%")

st.divider()

# Aggregating data by date
# Ensure 'hit_time' is in datetime format
dfh['hit_time'] = pd.to_datetime(dfh['hit_time'], errors='coerce')

# Handle any invalid conversions (if 'errors="coerce"', non-datetime entries will become NaT)
if dfh['hit_time'].isna().any():
    st.warning("Some entries in 'hit_time' could not be converted to datetime and were dropped.")
    dfh = dfh.dropna(subset=['hit_time'])

# Extract the date for aggregation
dfh['tanggal'] = dfh['hit_time'].dt.date  # Extract date from datetime
daily_visits = dfh.groupby('tanggal').size().reset_index(name='visit_count')


tab1, tab2, tab3 = st.tabs(["Jumlah Kunjungan per Wilayah","Jumlah Kunjungan per Halaman",  "Pengguna Terdaftar"])

with (tab1):
    # DAILY TIME ANALYSYS

    st.markdown("## Analisa Kunjungan Per Hari")

    # Filter out "Other" and "Unknown"
    dfh = dfh[~dfh['country'].isin(["Other", "Unknown"])]
    dfh = dfh[~dfh['city'].isin(["Other", "Unknown"])]

    st.markdown("### Filter Menurut Negara dan Kota")

    # Multiselect for country
    selected_countries = st.multiselect(
        "Pilih Negara",
        options=["All"] + dfh['country'].unique().tolist(),
        default=["All"],
    )

    # Filter based on selected countries
    if "All" not in selected_countries:
        dfh = dfh[dfh['country'].isin(selected_countries)]

    # Multiselect for city
    filtered_cities = dfh['city'].unique()
    selected_cities = st.multiselect(
        "Pilih Kota",
        options=["All"] + sorted(filtered_cities),
        default=["All"],
    )

    # Filter based on selected cities
    if "All" not in selected_cities:
        dfh = dfh[dfh['city'].isin(selected_cities)]

    # Aggregate filtered data
    daily_visits_filtered = dfh.groupby('tanggal').size().reset_index(name='visit_count')

    # Plot the filtered data
    if not daily_visits_filtered.empty:
        time_series_chart_filtered = alt.Chart(daily_visits_filtered).mark_line().encode(
            x=alt.X('tanggal:T', title='Tanggal'),
            y=alt.Y('visit_count:Q', title='Jumlah Kunjungan'),
            tooltip=[
                alt.Tooltip('tanggal:T', title='Tanggal', format='%Y-%m-%d'),
                alt.Tooltip('visit_count:Q', title='Kunjungan')
            ]
        ).properties(
            title="Kunjungan Per Hari Berdasarkan Wilayah",
            height=400,
            width=1200
        ).interactive()
        st.altair_chart(time_series_chart_filtered)
    else:
        st.warning("Tidak ada  data tersedia untuk filters yang dipilih.")

    st.divider()

    st.markdown("## Kunjungan Per Wilayah")
    # Altair Bar Chart for All Countries

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

    df = df.copy()
    df['trunc_city'] = df['city'].apply(lambda x: x if len(x) <= 10 else x[:10] + '...')

    colD, colE, colF = st.columns(3)
    with colD:
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


    with colE:
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

    with colF:
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

#kunjungan per halaman
with tab2:

    # DAILY TIME ANALYSYS
    st.markdown("## Analisa Kunjungan Per Hari")

    # Multiselect for country
    selected_countries = st.multiselect(
        "Pilih Negara",
        options=["All"] + dfh['country'].unique().tolist(),
        default=["All"],
        key="halaman_country"
    )

    if "All" not in selected_countries:
        dfh = dfh[dfh['country'].isin(selected_countries)]

    # Multiselect for pages
    filtered_pages = dfh['title'].unique()
    selected_pages = st.multiselect(
        "Pilih Halaman",
        options=["All"] + sorted(filtered_pages),
        default=["All"],
    )

    if "All" not in selected_pages:
        dfh = dfh[dfh['title'].isin(selected_pages)]

    # Aggregate filtered data
    daily_visits_filtered = dfh.groupby('tanggal').size().reset_index(name='visit_count')

    # Plot filtered data
    if not daily_visits_filtered.empty:
        time_series_chart_filtered = alt.Chart(daily_visits_filtered).mark_line().encode(
            x=alt.X('tanggal:T', title='Tanggal'),
            y=alt.Y('visit_count:Q', title='Jumlah Kunjungan'),
            tooltip=[
                alt.Tooltip('tanggal:T', title='Tanggal', format='%Y-%m-%d'),
                alt.Tooltip('visit_count:Q', title='Kunjungan')
            ]
        ).properties(
            title="Kunjungan Per Hari Berdasarkan Halaman",
            height=400,
            width=1200
        ).interactive()
        st.altair_chart(time_series_chart_filtered)
    else:
        st.warning("Tidak ada  data tersedia untuk filters yang dipilih.")

    st.divider()


    st.markdown("## Kunjungan Per Halaman")
    # Altair Bar Chart

    # filter other or unknown
    df = dfh[~dfh['title'].isin(["Other", "Unknown", "Login", "Register"])]

    all_countries = df['country'].unique().tolist()

    selection = alt.selection_point(fields=['country'], bind='legend')

    bars = alt.Chart(df).mark_bar(size=6).encode(
        x=alt.X(
            "title:N",
            title="Judul Halaman",
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
        tooltip=["country", "title", "count(id)"]  # Add tooltips for interactivity
    ).add_params(selection).transform_filter(selection).properties(
        height=800,
        width=1200
    ).interactive(bind_x=True, bind_y=True)

    st.altair_chart(bars)

    st.divider()

    df = df.copy()
    df['trunc_title'] = df['title'].apply(lambda x: x if len(x) <= 10 else x[:10] + '...')

    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown("<h4 style='text-align: center;'>Top 10 Halaman/Menu</h4>", unsafe_allow_html=True)


        # Select the top 10 cities (you can define criteria, e.g., most frequent)
        top_10_pages = df['title'].value_counts().head(10).index.tolist()

        # Filter the DataFrame to include only these top 10 cities
        filtered_df = df[df['title'].isin(top_10_pages)]

        bars = alt.Chart(filtered_df).mark_bar(size=30).encode(
            x=alt.X(
                "trunc_title:N",
                title=("Top 10 Halaman Dikunjungi"),
                axis=alt.Axis(labelAngle=90),
                sort=alt.EncodingSortField(field="id", op="count", order="descending")
            ),
            y=alt.Y("count(id):Q", title="Jumlah Kunjungan"),  # Count occurrences by city
            # Different colors for each country
            tooltip=["title", "count(id)"]  # Add tooltips for interactivity
        ).properties(
            height=400,
            width=400
        ).interactive(bind_x=True, bind_y=True)

        st.altair_chart(bars)


    with colB:
        st.markdown("<h4 style='text-align: center;'>Top 10 diakses Dalam Negri</h4>", unsafe_allow_html=True)

        # Filter rows where the country is "Indonesia"
        indonesia_pages = df[df['country'] == 'Indonesia']

        # Select the top 10 cities (you can define criteria, e.g., most frequent)
        top_10_pages = indonesia_pages['title'].value_counts().head(10).index.tolist()

        # Filter the DataFrame to include only these top 10 cities
        filtered_df = indonesia_pages[indonesia_pages['title'].isin(top_10_pages)]

        bars = alt.Chart(filtered_df).mark_bar(size=30).encode(
            x=alt.X(
                "trunc_title:N",
                title="Judul Halaman",
                axis=alt.Axis(labelAngle=90),
                sort=alt.EncodingSortField(field="id", op="count", order="descending")
            ),
            y=alt.Y("count(id):Q", title="Jumlah Kunjungan"),  # Count occurrences by city
            # Different colors for each country
            tooltip=[ "title", "count(id)"]  # Add tooltips for interactivity
        ).properties(
            height=400,
            width=400
        ).interactive(bind_x=True, bind_y=True)

        st.altair_chart(bars)

    with colC:
        st.markdown("<h4 style='text-align: center;'>Top 10 Halaman diakses Luar Negeri</h4>", unsafe_allow_html=True)

        # Filter rows where the country is outside "Indonesia"
        abroad_cities = df[df['country'] != 'Indonesia']

        # Select the top 10 cities (you can define criteria, e.g., most frequent)
        top_10_pages = abroad_cities['title'].value_counts().head(10).index.tolist()

        # Filter the DataFrame to include only these top 10 cities
        filtered_df = abroad_cities[abroad_cities['title'].isin(top_10_pages)]

        bars = alt.Chart(filtered_df).mark_bar(size=30).encode(
            x=alt.X(
                "trunc_title:N",
                title="Judul Halaman",
                axis=alt.Axis(labelAngle=90),
                sort=alt.EncodingSortField(field="id", op="count", order="descending")
            ),
            y=alt.Y("count(id):Q", title="Jumlah Kunjungan"),  # Count occurrences by city
            # Different colors for each country
            tooltip=["title", "count(id)"]  # Add tooltips for interactivity
        ).properties(
            height=400,
            width=400
        ).interactive(bind_x=True, bind_y=True)

        st.altair_chart(bars)

#kunjungan per wilayah

with tab3:

    interactive_table(dfu,
                      caption='Users',
                      select=False,
                      buttons=['copyHtml5', 'csvHtml5', 'excelHtml5', 'colvis'])