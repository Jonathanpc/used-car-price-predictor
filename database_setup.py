import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='#####'  
        )
        
        cursor = connection.cursor()
        cursor.execute("DROP DATABASE IF EXISTS used_cars_db")
        cursor.execute("CREATE DATABASE used_cars_db")
        cursor.execute("USE used_cars_db")
        
        # Create cars table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            car_id INT AUTO_INCREMENT PRIMARY KEY,
            make VARCHAR(100) NOT NULL DEFAULT 'Unknown',
            model VARCHAR(100) NOT NULL,
            year YEAR NULL,
            engine_size_cc SMALLINT NULL,
            fuel_type ENUM(
                'gasoline', 'diesel', 'hybrid', 'electric',
                'flex_fuel', 'unknown'
            ) NOT NULL DEFAULT 'unknown',
            transmission ENUM(
                'manual', 'automatic', '6_speed_at', '8_speed_automatic',
                '7_speed_at', 'unknown'
            ) NOT NULL DEFAULT 'unknown'
        )
        """)
        
        # Create listings table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            listing_id INT AUTO_INCREMENT PRIMARY KEY,
            car_id INT NOT NULL,
            location VARCHAR(100) NOT NULL DEFAULT 'Unknown',
            listing_date DATE NOT NULL,
            listed_price DECIMAL(10,2) NOT NULL,
            mileage INT NOT NULL,
            FOREIGN KEY (car_id) REFERENCES cars(car_id)
        )
        """)
        
        # Create economic indicators table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS economic_indicators (
            region VARCHAR(50) NOT NULL,
            date DATE NOT NULL,
            median_income DECIMAL(10,2),
            unemployment_rate DECIMAL(5,2),
            PRIMARY KEY (region, date)
        )
        """)
        
        # Add indexes
        cursor.execute("CREATE INDEX idx_listing_date ON listings (listing_date)")
        cursor.execute("CREATE INDEX idx_make_model ON cars (make, model)")
        
        print("Database and tables created successfully!")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database()