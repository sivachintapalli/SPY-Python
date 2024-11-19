# SPY-Python

A Python application for analyzing and visualizing SPY (S&P 500 ETF) data using TradingView-like charts with advanced technical indicators.

## Features

- **Interactive Charts**
  - Real-time OHLC candlestick display
  - Volume histogram with color-coding for bullish/bearish periods
  - Smooth navigation with crosshair and time scale controls
  - Floating legend with live data updates

- **Technical Indicators**
  - Saty Phase Oscillator for market phase analysis
  - Zone transition markers (LA, LED, LD, LEU)
  - Real-time indicator value display in legend

- **Data Management**
  - PostgreSQL database integration with SQLAlchemy ORM
  - Efficient data retrieval and caching
  - Comprehensive logging system

## Project Structure

```
SPY-Python/
├── src/
│   └── spy_python/
│       ├── config/
│       │   ├── database.py     # Database configuration
│       │   └── logging.py      # Logging configuration
│       ├── models/
│       │   └── spy_data.py     # SQLAlchemy models
│       ├── services/
│       │   ├── data_service.py # Data retrieval service
│       │   └── chart_service.py# Chart visualization service
│       ├── indicators/
│       │   └── saty_phase_oscillator.py  # Technical indicators
│       ├── static/
│       │   └── js/
│       │       └── chart.js    # Chart initialization and updates
│       ├── templates/
│       │   └── index.html      # Web interface
│       ├── __init__.py
│       └── web_app.py         # Flask application
├── logs/                      # Log files directory
├── tests/                     # Test files
├── .env                       # Environment variables
├── pyproject.toml            # Project dependencies and metadata
└── README.md                 # Project documentation
```

## Setup

1. Install Poetry (if not already installed):
```bash
pip install poetry
```

2. Install project dependencies:
```bash
poetry install
```

3. Configure your database credentials in `.env`:
```
DB_HOST=localhost
DB_NAME=spy_data
DB_USER=your_username
DB_PASSWORD=your_password
```

4. Initialize the database:
```bash
poetry run python -m spy_python.scripts.init_db
```

5. Run the application:
```bash
poetry run python -m flask --app src.spy_python.web_app run --debug
```

6. Open your browser and navigate to:
```
http://localhost:5000
```

## Technical Indicators

### Saty Phase Oscillator
The Saty Phase Oscillator is a technical indicator that helps identify different market phases:
- **Accumulation (LA)**: Price is forming a base, potential reversal point
- **Extreme Down (LED)**: Price has reached oversold conditions
- **Distribution (LD)**: Price is topping out, potential reversal point
- **Extreme Up (LEU)**: Price has reached overbought conditions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
