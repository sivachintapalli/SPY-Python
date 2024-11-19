import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
from lightweight_charts import Chart

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def get_data_from_db(limit=1000):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                timestamp_market as timestamp,
                open,
                high,
                low,
                close,
                volume
            FROM minute_data
            WHERE trading_session = 'regular'
            ORDER BY timestamp_market DESC
            LIMIT %s
        """
        
        cursor.execute(query, (limit,))
        data = cursor.fetchall()
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Sort by timestamp ascending for the chart
        df = df.sort_values('timestamp')
        
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()
    
    finally:
        cursor.close()
        conn.close()

def main():
    # Create a new chart
    chart = Chart()
    
    # Get data from database
    df = get_data_from_db()
    
    if not df.empty:
        # Add candlestick series
        candlestick = chart.create_candlestick_series()
        candlestick.set_data(df)
        
        # Add volume series
        volume = chart.create_volume_series()
        volume.set_data(df)
        
        # Customize chart appearance
        chart.set(
            layout={'background': {'color': '#1e222d'},
                   'textColor': '#d9d9d9'},
            grid={'vertLines': {'color': '#2B2B43'},
                  'horzLines': {'color': '#2B2B43'}},
            crosshair={'mode': 'normal'},
            rightPriceScale={'borderColor': '#2B2B43'},
            timeScale={'borderColor': '#2B2B43',
                      'timeVisible': True,
                      'secondsVisible': False}
        )
        
        print(f"Displaying chart with {len(df)} data points...")
        # Show the chart
        chart.show(block=True)
    else:
        print("No data available from the database")

if __name__ == "__main__":
    main()
