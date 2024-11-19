"""
Series implementations for Lightweight Charts.
"""
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class OHLCData:
    """OHLC data point."""
    time: Union[str, int, datetime]
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for JavaScript."""
        if isinstance(self.time, datetime):
            time_val = int(self.time.timestamp())
        elif isinstance(self.time, str):
            time_val = self.time
        else:
            time_val = self.time

        data = {
            'time': time_val,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
        }
        if self.volume is not None:
            data['volume'] = self.volume
        return data

class SeriesBase:
    """Base class for all series types."""
    def __init__(self, chart_id: str, series_id: str):
        self.chart_id = chart_id
        self.series_id = series_id
        self._data: List[Dict[str, Any]] = []

    def update_data(self, data: List[Dict[str, Any]]) -> None:
        """Update series data."""
        self._data = data

    def to_json(self) -> str:
        """Convert series data to JSON string."""
        return json.dumps(self._data)

class CandlestickSeries(SeriesBase):
    """Candlestick series implementation."""
    def __init__(self, chart_id: str, series_id: str, options: Dict[str, Any]):
        super().__init__(chart_id, series_id)
        self.options = options

    def set_data(self, data: List[OHLCData]) -> None:
        """Set candlestick series data."""
        self._data = [d.to_dict() for d in data]

    def update(self, data_point: OHLCData) -> None:
        """Update last candlestick or add new one."""
        self._data.append(data_point.to_dict())

class LineSeries(SeriesBase):
    """Line series implementation."""
    def __init__(self, chart_id: str, series_id: str, options: Dict[str, Any]):
        super().__init__(chart_id, series_id)
        self.options = options

    def set_data(self, data: List[Dict[str, Union[int, float]]]) -> None:
        """Set line series data."""
        self._data = data

    def update(self, time: Union[int, str], value: float) -> None:
        """Update line series with new data point."""
        self._data.append({'time': time, 'value': value})

class HistogramSeries(SeriesBase):
    """Histogram series implementation."""
    def __init__(self, chart_id: str, series_id: str, options: Dict[str, Any]):
        super().__init__(chart_id, series_id)
        self.options = options

    def set_data(self, data: List[Dict[str, Union[int, float]]]) -> None:
        """Set histogram series data."""
        self._data = data

    def update(self, time: Union[int, str], value: float, color: Optional[str] = None) -> None:
        """Update histogram series with new data point."""
        data_point = {'time': time, 'value': value}
        if color:
            data_point['color'] = color
        self._data.append(data_point)
