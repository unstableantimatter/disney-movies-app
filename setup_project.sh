#!/bin/bash

# Create main project directories
mkdir -p src/data
mkdir -p src/utils
mkdir -p src/visualizations
mkdir -p src/styles
mkdir -p assets

# Create necessary Python files
touch src/__init__.py
touch src/utils/__init__.py
touch src/visualizations/__init__.py
touch src/styles/__init__.py

# Create main application file
touch src/app.py

# Create utility files
touch src/utils/data_processor.py
touch src/utils/theme_config.py

# Create visualization files
touch src/visualizations/box_office.py
touch src/visualizations/genre_analysis.py
touch src/visualizations/rating_trends.py

# Create style configuration
touch src/styles/custom_theme.py

# Move the CSV file to the data directory
mv disney_movies.csv src/data/

echo "Project structure created successfully!" 