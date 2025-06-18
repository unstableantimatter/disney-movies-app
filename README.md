# Disney Movies Analytics Dashboard

An interactive dashboard for analyzing the box office performance of Disney movies from 1937 to 2016. This application allows users to explore trends in revenue, genre popularity, and top-performing films through a variety of visualizations and filters.

## Features

- **Dynamic Banner**: A visually engaging banner to welcome users.
- **Interactive Filters**:
    - **Year Range Slider**: Focus on a specific period of Disney's film history.
    - **Genre Selection**: Filter movies by one or more genres.
    - **MPAA Rating Selection**: Narrow down the dataset by MPAA rating.
    - **Minimum Revenue Filter**: Exclude movies that fall below a certain revenue threshold.
- **Key Performance Indicators**: At-a-glance metrics for total movies, date range, and average/median revenue.
- **Box Office Performance Over Time**: A line chart visualizing total gross revenue year over year.
- **Genre Analysis**:
    - **Genre Distribution**: A bar chart showing the number of movies per genre.
    - **Genre by Revenue**: A bar chart comparing total revenue for each genre.
- **Genre Revenue Trend Over Time**: A multi-line chart tracking the revenue of different genres throughout the years.
- **Top & Bottom Movies**: Data tables showcasing the top and bottom 20 movies by total gross revenue.

## How to Run

1.  **Install Dependencies**:
    Make sure you have Python 3.8+ installed. Then, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the App**:
    Execute the following command in your terminal:
    ```bash
    streamlit run src/app.py
    ```

## Data Source

The data for this dashboard was sourced from the [Disney Movies Dataset on Kaggle](https://www.kaggle.com/datasets/prateekmaj21/disney-movies).

## Project Structure
```
disney-movies-app/
├── src/
│   ├── data/
│   │   └── disney_movies.csv
│   ├── images/
│   │   └── disney_dashboard.png
│   ├── styles/
│   │   └── custom_theme.py
│   ├── utils/
│   │   └── data_processor.py
│   ├── visualizations/
│   │   └── chart_configs.py
│   └── app.py
├── requirements.txt
└── README.md
``` 