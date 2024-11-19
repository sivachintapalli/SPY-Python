import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from loguru import logger
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "spy_data")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "01551a0404")

def load_spy_data():
    # Create database connection
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
    
    # Download SPY data for the last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    logger.info(f"Downloading SPY data from {start_date.date()} to {end_date.date()}")
    
    # Download data from Yahoo Finance
    spy = yf.download("SPY", start=start_date, end=end_date, interval="1d")
    
    # Reset index to make Date a column
    spy.reset_index(inplace=True)
    
    # Rename columns to match our database schema
    spy.columns = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
    
    # Convert to datetime if not already
    spy['date'] = pd.to_datetime(spy['date'])
    
    logger.info(f"Downloaded {len(spy)} records")
    
    try:
        # Write to database
        spy.to_sql('stock_data', engine, if_exists='replace', index=False)
        logger.success(f"Successfully loaded {len(spy)} records into the database")
    except Exception as e:
        logger.error(f"Error loading data into database: {str(e)}")
        raise

if __name__ == "__main__":
    load_spy_data()
