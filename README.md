# Disney Movies Data Dashboard

An interactive data dashboard built with Streamlit to analyze Disney's historical movie data.

## Setup Instructions

1. Create and activate the conda environment:
```bash
conda create -n disneystream python=3.11
conda activate disneystream
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run src/app.py
```

## Project Structure

```
disney-movies-app/
├── src/
│   ├── data/               # Data files
│   ├── utils/              # Utility functions
│   ├── visualizations/     # Visualization components
│   ├── styles/            # UI styling and themes
│   └── app.py             # Main application file
├── assets/                # Static assets
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## Features

- Interactive time-series analysis of box office performance
- Genre distribution and evolution over time
- MPAA rating trends
- Inflation-adjusted vs. nominal box office comparisons
- Movie performance comparisons across different eras 