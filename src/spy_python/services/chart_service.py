"""Chart Service for SPY Data Visualization"""
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
from lightweight_charts import Chart
from ..config.logging import get_logger
from ..models.spy_data import SPYData

logger = get_logger()

class ChartService:
    """Service class for handling chart operations"""

    def __init__(self):
        start_time = datetime.now()
        logger.info("Initializing ChartService")
        try:
            # Initialize chart with dark theme
            logger.debug("Creating chart instance with dark theme")
            self.chart = Chart(
                width=800,
                height=600,
                title='SPY Chart',
                maximize=False,
                debug=False
            )
            
            # Configure chart appearance
            logger.debug("Configuring chart layout")
            self.chart.layout(
                background_color='#1e222d',
                text_color='#d9d9d9',
                font_size=12,
                font_family='Courier New'
            )
            
            logger.debug("Configuring chart grid")
            self.chart.grid(
                vert_enabled=True,
                horz_enabled=True,
                color='rgba(43, 43, 67, 0.5)'
            )
            
            logger.debug("Configuring time scale")
            self.chart.time_scale(
                visible=True,
                time_visible=True,
                seconds_visible=False,
                border_visible=True,
                border_color='#2B2B43'
            )
            
            logger.debug("Configuring crosshair")
            self.chart.crosshair(
                mode='normal',
                vert_visible=True,
                horz_visible=True,
                vert_label_background_color='#2B2B43',
                horz_label_background_color='#2B2B43'
            )
            
            logger.debug("Configuring legend")
            self.chart.legend(
                visible=True,
                ohlc=True,
                percent=True,
                lines=True,
                color='#d9d9d9',
                font_size=11,
                font_family='Courier New'
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"ChartService initialized successfully in {duration:.2f} seconds")

        except Exception as e:
            logger.error(f"Error initializing chart: {str(e)}", exc_info=True)
            raise

    def display_chart(self, data: List[SPYData]):
        """
        Display SPY data chart
        
        Args:
            data: List of SPYData objects
        """
        try:
            start_time = datetime.now()
            logger.info("Starting chart display process")
            logger.debug(f"Input data count: {len(data)}")

            if not data:
                logger.warning("No data available to display")
                return

            # Convert data to OHLC format
            logger.debug("Converting data to OHLC format")
            ohlc_data = SPYData.format_ohlc_list(data)

            # Add candlestick series
            logger.debug("Adding candlestick series")
            candlestick_series = self.chart.candlestick_series(
                title='SPY',
                up_color='#26a69a',
                down_color='#ef5350',
                border_up_color='#26a69a',
                border_down_color='#ef5350',
                wick_up_color='#26a69a',
                wick_down_color='#ef5350'
            )
            candlestick_series.set_data(ohlc_data)

            # Add volume series
            logger.debug("Adding volume series")
            volume_series = self.chart.volume_series(
                title='Volume',
                up_color='rgba(38, 166, 154, 0.5)',
                down_color='rgba(239, 83, 80, 0.5)'
            )
            volume_data = [
                {
                    'time': item['time'],
                    'value': item['volume'],
                    'color': 'rgba(38, 166, 154, 0.5)' if item['close'] >= item['open'] else 'rgba(239, 83, 80, 0.5)'
                }
                for item in ohlc_data
            ]
            volume_series.set_data(volume_data)

            # Add oscillator series
            logger.debug("Adding oscillator series")
            oscillator_series = self.chart.line_series(
                title='Oscillator',
                color='rgba(255, 255, 255, 0.5)'
            )
            oscillator_data = [
                {
                    'time': item['time'],
                    'value': item['oscillator']
                }
                for item in ohlc_data
            ]
            oscillator_series.set_data(oscillator_data)

            # Add markers for zone transitions
            logger.debug("Adding markers for zone transitions")
            for item in ohlc_data:
                if item['leaving_accumulation']:
                    self.chart.create_marker(
                        time=item['time'],
                        position='belowBar',
                        color='#2196F3',
                        shape='arrowUp',
                        text='LA'
                    )
                if item['leaving_extreme_down']:
                    self.chart.create_marker(
                        time=item['time'],
                        position='belowBar',
                        color='#4CAF50',
                        shape='arrowUp',
                        text='LED'
                    )
                if item['leaving_distribution']:
                    self.chart.create_marker(
                        time=item['time'],
                        position='aboveBar',
                        color='#FFC107',
                        shape='arrowDown',
                        text='LD'
                    )
                if item['leaving_extreme_up']:
                    self.chart.create_marker(
                        time=item['time'],
                        position='aboveBar',
                        color='#FF5252',
                        shape='arrowDown',
                        text='LEU'
                    )

            # Set up legend update on crosshair move
            def update_legend(param: Dict[str, Any]):
                if param and 'time' in param:
                    data_point = next((d for d in data if int(d.timestamp.timestamp()) == param['time']), None)
                    if data_point:
                        is_up = data_point.is_bullish
                        color = '#26a69a' if is_up else '#ef5350'
                        self.chart.update_legend({
                            'ohlc': {
                                'open': data_point.format_price(data_point.open),
                                'high': data_point.format_price(data_point.high),
                                'low': data_point.format_price(data_point.low),
                                'close': data_point.format_price(data_point.close),
                                'color': color
                            },
                            'volume': data_point.format_volume(),
                            'change': f"{data_point.price_change_percent:+.2f}%"
                        })

            self.chart.subscribe_crosshair_move(update_legend)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"Chart display completed in {duration:.2f} seconds")

        except Exception as e:
            logger.error(f"Error displaying chart: {str(e)}", exc_info=True)
            raise

    def resize(self, width: int, height: int):
        """Resize the chart"""
        try:
            logger.debug(f"Resizing chart to {width}x{height}")
            self.chart.resize(width, height)
        except Exception as e:
            logger.error(f"Error resizing chart: {str(e)}", exc_info=True)
            raise

    def set_visible_range(self, from_time: datetime, to_time: datetime):
        """Set the visible time range on the chart"""
        try:
            logger.debug(f"Setting visible range from {from_time} to {to_time}")
            self.chart.set_visible_range(
                from_time=int(from_time.timestamp()),
                to_time=int(to_time.timestamp())
            )
        except Exception as e:
            logger.error(f"Error setting visible range: {str(e)}", exc_info=True)
            raise
