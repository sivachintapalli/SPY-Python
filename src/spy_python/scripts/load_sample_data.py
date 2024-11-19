"""Script to load sample SPY data into the database"""
import yfinance as yf
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from ..config.database import get_session
from ..models.spy_data import SPYData
from ..config.logging import get_logger

logger = get_logger()

def load_sample_data():
    """Load sample SPY data from Yahoo Finance"""
    try:
        logger.info("Starting to load sample SPY data")
        
        # Get SPY data for the last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Download data from Yahoo Finance
        spy = yf.Ticker("SPY")
        df = spy.history(start=start_date, end=end_date, interval="1h")
        
        if df.empty:
            logger.error("No data retrieved from Yahoo Finance")
            return
            
        logger.info(f"Retrieved {len(df)} records from Yahoo Finance")
        
        # Create session
        session = get_session()
        
        try:
            # Insert data into database
            for index, row in df.iterrows():
                spy_data = SPYData(
                    date=index,
                    open=float(row['Open']),
                    high=float(row['High']),
                    low=float(row['Low']),
                    close=float(row['Close']),
                    volume=int(row['Volume'])
                )
                session.add(spy_data)
            
            session.commit()
            logger.info("Successfully loaded sample data into database")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error inserting data: {str(e)}")
            raise
            
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error loading sample data: {str(e)}")
        raise

if __name__ == "__main__":
    load_sample_data()
