import altair as alt
from src.styles.custom_theme import get_color_palette

COLORS = get_color_palette()

def get_time_series_config():
    """
    Configuration for time series visualizations.
    """
    return {
        'line_color': COLORS['primary'],
        'fill_color': COLORS['primary'],
        'hover_color': COLORS['secondary'],
        'axis_color': COLORS['text'],
        'grid_color': COLORS['muted'],
        'tooltip_template': """
            <div style="background-color: white; padding: 10px; border-radius: 5px;">
                <b>Year:</b> @year<br>
                <b>Total Gross:</b> $@total_gross{0,0}<br>
                <b>Inflation Adjusted:</b> $@inflation_adjusted_gross{0,0}<br>
                <b>Movies Released:</b> @movie_count
            </div>
        """
    }

def get_genre_chart_config():
    """
    Configuration for genre distribution charts.
    """
    return {
        'color_scheme': 'blues',
        'sort_by': '-y',
        'title': 'Genre Distribution',
        'axis_labels': {
            'x': 'Number of Movies',
            'y': 'Genre'
        },
        'tooltip': ['genre', 'count']
    }

def get_rating_chart_config():
    """
    Configuration for MPAA rating charts.
    """
    return {
        'colors': [COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['warning']],
        'title': 'MPAA Rating Distribution',
        'inner_radius': 0.6,
        'tooltip': ['rating', 'count', 'percentage']
    }

def get_seasonal_heatmap_config():
    """
    Configuration for seasonal analysis heatmap.
    """
    return {
        'colorscale': [
            [0, COLORS['background']],
            [0.5, COLORS['primary']],
            [1, COLORS['secondary']]
        ],
        'title': 'Seasonal Release Patterns',
        'axis_labels': {
            'x': 'Season',
            'y': 'Metric'
        }
    }

def get_success_metrics_config():
    """
    Configuration for success metrics visualizations.
    """
    return {
        'success_color': COLORS['success'],
        'warning_color': COLORS['warning'],
        'danger_color': COLORS['danger'],
        'tooltip_template': """
            <div style="background-color: white; padding: 10px; border-radius: 5px;">
                <b>Movie:</b> @movie_title<br>
                <b>Revenue:</b> $@total_gross{0,0}<br>
                <b>Performance Ratio:</b> @performance_ratio{0.00}<br>
                <b>Success Level:</b> @success_level
            </div>
        """
    }

def create_time_series_line_chart(data):
    return alt.Chart(data).mark_line(point=True, color=COLORS[0]).encode(
        x=alt.X('year:O', title='Year'),
        y=alt.Y('total_gross:Q', title='Revenue ($)', axis=alt.Axis(format='$~s')),
        tooltip=[alt.Tooltip('year:O', title='Year'), alt.Tooltip('total_gross:Q', title='Total Gross', format=',')]
    ).properties(width=900, height=350, background='#fff').configure_axis(
        labelColor='#23272f', titleColor='#23272f'
    )

def create_genre_chart(data):
    chart = alt.Chart(data).mark_bar(size=20).encode(
        x=alt.X('count:Q', title='count', axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
        y=alt.Y('genre:N', sort='-x', axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
        color=alt.value(COLORS[0]),
        tooltip=[alt.Tooltip('genre:N'), alt.Tooltip('count:Q')]
    ).properties(
        width=400,
        height=300,
        background="#fff"
    ).configure_axis(
        labelColor='#1c1e21',
        titleColor='#1c1e21'
    ).configure_view(
        stroke=None
    )
    return chart

def create_rating_chart(data):
    fig = go.Figure(
        data=[go.Pie(
            labels=data['mpaa_rating'],
            values=data['count'],
            hole=0.5,
            marker=dict(colors=COLORS),
            textinfo='percent+label',
            insidetextorientation='radial',
            textfont=dict(color='#1c1e21', size=14),
            hoverinfo='label+percent+value',
        )]
    )
    fig.update_layout(
        paper_bgcolor="#fff",
        plot_bgcolor="#fff",
        font=dict(color='#1c1e21', size=14),
        legend=dict(font=dict(color='#1c1e21', size=12)),
        margin=dict(t=40, b=40, l=40, r=40)
    )
    return fig

def create_seasonal_heatmap(data):
    fig = go.Figure(
        data=go.Bar(
            x=data['season'],
            y=data['movie_title'],
            marker_color=COLORS[1],
            text=data['movie_title'],
            textposition='auto',
            hoverinfo='x+y',
        )
    )
    fig.update_layout(
        paper_bgcolor="#fff",
        plot_bgcolor="#fff",
        font=dict(color='#1c1e21', size=14),
        margin=dict(t=40, b=40, l=40, r=40)
    )
    return fig 