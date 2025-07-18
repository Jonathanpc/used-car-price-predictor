import pandas as pd
import os
import re
from datetime import datetime
from config import DB_CONFIG, DATA_PATHS
from sqlalchemy import create_engine

def clean_mileage(value):
    """Convert mileage strings to integers"""
    if pd.isna(value):
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        cleaned = re.sub(r'[^\d]', '', value)
        return int(cleaned) if cleaned else 0
    return 0

def clean_price(value):
    """Convert price strings to floats"""
    if pd.isna(value):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = re.sub(r'[^\d.]', '', value)
        return float(cleaned) if cleaned else 0.0
    return 0.0

def ingest_kaggle_data():
    # Load Kaggle dataset
    file_path = DATA_PATHS['kaggle']
    print(f"Reading file from: {os.path.abspath(file_path)}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    # Read CSV without dtype specification
    df = pd.read_csv(file_path)
    print("Original columns:", df.columns.tolist())
    
    # Debug: Show model values
    print("\nOriginal model values:")
    print(df['model'].unique()[:10])
    print(f"Max model length: {df['model'].str.len().max()}")
    
    # Map columns to our schema
    column_mapping = {
        'brand': 'make',
        'model': 'model',
        'model_year': 'year',
        'milage': 'mileage',
        'fuel_type': 'fuel_type',
        'transmission': 'transmission',
        'price': 'listed_price'
    }
    df.rename(columns=column_mapping, inplace=True)
    
    # Clean and convert columns
    if 'mileage' in df:
        print("Cleaning mileage column...")
        df['mileage'] = df['mileage'].apply(clean_mileage)
    
    if 'listed_price' in df:
        print("Cleaning price column...")
        df['listed_price'] = df['listed_price'].apply(clean_price)
    
    # Create database connection
    engine = create_engine(
        f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
    )
    
    # Prepare cars data
    cars_df = df[['make', 'model', 'year', 'fuel_type', 'transmission']].copy()
    
    # Handle missing values
    cars_df['year'] = cars_df['year'].fillna(0).astype(int)
    cars_df['make'] = cars_df['make'].fillna('Unknown')
    cars_df['fuel_type'] = cars_df['fuel_type'].fillna('Unknown')
    cars_df['transmission'] = cars_df['transmission'].fillna('Unknown')
    
    # Clean transmission values
    transmission_mapping = {
        '6-Speed A/T': '6_speed_at',
        '8-Speed Automatic': '8_speed_automatic',
        '7-Speed A/T': '7_speed_at',
        'Automatic': 'automatic',
        'A/T': 'automatic',
        'Manual': 'manual',
        'F': 'unknown'
    }
    cars_df['transmission'] = cars_df['transmission'].map(
        lambda x: transmission_mapping.get(x, 'unknown')
    )
    
    # Clean fuel_type values
    fuel_mapping = {
        'E85 Flex Fuel': 'flex_fuel',
        'Gasoline': 'gasoline',
        'Hybrid': 'hybrid',
        'Diesel': 'diesel',
        'Electric': 'electric'
    }
    cars_df['fuel_type'] = cars_df['fuel_type'].map(
        lambda x: fuel_mapping.get(x, 'unknown')
    )
    
    # Debug: Show processed model values
    print("\nProcessed model values:")
    print(cars_df['model'].unique()[:10])
    print(f"Max model length: {cars_df['model'].str.len().max()}")
    
    # Truncate long model names
    long_models = cars_df[cars_df['model'].str.len() > 100]
    if not long_models.empty:
        print("\nWARNING: Long model names detected:")
        print(long_models[['make', 'model']].head())
        print("Truncating to 100 characters...")
        cars_df['model'] = cars_df['model'].str.slice(0, 100)
    
    # Add dummy engine_size_cc
    cars_df['engine_size_cc'] = 0
    
    # Drop duplicates
    cars_df = cars_df.drop_duplicates()
    
    # Print sample data
    print("\nSample cars data:")
    print(cars_df.head())
    
    # Ingest cars data
    cars_df.to_sql('cars', engine, if_exists='append', index=False)
    print(f"Inserted {len(cars_df)} records into cars table")
    
    # Get car IDs
    with engine.connect() as conn:
        cars_db = pd.read_sql("SELECT car_id, make, model, year FROM cars", conn)
    
    # Merge to get car IDs
    merged = pd.merge(
        df, 
        cars_db,
        on=['make', 'model', 'year'],
        how='left'
    )
    
    # Prepare listings data
    listings_df = merged[['car_id', 'listed_price', 'mileage']].copy()
    
    # Add required fields with dummy values
    listings_df['location'] = 'Unknown'
    listings_df['listing_date'] = datetime.today().date()
    
    # Reorder columns
    listings_df = listings_df[['car_id', 'location', 'listing_date', 'listed_price', 'mileage']]
    
    # Print sample listings
    print("\nSample listings data:")
    print(listings_df.head())
    
    # Ingest listings
    listings_df.to_sql('listings', engine, if_exists='append', index=False)
    print(f"Inserted {len(listings_df)} records into listings table")
    
    print("Data ingestion complete!")

if __name__ == "__main__":
    ingest_kaggle_data()