import streamlit as st

def apply_custom_theme():
    """
    Apply custom theme to the Streamlit app.
    """
    st.set_page_config(
        page_title="Disney Movies Dashboard",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Poppins:wght@400;500;600;700&display=swap');
        /* --- LAYOUT & TYPOGRAPHY --- */
        .main, [data-testid="stAppViewContainer"] {
            background-color: #fff;
            color: #23272f;
            padding: 0 2rem 2rem 2rem;
        }
        h1, h2, h3 {
            font-family: 'Poppins', sans-serif;
            color: #212121;
        }
        h1 { font-size: 2.5rem; font-weight: 700; }
        h2 { font-size: 2rem; font-weight: 600; }
        h3 { font-size: 1.75rem; font-weight: 500; }
        p, div { font-family: 'Roboto', sans-serif; color: #212121; }
        /* --- SIDEBAR --- */
        [data-testid="stSidebar"] {
            background-color: #fff;
            color: #23272f;
            padding: 0 1rem 2rem 1rem;
            border-right: 1px solid #e4e6eb;
            box-shadow: 2px 0 8px rgba(0,0,0,0.03);
        }
        [data-testid="stSidebar"] section {
            background: transparent;
            border-radius: 0;
            box-shadow: none;
            margin-bottom: 1.5rem;
            padding: 1rem;
        }
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] .st-bb {
            color: #23272f !important;
            font-size: 1.1rem;
        }
        /* --- BUTTONS --- */
        .stButton>button, [data-testid="stSidebar"] button {
            background-color: #e3eafc !important;
            color: #23272f !important;
            border-radius: 4px !important;
            border: 1px solid #b6c6e3 !important;
            font-weight: 500;
            padding: 0.5rem 1rem;
        }
        .stButton>button:hover, [data-testid="stSidebar"] button:hover {
            background-color: #b6c6e3 !important;
        }
        /* --- CHECKBOXES --- */
        [data-testid="stSidebar"] .stCheckbox > div[role="checkbox"] {
            border: 2px solid #b6c6e3 !important;
            border-radius: 4px !important;
        }
        [data-testid="stSidebar"] .stCheckbox > div[role="checkbox"][aria-checked="true"] {
            border-color: #4169e1 !important;
            background: #4169e1 !important;
        }
        [data-testid="stSidebar"] input[type="checkbox"]:checked + div > svg {
            color: #fff !important;
            background: transparent !important;
        }
        /* --- SLIDERS --- */
        [data-testid="stSidebar"] .stSlider .rc-slider-track {
            background-color: #4169e1 !important;
        }
        [data-testid="stSidebar"] .stSlider .rc-slider-handle {
            border-color: #4169e1 !important;
            background-color: #4169e1 !important;
            box-shadow: 0 0 0 2px #d1d9ec !important;
        }
        [data-testid="stSidebar"] .stSlider .rc-slider-handle:active {
            border-color: #274bb5 !important;
            background-color: #274bb5 !important;
        }
        [data-testid="stSidebar"] .stSlider .rc-slider-dot-active {
            border-color: #4169e1 !important;
        }
        [data-testid="stSidebar"] .stSlider > div[data-baseweb="slider"] > div {
            background: #fff !important;
        }
        [data-testid="stSidebar"] .stSlider span {
            color: #23272f !important;
        }
        /* --- SIDEBAR EXPAND/COLLAPSE BUTTONS --- */
        /* Collapsed sidebar expand button */
        [data-testid="stSidebar"] [data-testid="stSidebarNavCollapseButton"] {
            background-color: #f0f2f6;
            border: 1px solid #d1d9ec;
        }

        /* Full sidebar close button */
        [data-testid="stSidebar"] [data-testid="stSidebarNavCollapseButton"] button {
            background-color: transparent !important;
        }

        [data-testid="stSidebar"] [data-testid="stSidebarNavCollapseButton"] button:hover {
            background-color: #e3eafc !important;
        }
        
        /* --- SELECTBOX --- */
        [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #23272f !important;
            border: 1px solid #b6c6e3 !important;
            border-radius: 4px !important;
        }
        [data-testid="stSidebar"] [data-testid="stSelectbox"] svg {
            color: #23272f !important;
        }
        div[data-baseweb="popover"] ul {
            background-color: #FFFFFF !important;
        }
        div[data-baseweb="popover"] ul li {
            color: #23272f !important;
        }
        div[data-baseweb="popover"] ul li:hover {
            background-color: #e3eafc !important;
        }
        div[data-baseweb="popover"] ul li[aria-selected="true"] {
            background-color: #d1d9ec !important;
            color: #23272f !important;
        }
        /* --- MISC --- */
        .stMetric, .stPlotlyChart, .stDataFrame {
            background-color: #fff;
            border-radius: 0.5rem;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .success { color: #4CAF50; }
        .warning { color: #FFC107; }
        .danger { color: #F44336; }
        header[data-testid="stHeader"] { display: none !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

def get_color_palette():
    """
    Return the color palette for visualizations.
    """
    return [
        "#1f77b4",  # blue
        "#ff7f0e",  # orange
        "#2ca02c",  # green
        "#d62728",  # red
        "#9467bd",  # purple
        "#8c564b",  # brown
        "#e377c2",  # pink
        "#7f7f7f",  # gray
        "#bcbd22",  # olive
        "#17becf"   # cyan
    ]

def get_typography():
    """
    Return typography settings.
    """
    return {
        'header': 'Poppins',
        'body': 'Roboto',
        'sizes': {
            'h1': '2.5rem',
            'h2': '2rem',
            'h3': '1.75rem',
            'body': '1rem',
            'small': '0.875rem'
        }
    } 