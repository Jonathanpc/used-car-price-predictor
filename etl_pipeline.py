import pandas as pd
import numpy as np
import os
from config import DB_CONFIG, DATA_PATHS
from sqlalchemy import create_engine
from sklearn.impute import KNNImputer

def run_etl():
    # Database connection
    engine = create_engine(
        f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
    )
    
    # Load data from database
    query = """
    SELECT c.car_id, c.make, c.model, c.year, c.engine_size_cc, c.fuel_type, c.transmission,
           l.listing_id, l.location, l.listing_date, l.listed_price, l.mileage
    FROM cars c
    JOIN listings l ON c.car_id = l.car_id
    """
    df = pd.read_sql(query, engine)
    print(f"Loaded {len(df)} records from database")
    
    # Data cleaning
    # Remove unrealistic mileage
    df = df[df['mileage'] <= 500000]
    print(f"After mileage filter: {len(df)} records")
    
    # Remove unrealistic prices
    df = df[df['listed_price'] > 500]
    print(f"After price filter: {len(df)} records")
    
    # Feature engineering
    current_year = pd.Timestamp.now().year
    df['vehicle_age'] = current_year - df['year']
    
    # Avoid division by zero for vehicle_age
    df.loc[df['vehicle_age'] == 0, 'vehicle_age'] = 1
    df['mileage_rate'] = df['mileage'] / df['vehicle_age']
    
    # Handle missing engine sizes (KNN imputation)
    if 'engine_size_cc' in df.columns:
        print("Imputing missing engine sizes...")
        imputer = KNNImputer(n_neighbors=5)
        df['engine_size_cc'] = imputer.fit_transform(df[['engine_size_cc']])
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(DATA_PATHS['output'])
    os.makedirs(output_dir, exist_ok=True)
    
    # Save cleaned data
    df.to_csv(DATA_PATHS['output'], index=False)
    print(f"Cleaned data saved to {DATA_PATHS['output']}")
    print(f"Final record count: {len(df)}")

if __name__ == "__main__":
    run_etl()