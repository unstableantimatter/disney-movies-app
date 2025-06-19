import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import numpy as np
import altair as alt
from PIL import Image

# Add the src directory to Python path
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from src.utils.data_processor import (
    load_and_process_data,
    get_summary_statistics,
    get_time_series_data,
    get_genre_distribution,
    get_rating_distribution,
    get_seasonal_analysis
)
from src.visualizations.chart_configs import (
    create_time_series_line_chart,
    create_genre_chart,
    create_rating_chart,
    create_seasonal_heatmap
)
from src.styles.custom_theme import apply_custom_theme, get_color_palette

# Apply custom theme
apply_custom_theme()
COLORS = get_color_palette()

# Load and process data
DATA_PATH = Path(__file__).parent / "data" / "disney_movies.csv"
@st.cache_data
def load_data():
    return load_and_process_data(DATA_PATH)

df = load_data()
summary_stats = get_summary_statistics(df)

# Compute revenue quartiles for dropdown
revenue_quartiles = df['total_gross'].quantile([0, 0.25, 0.5, 0.75, 0.9]).astype(int)
revenue_options = [
    (0, "No Minimum"),
    (revenue_quartiles.loc[0.25], f"25th Percentile (${'{:,}'.format(revenue_quartiles.loc[0.25])})"),
    (revenue_quartiles.loc[0.5], f"Median (${'{:,}'.format(revenue_quartiles.loc[0.5])})"),
    (revenue_quartiles.loc[0.75], f"75th Percentile (${'{:,}'.format(revenue_quartiles.loc[0.75])})"),
    (revenue_quartiles.loc[0.9], f"90th Percentile (${'{:,}'.format(revenue_quartiles.loc[0.9])})"),
]

# Sidebar Filters
with st.sidebar:
    st.header("Filters")
    year_range = st.slider(
        "Select Year Range",
        min_value=int(df['year'].min()),
        max_value=int(df['year'].max()),
        value=(int(df['year'].min()), int(df['year'].max()))
    )

    # Genre Checkbox Group
    st.markdown("**Select Genres**")
    all_genres = sorted(df['genre'].unique())
    if 'selected_genres' not in st.session_state:
        st.session_state.selected_genres = set(all_genres)
    for genre in all_genres:
        checked = genre in st.session_state.selected_genres
        if st.checkbox(genre, value=checked, key=f"genre_{genre}"):
            st.session_state.selected_genres.add(genre)
        else:
            st.session_state.selected_genres.discard(genre)
    selected_genres = list(st.session_state.selected_genres)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Select All", key="select_all_genres"):
            st.session_state.selected_genres = set(all_genres)
    with col2:
        if st.button("Clear All", key="clear_all_genres"):
            st.session_state.selected_genres = set()

    # MPAA Rating Checkbox Group
    st.markdown("**Select MPAA Ratings**")
    all_ratings = sorted(df['mpaa_rating'].unique())
    if 'selected_ratings' not in st.session_state:
        st.session_state.selected_ratings = set(all_ratings)
    for rating in all_ratings:
        checked = rating in st.session_state.selected_ratings
        if st.checkbox(rating, value=checked, key=f"rating_{rating}"):
            st.session_state.selected_ratings.add(rating)
        else:
            st.session_state.selected_ratings.discard(rating)
    selected_ratings = list(st.session_state.selected_ratings)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Select All", key="select_all_ratings"):
            st.session_state.selected_ratings = set(all_ratings)
    with col2:
        if st.button("Clear All", key="clear_all_ratings"):
            st.session_state.selected_ratings = set()

    min_revenue_label = st.selectbox(
        "Minimum Revenue",
        options=[label for _, label in revenue_options],
        index=0
    )
    min_revenue = next(val for val, label in revenue_options if label == min_revenue_label)
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; padding-top: 1rem;'>"
        "<a href='https://www.kaggle.com/datasets/prateekmaj21/disney-movies' "
        "style='font-size: 0.9em; text-decoration: none;'>Source Data</a>"
        "</div>",
        unsafe_allow_html=True
    )

