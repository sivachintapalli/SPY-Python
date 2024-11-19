"""Data Service for SPY Data"""
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ..models.spy_data import SPYData
from ..config.database import engine
from ..config.logging import get_logger
from ..indicators.saty_phase_oscillator import SatyPhaseOscillator

logger = get_logger()

class DataService:
    """Service class for handling data operations"""

    def __init__(self):
        self.engine = engine
        self.oscillator = SatyPhaseOscillator()

    def get_latest_date(self) -> datetime:
        """Get the latest date from the database"""
        try:
            with Session(self.engine) as session:
                result = session.execute(
                    select(func.max(SPYData.timestamp))
                ).scalar()
                return result or datetime.now()
        except Exception as e:
            logger.error(f"Error getting latest date: {str(e)}", exc_info=True)
            raise

    def get_data_for_date(self, date: datetime) -> dict:
        """
        Get data for a specific date
        
        Args:
            date: Date to get data for
            
        Returns:
            Dictionary containing candlestick and oscillator data
        """
        try:
            start_time = datetime.now()
            logger.info(f"Fetching data for date: {date}")

            # Get data from database
            with Session(self.engine) as session:
                query = select(SPYData).where(
                    SPYData.timestamp >= date.replace(hour=0, minute=0, second=0),
                    SPYData.timestamp < (date + timedelta(days=1)).replace(hour=0, minute=0, second=0)
                ).order_by(SPYData.timestamp)
                
                result = session.execute(query)
                data = result.scalars().all()

            if not data:
                logger.warning(f"No data found for date: {date}")
                return {'candlesticks': [], 'volume': [], 'oscillator': []}

            # Convert to DataFrame for calculations
            df = pd.DataFrame([{
                'timestamp': d.timestamp,
                'open': float(d.open),
                'high': float(d.high),
                'low': float(d.low),
                'close': float(d.close),
                'volume': d.volume
            } for d in data])

            # Calculate oscillator values
            oscillator_data = self.oscillator.calculate(df)

            # Prepare response data
            response_data = []
            for i, row in df.iterrows():
                time = int(row['timestamp'].timestamp())
                item = {
                    'time': time,
                    'open': row['open'],
                    'high': row['high'],
                    'low': row['low'],
                    'close': row['close'],
                    'volume': row['volume'],
                    'oscillator': oscillator_data['oscillator'][i],
                    'compression': oscillator_data['compression_tracker'][i],
                    'color': oscillator_data['colors'][i],
                    'leaving_accumulation': oscillator_data['signals']['leaving_accumulation'][i],
                    'leaving_extreme_down': oscillator_data['signals']['leaving_extreme_down'][i],
                    'leaving_distribution': oscillator_data['signals']['leaving_distribution'][i],
                    'leaving_extreme_up': oscillator_data['signals']['leaving_extreme_up'][i]
                }
                response_data.append(item)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"Data fetched successfully in {duration:.2f} seconds")

            return response_data

        except Exception as e:
            logger.error(f"Error fetching data: {str(e)}", exc_info=True)
            raise
