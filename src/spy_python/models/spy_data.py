"""SPY Data Models"""
from datetime import datetime
from typing import Dict, Any, List
from decimal import Decimal
from sqlalchemy import Column, Integer, Numeric, DateTime, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SPYData(Base):
    """SPY Data Model representing the stock_data table"""
    __tablename__ = 'stock_data'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    open = Column(Numeric, nullable=False)
    high = Column(Numeric, nullable=False)
    low = Column(Numeric, nullable=False)
    close = Column(Numeric, nullable=False)
    volume = Column(BigInteger, nullable=False)
    market_type = Column(String, nullable=True)
    long = Column(Numeric, nullable=True)
    short = Column(Numeric, nullable=True)
    long_close = Column(Numeric, nullable=True)
    short_close = Column(Numeric, nullable=True)
    profit = Column(Numeric, nullable=True)
    running_profit = Column(Numeric, nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary format."""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'timestamp': self.timestamp,
            'open': float(self.open) if self.open else None,
            'high': float(self.high) if self.high else None,
            'low': float(self.low) if self.low else None,
            'close': float(self.close) if self.close else None,
            'volume': self.volume,
            'market_type': self.market_type,
            'long': float(self.long) if self.long else None,
            'short': float(self.short) if self.short else None,
            'long_close': float(self.long_close) if self.long_close else None,
            'short_close': float(self.short_close) if self.short_close else None,
            'profit': float(self.profit) if self.profit else None,
            'running_profit': float(self.running_profit) if self.running_profit else None,
        }

    def to_ohlc(self) -> Dict[str, Any]:
        """Convert to OHLC format for chart display."""
        return {
            'time': int(self.timestamp.timestamp()),
            'open': float(self.open) if self.open else None,
            'high': float(self.high) if self.high else None,
            'low': float(self.low) if self.low else None,
            'close': float(self.close) if self.close else None,
            'volume': self.volume,
        }

    @staticmethod
    def format_ohlc_list(data_list: List['SPYData']) -> List[Dict[str, Any]]:
        """Convert a list of SPYData objects to OHLC format."""
        return [item.to_ohlc() for item in data_list]

    @property
    def is_bullish(self) -> bool:
        """Check if the candle is bullish (close >= open)."""
        return float(self.close) >= float(self.open) if self.close and self.open else False

    @property
    def price_change(self) -> float:
        """Calculate price change from open to close."""
        if self.open and self.close:
            return float(self.close) - float(self.open)
        return 0.0

    @property
    def price_change_percent(self) -> float:
        """Calculate percentage price change from open to close."""
        if self.open and self.close and float(self.open) != 0:
            return (float(self.close) - float(self.open)) / float(self.open) * 100
        return 0.0

    def format_price(self, price: Decimal) -> str:
        """Format price with 2 decimal places."""
        return f"{float(price):.2f}" if price else "-"

    def format_volume(self) -> str:
        """Format volume with K/M suffix."""
        if not self.volume:
            return "-"
        volume = self.volume
        if volume >= 1_000_000:
            return f"{volume/1_000_000:.2f}M"
        if volume >= 1_000:
            return f"{volume/1_000:.2f}K"
        return str(volume)
