"""
Main chart implementation for Lightweight Charts.
"""
from typing import Dict, Any, Optional, List, Union
import json
import uuid
from datetime import datetime

from .options import ChartOptions, CandlestickSeriesOptions, HistogramSeriesOptions
from .series import CandlestickSeries, LineSeries, HistogramSeries, OHLCData

class Chart:
    """Python wrapper for Lightweight Charts."""
    def __init__(self, container_id: str, options: Optional[ChartOptions] = None):
        self.container_id = container_id
        self.chart_id = f'chart_{uuid.uuid4().hex}'
        self.options = options or ChartOptions()
        self._series: Dict[str, Union[CandlestickSeries, LineSeries, HistogramSeries]] = {}
        self._subscriptions: Dict[str, List[str]] = {}

    def to_json(self) -> str:
        """Convert chart configuration to JSON string."""
        return json.dumps({
            'container': self.container_id,
            'options': self.options.to_dict(),
            'chart_id': self.chart_id,
        })

    def add_candlestick_series(self, 
                              options: Optional[CandlestickSeriesOptions] = None,
                              data: Optional[List[OHLCData]] = None) -> CandlestickSeries:
        """Add a candlestick series to the chart."""
        series_id = f'series_{uuid.uuid4().hex}'
        series_options = options.to_dict() if options else CandlestickSeriesOptions().to_dict()
        series = CandlestickSeries(self.chart_id, series_id, series_options)
        if data:
            series.set_data(data)
        self._series[series_id] = series
        return series

    def add_line_series(self, 
                       options: Optional[Dict[str, Any]] = None,
                       data: Optional[List[Dict[str, Union[int, float]]]] = None) -> LineSeries:
        """Add a line series to the chart."""
        series_id = f'series_{uuid.uuid4().hex}'
        series = LineSeries(self.chart_id, series_id, options or {})
        if data:
            series.set_data(data)
        self._series[series_id] = series
        return series

    def add_histogram_series(self,
                           options: Optional[HistogramSeriesOptions] = None,
                           data: Optional[List[Dict[str, Union[int, float]]]] = None) -> HistogramSeries:
        """Add a histogram series to the chart."""
        series_id = f'series_{uuid.uuid4().hex}'
        series_options = options.to_dict() if options else HistogramSeriesOptions().to_dict()
        series = HistogramSeries(self.chart_id, series_id, series_options)
        if data:
            series.set_data(data)
        self._series[series_id] = series
        return series

    def subscribe_crosshair_move(self, callback) -> str:
        """Subscribe to crosshair movement events."""
        subscription_id = f'sub_{uuid.uuid4().hex}'
        if 'crosshair_move' not in self._subscriptions:
            self._subscriptions['crosshair_move'] = []
        self._subscriptions['crosshair_move'].append(subscription_id)
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from an event."""
        for event_type, subscriptions in self._subscriptions.items():
            if subscription_id in subscriptions:
                subscriptions.remove(subscription_id)

    def set_visible_range(self, from_time: Union[datetime, str, int], 
                         to_time: Union[datetime, str, int]) -> None:
        """Set the visible time range on the chart."""
        if isinstance(from_time, datetime):
            from_time = int(from_time.timestamp())
        if isinstance(to_time, datetime):
            to_time = int(to_time.timestamp())

    def fit_content(self) -> None:
        """Fit all data into the chart's viewport."""
        pass  # This will be handled by JavaScript

    def remove_series(self, series: Union[CandlestickSeries, LineSeries, HistogramSeries]) -> None:
        """Remove a series from the chart."""
        series_id = series.series_id
        if series_id in self._series:
            del self._series[series_id]

    def apply_options(self, options: ChartOptions) -> None:
        """Apply new options to the chart."""
        self.options = options

    def take_screenshot(self) -> str:
        """Take a screenshot of the chart."""
        # This will be implemented in JavaScript
        pass

    def resize(self, width: int, height: int) -> None:
        """Resize the chart."""
        self.options.width = width
        self.options.height = height
