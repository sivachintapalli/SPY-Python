"""Main application module"""
from datetime import datetime, timedelta
from .services.data_service import DataService
from .services.chart_service import ChartService
from .config.logging import get_logger

logger = get_logger()

def main():
    """Main application entry point"""
    try:
        logger.info("Starting SPY Python application")
        
        # Initialize services
        data_service = DataService()
        chart_service = ChartService()
        
        # Get latest data info
        latest_date, total_records = data_service.get_latest_data_info()
        
        if not latest_date:
            logger.error("No data available in the database")
            return
        
        # Get data for the latest day
        start_date = latest_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        logger.info(f"Retrieving data for {start_date.date()}")
        data = data_service.get_spy_data(start_date=start_date, end_date=end_date)
        
        if data.empty:
            logger.error("No data available for the specified date")
            return
        
        # Display chart
        chart_service.display_chart(data)
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        
if __name__ == "__main__":
    main()
