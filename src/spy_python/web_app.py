"""Web Application for SPY Data Visualization"""
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from .services.data_service import DataService
from .config.logging import get_logger

logger = get_logger()

app = Flask(__name__)
data_service = DataService()

@app.route('/')
def index():
    """Render the main page with SPY chart"""
    logger.info("Rendering main page")
    return render_template('index.html')

@app.route('/api/latest-date')
def get_latest_date():
    """Get the latest available date from the database"""
    try:
        logger.info("Getting latest available date")
        latest_date, _ = data_service.get_latest_data_info()
        if not latest_date:
            logger.warning("No data available in database")
            return jsonify({'error': 'No data available'}), 404
            
        logger.info(f"Latest date: {latest_date}")
        return jsonify({'date': latest_date.isoformat()})
    except Exception as e:
        logger.error(f"Error getting latest date: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/data')
def get_data():
    """Get SPY data for the chart"""
    try:
        logger.info("Getting data for chart API endpoint")
        
        # Parse date parameter
        date_str = request.args.get('date')
        if date_str:
            try:
                selected_date = datetime.fromisoformat(date_str.split('T')[0])
                logger.debug(f"Using selected date: {selected_date}")
            except ValueError as e:
                logger.error(f"Invalid date format: {str(e)}")
                return {'error': 'Invalid date format'}, 400
        else:
            # Get latest date from database
            selected_date, _ = data_service.get_latest_data_info()
            if not selected_date:
                logger.warning("No data available in database")
                return {'error': 'No data available'}, 404

        # Get data for the selected date
        start_date = selected_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        logger.debug(f"Retrieving data from {start_date} to {end_date}")
        df = data_service.get_spy_data(start_date, end_date)
        
        if df.empty:
            logger.warning("No data found for the specified date range")
            return {'error': 'No data found'}, 404

        # Convert DataFrame to list of dictionaries for JSON serialization
        data = df.to_dict('records')
        logger.info(f"Successfully retrieved {len(data)} records")
        return {'data': data}

    except Exception as e:
        logger.error(f"Error getting data: {str(e)}", exc_info=True)
        return {'error': str(e)}, 500

def run_web_app(host='localhost', port=5000, debug=False):
    """Run the Flask web application"""
    logger.info(f"Starting web application on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
