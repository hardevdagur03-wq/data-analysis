"""
ENTERPRISE DATALENS PRO
Single File Production-Ready Streamlit App

Run:
streamlit run app.py
"""

# =============================================================================
# IMPORTS
# =============================================================================

import io
import logging
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

warnings.filterwarnings("ignore")

# =============================================================================
# LOGGING
# =============================================================================

logging.basicConfig(
    filename="datalens.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Enterprise DataLens Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.stButton>button {
    width: 100%;
    border-radius: 8px;
    height: 3em;
    background-color: #1f77b4;
    color: white;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #0b5ed7;
}

.metric-box {
    background: #161B22;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #00d4ff;
}

.metric-label {
    font-size: 12px;
    color: #999;
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE
# =============================================================================

if "df" not in st.session_state:
    st.session_state.df = None

if "history" not in st.session_state:
    st.session_state.history = []

# =============================================================================
# UTILITIES
# =============================================================================

def log_action(action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.history.append(f"{timestamp} - {action}")
    logger.info(action)


def numeric_columns(df):
    return df.select_dtypes(include=np.number).columns.tolist()


def categorical_columns(df):
    return df.select_dtypes(include=["object", "category"]).columns.tolist()


def metric_card(value, label):
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.title("📊 Enterprise DataLens")

page = st.sidebar.radio(
    "Navigation",
    [
        "Upload Data",
        "Data Cleaning",
        "Data Analysis",
        "Visualizations",
        "ML Models",
        "Reports",
    ],
)

# =============================================================================
# UPLOAD PAGE
# =============================================================================

if page == "Upload Data":

    st.title("📂 Upload Dataset")

    uploaded = st.file_uploader(
        "Upload CSV or Excel File",
        type=["csv", "xlsx", "xls"],
    )

    if uploaded:

        try:

            if uploaded.name.endswith(".csv"):
                df = load_csv(uploaded)

            else:
                df = pd.read_excel(uploaded)

            st.session_state.df = df

            log_action(f"Dataset uploaded: {uploaded.name}")

            st.success("Dataset loaded successfully")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                metric_card(df.shape[0], "Rows")

            with col2:
                metric_card(df.shape[1], "Columns")

            with col3:
                metric_card(df.isnull().sum().sum(), "Missing")

            with col4:
                metric_card(df.duplicated().sum(), "Duplicates")

            st.dataframe(df.head(), use_container_width=True)

        except Exception as e:
            logger.exception(str(e))
            st.error(str(e))

# =============================================================================
# DATA CLEANING
# =============================================================================

elif page == "Data Cleaning":

    st.title("🧹 Data Cleaning")

    if st.session_state.df is None:
        st.warning("Upload dataset first")
        st.stop()

    df = st.session_state.df.copy()

    tab1, tab2, tab3, tab4 = st.tabs([
        "Missing Values",
        "Duplicates",
        "Data Types",
        "Feature Engineering",
    ])

    # =========================================================================
    # MISSING VALUES
    # =========================================================================

    with tab1:

        st.subheader("Handle Missing Values")

        strategy = st.selectbox(
            "Strategy",
            [
                "Remove Missing Rows",
                "Fill Mean",
                "Fill Median",
                "Fill Mode",
                "Custom Value",
            ],
        )

        columns = st.multiselect(
            "Select Columns",
            df.columns.tolist(),
            default=df.columns.tolist(),
        )

        custom_value = None

        if strategy == "Custom Value":
            custom_value = st.text_input("Enter Value")

        if st.button("Apply Missing Value Operation"):

            try:

                if strategy == "Remove Missing Rows":
                    df = df.dropna()

                elif strategy == "Fill Mean":

                    for col in columns:

                        if col in numeric_columns(df):
                            df[col] = df[col].fillna(df[col].mean())

                elif strategy == "Fill Median":

                    for col in columns:

                        if col in numeric_columns(df):
                            df[col] = df[col].fillna(df[col].median())

                elif strategy == "Fill Mode":

                    for col in columns:
                        df[col] = df[col].fillna(df[col].mode()[0])

                elif strategy == "Custom Value":
                    df[columns] = df[columns].fillna(custom_value)

                st.session_state.df = df

                log_action(f"Missing value strategy applied: {strategy}")

                st.success("Operation completed")

            except Exception as e:
                logger.exception(str(e))
                st.error(str(e))

    # =========================================================================
    # DUPLICATES
    # =========================================================================

    with tab2:

        st.subheader("Duplicate Rows")

        duplicates = df.duplicated().sum()

        st.info(f"Duplicate rows found: {duplicates}")

        if st.button("Remove Duplicates"):

            df = df.drop_duplicates()

            st.session_state.df = df

            log_action("Duplicates removed")

            st.success("Duplicates removed successfully")

    # =========================================================================
    # DATA TYPES
    # =========================================================================

    with tab3:

        st.subheader("Column Type Conversion")

        column = st.selectbox("Select Column", df.columns)

        dtype = st.selectbox(
            "Convert To",
            [
                "int",
                "float",
                "string",
                "datetime",
            ],
        )

        if st.button("Convert Type"):

            try:

                if dtype == "int":
                    df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")

                elif dtype == "float":
                    df[column] = pd.to_numeric(df[column], errors="coerce")

                elif dtype == "string":
                    df[column] = df[column].astype(str)

                elif dtype == "datetime":
                    df[column] = pd.to_datetime(df[column], errors="coerce")

                st.session_state.df = df

                log_action(f"Converted {column} to {dtype}")

                st.success("Conversion successful")

            except Exception as e:
                logger.exception(str(e))
                st.error(str(e))

    # =========================================================================
    # FEATURE ENGINEERING
    # =========================================================================

    with tab4:

        st.subheader("Create Features")

        num_cols = numeric_columns(df)

        if len(num_cols) >= 2:

            col1 = st.selectbox("Column A", num_cols)

            operation = st.selectbox(
                "Operation",
                ["+", "-", "*", "/", "log", "sqrt"],
            )

            col2 = st.selectbox("Column B", num_cols)

            new_col = st.text_input("New Column Name", "new_feature")

            if st.button("Create Feature"):

                try:

                    if operation == "+":
                        df[new_col] = df[col1] + df[col2]

                    elif operation == "-":
                        df[new_col] = df[col1] - df[col2]

                    elif operation == "*":
                        df[new_col] = df[col1] * df[col2]

                    elif operation == "/":
                        df[new_col] = df[col1] / df[col2]

                    elif operation == "log":
                        df[new_col] = np.log1p(df[col1])

                    elif operation == "sqrt":
                        df[new_col] = np.sqrt(df[col1])

                    st.session_state.df = df

                    log_action(f"Feature created: {new_col}")

                    st.success("Feature created")

                except Exception as e:
                    logger.exception(str(e))
                    st.error(str(e))

    st.dataframe(df, use_container_width=True)

# =============================================================================
# DATA ANALYSIS
# =============================================================================

elif page == "Data Analysis":

    st.title("📈 Data Analysis")

    if st.session_state.df is None:
        st.warning("Upload dataset first")
        st.stop()

    df = st.session_state.df

    st.subheader("Dataset Summary")

    st.dataframe(df.describe(include="all").T)

    num_cols = numeric_columns(df)

    if len(num_cols) > 0:

        column = st.selectbox("Select Numeric Column", num_cols)

        fig = px.histogram(
            df,
            x=column,
            nbins=30,
            title=f"Distribution of {column}",
        )

        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.box(
            df,
            y=column,
            title=f"Boxplot of {column}",
        )

        st.plotly_chart(fig2, use_container_width=True)

# =============================================================================
# VISUALIZATION
# =============================================================================

elif page == "Visualizations":

    st.title("📊 Visualizations")

    if st.session_state.df is None:
        st.warning("Upload dataset first")
        st.stop()

    df = st.session_state.df

    num_cols = numeric_columns(df)
    cat_cols = categorical_columns(df)

    chart = st.selectbox(
        "Chart Type",
        [
            "Scatter",
            "Line",
            "Bar",
            "Pie",
            "Heatmap",
        ],
    )

    if chart == "Scatter":

        x = st.selectbox("X", num_cols)

        y = st.selectbox(
            "Y",
            [c for c in num_cols if c != x],
        )

        fig = px.scatter(df, x=x, y=y)

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Line":

        x = st.selectbox("X", df.columns)

        y = st.selectbox("Y", num_cols)

        fig = px.line(df, x=x, y=y)

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Bar":

        x = st.selectbox("Category", cat_cols)

        y = st.selectbox("Value", num_cols)

        grouped = df.groupby(x)[y].mean().reset_index()

        fig = px.bar(grouped, x=x, y=y)

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Pie":

        names = st.selectbox("Names", cat_cols)

        values = st.selectbox("Values", num_cols)

        grouped = df.groupby(names)[values].sum().reset_index()

        fig = px.pie(grouped, names=names, values=values)

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Heatmap":

        corr = df[num_cols].corr()

        fig = px.imshow(corr, text_auto=True)

        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# ML MODELS
# =============================================================================

elif page == "ML Models":

    st.title("🤖 Machine Learning")

    if st.session_state.df is None:
        st.warning("Upload dataset first")
        st.stop()

    df = st.session_state.df

    num_cols = numeric_columns(df)

    tab1, tab2 = st.tabs(["Regression", "Classification"])

    # =========================================================================
    # REGRESSION
    # =========================================================================

    with tab1:

        if len(num_cols) >= 2:

            target = st.selectbox("Target", num_cols)

            features = st.multiselect(
                "Features",
                [c for c in num_cols if c != target],
            )

            model_name = st.selectbox(
                "Model",
                [
                    "Linear Regression",
                    "Random Forest",
                    "Gradient Boosting",
                ],
            )

            if st.button("Train Regression Model"):

                try:

                    data = df[features + [target]].dropna()

                    X = data[features]
                    y = data[target]

                    X_train, X_test, y_train, y_test = train_test_split(
                        X,
                        y,
                        test_size=0.2,
                        random_state=42,
                    )

                    scaler = StandardScaler()

                    X_train = scaler.fit_transform(X_train)
                    X_test = scaler.transform(X_test)

                    if model_name == "Linear Regression":
                        model = LinearRegression()

                    elif model_name == "Random Forest":
                        model = RandomForestRegressor()

                    else:
                        model = GradientBoostingRegressor()

                    model.fit(X_train, y_train)

                    preds = model.predict(X_test)

                    r2 = r2_score(y_test, preds)

                    mae = mean_absolute_error(y_test, preds)

                    rmse = np.sqrt(mean_squared_error(y_test, preds))

                    c1, c2, c3 = st.columns(3)

                    with c1:
                        metric_card(round(r2, 4), "R²")

                    with c2:
                        metric_card(round(mae, 4), "MAE")

                    with c3:
                        metric_card(round(rmse, 4), "RMSE")

                    fig = px.scatter(
                        x=y_test,
                        y=preds,
                        labels={"x": "Actual", "y": "Predicted"},
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    log_action(f"Regression model trained: {model_name}")

                except Exception as e:
                    logger.exception(str(e))
                    st.error(str(e))

    # =========================================================================
    # CLASSIFICATION
    # =========================================================================

    with tab2:

        all_cols = df.columns.tolist()

        target = st.selectbox("Classification Target", all_cols)

        features = st.multiselect(
            "Classification Features",
            [c for c in num_cols if c != target],
        )

        if st.button("Train Classification Model"):

            try:

                data = df[features + [target]].dropna()

                X = data[features]

                le = LabelEncoder()

                y = le.fit_transform(data[target].astype(str))

                X_train, X_test, y_train, y_test = train_test_split(
                    X,
                    y,
                    test_size=0.2,
                    random_state=42,
                )

                scaler = StandardScaler()

                X_train = scaler.fit_transform(X_train)
                X_test = scaler.transform(X_test)

                model = RandomForestClassifier()

                model.fit(X_train, y_train)

                preds = model.predict(X_test)

                acc = accuracy_score(y_test, preds)

                metric_card(round(acc * 100, 2), "Accuracy %")

                cm = confusion_matrix(y_test, preds)

                fig = px.imshow(cm, text_auto=True)

                st.plotly_chart(fig, use_container_width=True)

                report = classification_report(
                    y_test,
                    preds,
                    output_dict=True,
                )

                st.dataframe(pd.DataFrame(report).T)

                log_action("Classification model trained")

            except Exception as e:
                logger.exception(str(e))
                st.error(str(e))

# =============================================================================
# REPORTS
# =============================================================================

elif page == "Reports":

    st.title("📋 Reports")

    if st.session_state.df is None:
        st.warning("Upload dataset first")
        st.stop()

    df = st.session_state.df

    st.subheader("Data Quality Report")

    missing = df.isnull().sum().sum()

    duplicates = df.duplicated().sum()

    quality = max(
        0,
        100 - ((missing / df.size) * 100) - ((duplicates / len(df)) * 100),
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card(round(quality, 2), "Quality Score")

    with c2:
        metric_card(missing, "Missing Values")

    with c3:
        metric_card(duplicates, "Duplicates")

    st.subheader("Column Report")

    report = pd.DataFrame({
        "Column": df.columns,
        "Dtype": df.dtypes.astype(str),
        "Missing": df.isnull().sum(),
        "Unique": df.nunique(),
    })

    st.dataframe(report, use_container_width=True)

    st.download_button(
        "Download CSV",
        df.to_csv(index=False).encode(),
        "cleaned_data.csv",
        "text/csv",
    )

    st.subheader("Activity Logs")

    for item in st.session_state.history:
        st.write(item)