# Real-Time Used Car Price Estimation System

An end-to-end data engineering and machine learning project that delivers transparent, data-driven pricing guidance for used vehicles by combining historical Kaggle listings with structured storage, automated ETL, feature engineering, and predictive modeling.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Key Achievements](#key-achievements)
- [System Architecture](#system-architecture)
- [Core Features](#core-features)
- [Data Pipeline](#data-pipeline)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage Guide](#usage-guide)
- [Visual Insights](#visual-insights)
- [Modeling Roadmap](#modeling-roadmap)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## Project Overview
Car buyers and sellers often face fragmented listings or outdated price guides, leading to significant mispricing. This project builds a lightweight yet comprehensive system that ingests raw used car listings daily, stores them in a relational database, engineers interpretable features, and prepares the data for predictive price modeling. The goal is to empower stakeholders with reliable, up-to-date estimates that reflect current market conditions.

---

## Key Achievements
- Automated ingestion and processing of **4,855+** used car listings with robust cleaning, feature engineering, and storage.
- Designed a **normalized MySQL schema** with indexing for performant queries across cars, listings, and economic indicators.
- Implemented a reusable ETL workflow that prepares datasets for downstream machine learning (Random Forest and linear baselines).
- Generated interpretable visual analytics (price distributions, mileage trends, correlation heatmaps) to guide model design decisions.

---

## System Architecture

```
            ┌────────────────────┐
            │  Kaggle CSV Data   │
            └─────────┬──────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │  Data Ingestion (Python)    │
        │  • Cleans raw fields        │
        │  • Maps to schema           │
        │  • Loads into MySQL         │
        └─────────┬───────────────────┘
                  │
                  ▼
       ┌────────────────────────┐
       │  MySQL Database        │
       │  • cars                │
       │  • listings            │
       │  • economic_indicators │
       └─────────┬──────────────┘
                 │
                 ▼
   ┌─────────────────────────────┐
   │  ETL & Feature Engineering  │
   │  • Filters outliers         │
   │  • Computes vehicle_age     │
   │  • Derives mileage_rate     │
   │  • KNN imputes engine size  │
   │  • Exports cleaned dataset  │
   └─────────┬───────────────────┘
             │
             ▼
       ┌───────────────┐
       │Visualizations │
       │ & Modeling    │
       └───────────────┘
```

---

## Core Features
- **Database Infrastructure:** Creates a relational schema with referential integrity, foreign keys, and optimized indexes for analytical queries.
- **Automated Ingestion:** Cleans messy price and mileage fields, standardizes categorical values, and inserts normalized rows into the database.
- **ETL Processing:** Applies data validation, feature engineering, and missing value imputation before exporting curated datasets.
- **Exploratory Analytics:** Provides ready-to-use plots to understand price drivers and validate modeling assumptions.
- **Model-Ready Outputs:** Produces a clean CSV that can be fed into scikit-learn pipelines or deployed APIs for real-time inference.

---

## Data Pipeline
1. **Raw Data Acquisition**
   - Sources: Kaggle `used_cars.csv`, future hooks for scraped listings and economic indicators.
   - Location: `data/raw/used_cars.csv`.

2. **Database Setup**
   - Script: `database_setup.py`
   - Tasks: Creates `used_cars_db`, defines `cars`, `listings`, and `economic_indicators` tables, adds composite indexes, and enforces constraints.

3. **Data Ingestion**
   - Script: `data_ingestion.py`
   - Tasks: Cleans strings, normalizes enums, loads unique cars and listing facts into MySQL using SQLAlchemy.

4. **ETL & Feature Engineering**
   - Script: `etl_pipeline.py`
   - Tasks: Joins tables, filters outliers, computes vehicle age and mileage rate, imputes engine size via `KNNImputer`, and writes `data/processed/cleaned_cars.csv`.

5. **Visualization & Modeling**
   - Notebooks and generated plots in `visualizations/` showcase price distributions, correlations, and make popularity to inform model selection.

---

## Project Structure
```
Data_Project/
├── config.py                 # Centralized database credentials and data paths
├── database_setup.py         # Creates MySQL schema and indexes
├── data_ingestion.py         # Loads and cleans raw data into MySQL tables
├── etl_pipeline.py           # ETL pipeline with feature engineering
├── data/
│   ├── raw/used_cars.csv     # Original Kaggle dataset
│   └── processed/cleaned_cars.csv  # Model-ready dataset
├── notebooks/
│   └── eda.ipynb             # Exploratory analysis and experimentation
├── visualizations/
│   ├── correlation_matrix.png
│   ├── price_distribution.png
│   ├── price_vs_mileage.png
│   └── top_makes.png
└── Data_Project_Submission.zip  # Packaged archive for submissions
```

---

## Tech Stack
- **Languages:** Python 3.11+
- **Data Processing:** Pandas, NumPy, scikit-learn
- **Database:** MySQL (mysql-connector, SQLAlchemy)
- **Visualization:** Matplotlib, Seaborn
- **Environment:** Jupyter Notebooks, virtualenv/conda
- **Version Control:** Git, GitHub

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Jonathanpc/used-car-price-predictor.git
cd used-car-price-predictor
```

### 2. Create & Activate a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
Install the required packages:
```bash
pip install pandas numpy scikit-learn sqlalchemy mysql-connector-python matplotlib seaborn jupyter
```

### 4. Configure Database Credentials
Update `config.py` or set environment variables:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': os.getenv('DB_PASSWORD'),  # recommended
    'database': 'used_cars_db'
}
```

> **Security Tip:** Avoid hard-coding real passwords. Use environment variables or `.env` files excluded via `.gitignore`.

### 5. Initialize the Database
Ensure MySQL is running locally, then:
```bash
python database_setup.py
```

### 6. Load Raw Data into the Database
Place your Kaggle CSV under `data/raw/used_cars.csv`, then run:
```bash
python data_ingestion.py
```

### 7. Execute the ETL Pipeline
```bash
python etl_pipeline.py
```
The cleaned dataset will be saved to `data/processed/cleaned_cars.csv`.

---

## Usage Guide

### Run Exploratory Analysis
Open `notebooks/eda.ipynb` in Jupyter to explore price distributions, feature correlations, and candidate models.

### Train Models (Future Step)
- Load `data/processed/cleaned_cars.csv`.
- Split by temporal folds (70/15/15 train/validation/test).
- Compare Ridge/Lasso vs. Random Forest regressors.
- Log metrics such as MAE, RMSE, and calibration across regions.

### Serve Predictions (Planned)
- Develop a Flask or FastAPI endpoint that loads serialized models and responds with price estimates plus confidence intervals.

---

## Visual Insights
| Visualization | Purpose |
|---------------|---------|
| `price_distribution.png` | Understand price spread and detect skewness or outliers. |
| `price_vs_mileage.png` | Illustrate depreciation trends as mileage increases. |
| `correlation_matrix.png` | Identify relationships among numerical features. |
| `top_makes.png` | Highlight dataset composition by manufacturer. |

These assets live in the `visualizations/` directory and can be embedded into dashboards or reports.

---

## Modeling Roadmap
1. **Baseline Models:** Ridge and Lasso regression to capture interpretable linear relationships.
2. **Tree-Based Models:** Random Forest and Gradient Boosting for non-linear interactions (e.g., mileage thresholds).
3. **Model Management:** Serialize trained models with `joblib`, store metadata, and set up retraining triggers.
4. **Bias & Drift Monitoring:** Track MAE/RMSE by segment, monitor distribution shifts, and trigger retraining when performance degrades.

---

## Future Enhancements
- **Web Scraping:** Integrate real-time marketplace data (e.g., Craigslist, AutoTrader) using schedulers or Airflow DAGs.
- **Economic Indicators:** Pull regional income and unemployment data via open APIs and join to listings for localized adjustments.
- **API Deployment:** Expose REST endpoints with FastAPI/Flask and document via OpenAPI/Swagger.
- **Dashboard:** Build a lightweight UI (Streamlit/React) for interactive price queries and regional insights.
- **Cloud Migration:** Containerize and deploy pipelines on a managed service (e.g., AWS RDS + ECS) for scalability.

---

## License
This project is released for educational purposes.

---

**Maintainer:** Jonathan Perez Castro  
**Contact:** yeriel1322@gmail.com