# Filter the DataFrame based on sidebar selections
def filter_df(df):
    if not selected_genres or not selected_ratings:
        # Return empty DataFrame with correct columns if any filter group is empty
        return df.iloc[0:0]
    filtered = df[
        (df['year'] >= year_range[0]) &
        (df['year'] <= year_range[1]) &
        (df['genre'].isin(selected_genres)) &
        (df['mpaa_rating'].isin(selected_ratings)) &
        (df['total_gross'] >= min_revenue)
    ]
    return filtered

filtered_df = filter_df(df)

# Use filtered_df for all downstream calculations and visualizations
summary_stats = get_summary_statistics(filtered_df)

# --- BANNER ---
with st.container():
    try:
        image_path = Path(__file__).parent / "images" / "disney_dashboard.png"
        image = Image.open(image_path)
        st.image(image, use_container_width=True)
    except FileNotFoundError:
        st.info("To add a banner, place an image named `disney_dashboard.png` in the `src/images` directory.")

# --- TOP STATS ---
with st.container():
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        st.metric("Total Movies", f"{summary_stats['total_movies']:,}")
    with col2:
        st.metric("Date Range", summary_stats['date_range'])
    with col3:
        st.metric("Mean Revenue", f"${df['total_gross'].mean():,.0f}")
    with col4:
        st.metric("Median Revenue", f"${df['total_gross'].median():,.0f}")
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# --- BOX OFFICE PERFORMANCE OVER TIME ---
with st.container():
    st.subheader("Box Office Performance Over Time")
    time_series_data = get_time_series_data(filtered_df)

    hover = alt.selection_single(
        fields=["year"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    base = alt.Chart(time_series_data).encode(
        x=alt.X('year:O', title='Year'),
        y=alt.Y('total_gross:Q', title='Revenue ($)', axis=alt.Axis(labelExpr="'$' + replace(format(datum.value, '~s'), 'G', 'B')")),
        tooltip=[alt.Tooltip('year:O', title='Year'), alt.Tooltip('total_gross:Q', title='Total Gross', format='$,.0f')]
    )

    lines = base.mark_line(point=True, color=COLORS[0])

    # Create a transparent layer with points to attach selection
    selectors = base.mark_point(size=200, opacity=0).add_selection(
        hover
    )
    
    # Draw a rule at the location of the selection
    rule = alt.Chart(time_series_data).mark_rule(color='gray').encode(
        x='year:O'
    ).transform_filter(hover)

    # Layer the charts
    chart = alt.layer(
        lines, selectors, rule
    ).properties(width=900, height=350, background='#fff').configure_axis(
        labelColor='#23272f', titleColor='#23272f'
    )

    st.altair_chart(chart, use_container_width=True)
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# --- GENRE ANALYSIS ---
with st.container():
    st.subheader("Genre Analysis")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("**Genre Distribution**")
        genre_dist = filtered_df['genre'].value_counts().reset_index()
        genre_dist.columns = ['genre', 'count']
        genre_domain = genre_dist['genre'].tolist()
        chart = alt.Chart(genre_dist).mark_bar(size=18).encode(
            y=alt.Y('genre:N', sort='-x', title='Genre'),
            x=alt.X('count:Q', title='Number of Movies'),
            color=alt.Color('genre:N', scale=alt.Scale(domain=genre_domain, range=COLORS), legend=alt.Legend(labelColor='#23272f', titleColor='#23272f')),
            tooltip=['genre', 'count']
        ).properties(width=350, height=300, background='#fff').configure_axis(
            labelColor='#23272f', titleColor='#23272f'
        )
        st.altair_chart(chart, use_container_width=True)
    with col2:
        st.markdown("**Genre by Revenue**")
        genre_rev = filtered_df.groupby('genre', observed=True)['total_gross'].sum().reset_index().sort_values('total_gross', ascending=False)
        genre_rev_domain = genre_rev['genre'].tolist()
        chart = alt.Chart(genre_rev).mark_bar(size=18).encode(
            y=alt.Y('genre:N', sort='-x', title='Genre'),
            x=alt.X('total_gross:Q', title='Total Revenue ($)', axis=alt.Axis(labelExpr="'$' + replace(format(datum.value, '~s'), 'G', 'B')")),
            color=alt.Color('genre:N', scale=alt.Scale(domain=genre_rev_domain, range=COLORS), legend=alt.Legend(labelColor='#23272f', titleColor='#23272f')),
            tooltip=['genre', alt.Tooltip('total_gross:Q', title='Total Gross', format='$,.0f')]
        ).properties(width=350, height=300, background='#fff').configure_axis(
            labelColor='#23272f', titleColor='#23272f'
        )
        st.altair_chart(chart, use_container_width=True)
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# --- GENRE REVENUE TREND OVER TIME ---
with st.container():
    st.subheader("Genre Revenue Trend Over Time")
    if not filtered_df.empty:
        genre_trend = filtered_df.groupby(['year', 'genre'], observed=True)['total_gross'].sum().reset_index()
        genre_trend_domain = genre_trend['genre'].unique().tolist()
        hover = alt.selection_single(
            fields=["year"],
            nearest=True,
            on="mouseover",
            empty="none",
        )
        base = alt.Chart(genre_trend).encode(
            x=alt.X('year:O', title='Year'),
            y=alt.Y('total_gross:Q', title='Total Revenue ($)', axis=alt.Axis(labelExpr="'$' + replace(format(datum.value, '~s'), 'G', 'B')")),
            color=alt.Color('genre:N', scale=alt.Scale(domain=genre_trend_domain, range=COLORS), legend=alt.Legend(labelColor='#23272f', titleColor='#23272f')),
            tooltip=[
                alt.Tooltip('year:O', title='Year'),
                alt.Tooltip('genre:N', title='Genre'),
                alt.Tooltip('total_gross:Q', title='Gross', format='$,.0f')
            ]
        )
        lines = base.mark_line(point=True)
        selectors = base.mark_point(size=0).add_selection(hover)
        tooltips = alt.Chart(genre_trend).mark_rule(opacity=0).encode(
            x='year:O',
            tooltip=[
                alt.Tooltip('year:O', title='Year'),
                alt.Tooltip('genre:N', title='Genre'),
                alt.Tooltip('total_gross:Q', title='Gross', format='$,.0f')
            ]
        ).transform_filter(hover)
        rule = alt.Chart(genre_trend).mark_rule(color='gray').encode(
            x='year:O',
        ).transform_filter(hover)
        chart = alt.layer(
            lines, selectors, rule, tooltips
        ).properties(width=700, height=350, background='#fff').configure_axis(
            labelColor='#23272f', titleColor='#23272f'
        ).configure_legend(
            labelColor='#23272f', titleColor='#23272f'
        ).configure_view(
            stroke=None
        )
        st.altair_chart(chart, use_container_width=True)
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

# --- TOP/BOTTOM MOVIES GRIDS ---
with st.container():
    st.subheader("Top & Bottom Movies by Revenue")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("**Top 20 Movies**")
        top_movies = filtered_df.sort_values('total_gross', ascending=False).head(20)
        st.dataframe(top_movies[['movie_title', 'year', 'genre', 'total_gross']].style.format({'total_gross': '${:,.0f}'}), use_container_width=True)
    with col2:
        st.markdown("**Bottom 20 Movies**")
        bottom_movies = filtered_df.sort_values('total_gross', ascending=True).head(20)
        st.dataframe(bottom_movies[['movie_title', 'year', 'genre', 'total_gross']].style.format({'total_gross': '${:,.0f}'}), use_container_width=True)

st.markdown("---") 