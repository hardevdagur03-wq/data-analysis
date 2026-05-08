# Enterprise DataLens Pro

Enterprise DataLens Pro is a production-ready Data Analysis and Machine Learning platform built using Python and Streamlit. The application provides a complete end-to-end analytics workflow including data upload, preprocessing, exploratory data analysis, interactive visualizations, machine learning model building, and report generation — all within a modern enterprise-style dashboard.

---

# Live Demo

## Streamlit Deployment

[https://your-app.streamlit.app](https://data-analysis-ewnnx3aoeenph4qqf2vymf.streamlit.app/)]

---

# Features

## 1. Data Upload

Supports uploading:

- CSV files
- Excel files (.xlsx, .xls)

### Data Quality Metrics

Automatically displays:

- Number of rows
- Number of columns
- Missing values count
- Duplicate records count

---

## 2. Data Cleaning & Preprocessing

Comprehensive preprocessing utilities:

### Missing Value Handling

Users can handle missing data using:

- Mean
- Median
- Mode
- Custom values

### Additional Features

- Duplicate removal
- Data type conversion
- Feature engineering
- Column transformations
- Data filtering

---

## 3. Exploratory Data Analysis (EDA)

Automated analysis tools including:

- Descriptive statistics
- Correlation analysis
- Distribution analysis
- Histograms
- Boxplots
- Outlier detection

---

## 4. Interactive Visualizations

Interactive dashboards powered by Plotly.

### Supported Charts

- Scatter plots
- Line charts
- Bar charts
- Pie charts
- Heatmaps
- Correlation matrices

---

## 5. Machine Learning Models

Supports regression and classification workflows.

### Regression Models

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

### Regression Metrics

- R² Score
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)

### Classification Models

- Random Forest Classifier

### Classification Metrics

- Accuracy Score
- Confusion Matrix
- Classification Report

---

## 6. Reporting & Export

Generate downloadable reports and processed datasets.

### Reporting Features

- Data Quality Score
- Dataset summary
- Download cleaned datasets
- Automated analytical insights

---

# Screenshots

## Upload Dataset Page

![Upload Page](assets/screenshots/upload.png)

---

## Data Cleaning Dashboard

![Cleaning Dashboard](assets/screenshots/cleaning.png)

---

## Visualization Dashboard

![Visualization Dashboard](assets/screenshots/visualization.png)

---

## Machine Learning Models

![Machine Learning](assets/screenshots/ml.png)

---

## Reports Dashboard

![Reports Dashboard](assets/screenshots/reports.png)

---

# Technical Architecture

## Session Management

The application uses:

```python
st.session_state
```

for persistent dataset handling and activity tracking across multiple modules.

---

## Logging System

Tracks:

- User activity
- Errors and exceptions
- Application events

### Log File

```bash
datalens.log
```

---

## Performance Optimization

Efficient caching implemented using:

```python
st.cache_data
```

This improves performance and reduces redundant computations.

---

# Tech Stack

## Frontend & UI

- Streamlit
- Plotly

## Data Processing

- Pandas
- NumPy

## Machine Learning & Statistics

- Scikit-learn
- SciPy

---

# Project Structure

```bash
Enterprise-DataLens-Pro/
│
├── app1.py
├── requirements.txt
├── README.md
├── datalens.log
│
├── assets/
│   └── screenshots/
│       ├── upload.png
│       ├── cleaning.png
│       ├── visualization.png
│       ├── ml.png
│       └── reports.png
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/enterprise-datalens-pro.git
cd enterprise-datalens-pro
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Application

Execute:

```bash
streamlit run app1.py
```

The application will automatically open in your browser.

---

# Example Workflow

1. Upload CSV or Excel dataset
2. Clean and preprocess data
3. Perform exploratory data analysis
4. Create visualizations
5. Train machine learning models
6. Evaluate model performance
7. Generate reports and download processed datasets

---

# Resume Project Description

## Enterprise DataLens Pro — Data Analytics & Machine Learning Platform

Developed a production-ready analytics platform using Python and Streamlit to support complete data science workflows including data ingestion, preprocessing, exploratory analysis, interactive visualization, machine learning, and reporting. Integrated enterprise dashboard design, automated evaluation metrics, session management, caching systems, and logging mechanisms to streamline analytical operations.

---

# Key Skills Demonstrated

- Data Analysis
- Data Cleaning
- Exploratory Data Analysis (EDA)
- Data Visualization
- Machine Learning
- Dashboard Development
- Python Programming
- Streamlit Development
- Statistical Analysis
- Feature Engineering
- Model Evaluation
- Enterprise UI Design

---

# Future Enhancements

Potential future improvements:

- User authentication
- SQL database integration
- Advanced ML pipelines
- Real-time analytics
- PDF report generation
- Multi-user collaboration
- API integrations
- Automated feature selection
- Deep learning support
- Cloud scalability improvements

---

# Deployment

The application can be deployed on:

- Streamlit Community Cloud
- Render
- Railway
- AWS
- Azure
- Google Cloud Platform

---

# License

This project is licensed under the MIT License.

---

# Author

## Haradev Dagur

Data Analyst | Python Developer | Machine Learning Enthusiast

### Contact

- LinkedIn: https://www.linkedin.com/in/haradev-dagur-924760394/
- Email: hardevdagur03@gmail.com
