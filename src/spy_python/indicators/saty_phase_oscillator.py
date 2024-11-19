"""
Saty Phase Oscillator Implementation
Original by Saty Mahajan, converted to Python
"""
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any

class SatyPhaseOscillator:
    """Implementation of Saty Phase Oscillator indicator."""

    def __init__(self):
        self.colors = {
            'green': '#00ff00',
            'red': '#ff0000',
            'magenta': '#ff00ff',
            'light_gray': '#c8c8c8',
            'gray': '#969696',
            'dark_gray': '#646464',
            'yellow': '#ffff00'
        }

    def calculate_ema(self, data: np.ndarray, period: int) -> np.ndarray:
        """Calculate Exponential Moving Average."""
        alpha = 2 / (period + 1)
        return pd.Series(data).ewm(alpha=alpha, adjust=False).mean().values

    def calculate_stdev(self, data: np.ndarray, period: int) -> np.ndarray:
        """Calculate Standard Deviation."""
        return pd.Series(data).rolling(window=period).std().values

    def calculate_atr(self, high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int) -> np.ndarray:
        """Calculate Average True Range."""
        tr = np.maximum(high - low, 
                       np.maximum(
                           np.abs(high - np.roll(close, 1)),
                           np.abs(low - np.roll(close, 1))
                       ))
        return pd.Series(tr).rolling(window=period).mean().values

    def calculate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate Saty Phase Oscillator values.
        
        Args:
            df: DataFrame with 'close', 'high', 'low' columns
            
        Returns:
            Dictionary containing oscillator values and signals
        """
        close = df['close'].values
        high = df['high'].values
        low = df['low'].values

        # Pivot calculation
        pivot = self.calculate_ema(close, 21)
        above_pivot = close >= pivot

        # Bollinger Band calculations
        bband_offset = 2.0 * self.calculate_stdev(close, 21)
        bband_up = pivot + bband_offset
        bband_down = pivot - bband_offset

        # ATR calculations
        atr = self.calculate_atr(high, low, close, 14)
        compression_threshold_up = pivot + (2.0 * atr)
        compression_threshold_down = pivot - (2.0 * atr)
        expansion_threshold_up = pivot + (1.854 * atr)
        expansion_threshold_down = pivot - (1.854 * atr)

        # Compression calculations
        compression = np.where(
            above_pivot,
            bband_up - compression_threshold_up,
            compression_threshold_down - bband_down
        )
        in_expansion_zone = np.where(
            above_pivot,
            bband_up - expansion_threshold_up,
            expansion_threshold_down - bband_down
        )
        expansion = np.roll(compression, 1) <= compression

        # Compression tracker
        compression_tracker = np.zeros_like(compression, dtype=bool)
        for i in range(1, len(compression)):
            if expansion[i] and in_expansion_zone[i] > 0:
                compression_tracker[i] = False
            elif compression[i] <= 0:
                compression_tracker[i] = True
            else:
                compression_tracker[i] = False

        # Phase Oscillator calculation
        raw_signal = ((close - pivot) / (3.0 * atr)) * 100
        oscillator = self.calculate_ema(raw_signal, 3)

        # Zone crosses
        leaving_accumulation = (np.roll(oscillator, 1) <= -61.8) & (oscillator > -61.8)
        leaving_extreme_down = (np.roll(oscillator, 1) <= -100) & (oscillator > -100)
        leaving_distribution = (np.roll(oscillator, 1) >= 61.8) & (oscillator < 61.8)
        leaving_extreme_up = (np.roll(oscillator, 1) >= 100) & (oscillator < 100)

        # Color determination
        colors = np.where(compression_tracker, 
                         self.colors['magenta'],
                         np.where(oscillator >= 0.0, 
                                 self.colors['green'], 
                                 self.colors['red']))

        return {
            'oscillator': oscillator,
            'compression_tracker': compression_tracker,
            'colors': colors,
            'zones': {
                'extended_up': 100.0,
                'distribution': 61.8,
                'neutral_up': 23.6,
                'neutral_down': -23.6,
                'accumulation': -61.8,
                'extended_down': -100.0
            },
            'signals': {
                'leaving_accumulation': leaving_accumulation,
                'leaving_extreme_down': leaving_extreme_down,
                'leaving_distribution': leaving_distribution,
                'leaving_extreme_up': leaving_extreme_up
            }
        }
