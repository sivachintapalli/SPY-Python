"""
Configuration options for Lightweight Charts.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Union

@dataclass
class ColorOptions:
    """Color options for various chart elements."""
    background: str = '#1e222d'
    text: str = '#d9d9d9'
    grid: str = 'rgba(43, 43, 67, 0.5)'
    border: str = '#2b2b43'
    up: str = '#26a69a'
    down: str = '#ef5350'
    wick: str = '#737375'

@dataclass
class CrosshairLineOptions:
    """Options for crosshair lines."""
    color: str = '#758696'
    width: int = 1
    style: int = 1
    visible: bool = True
    label_visible: bool = True
    label_background_color: str = '#2b2b43'

@dataclass
class CrosshairOptions:
    """Options for chart crosshair."""
    mode: str = 'normal'
    vert_line: CrosshairLineOptions = field(default_factory=CrosshairLineOptions)
    horz_line: CrosshairLineOptions = field(default_factory=CrosshairLineOptions)

@dataclass
class HandleOptions:
    """Options for chart handling."""
    mouse_wheel: bool = True
    pressed_mouse_move: bool = True
    horz_touch_drag: bool = True
    vert_touch_drag: bool = True
    pinch: bool = True
    axis_pressed_mouse_move: bool = True

@dataclass
class TimeScaleOptions:
    """Options for time scale."""
    time_visible: bool = True
    seconds_visible: bool = False
    border_color: str = '#2b2b43'
    right_offset: int = 12
    bar_spacing: int = 6
    fix_left_edge: bool = False
    lock_visible_time_range_on_resize: bool = True
    right_bar_stays_on_scroll: bool = True
    border_visible: bool = False
    visible: bool = True

@dataclass
class PriceFormatOptions:
    """Options for price formatting."""
    type: str = 'price'
    precision: int = 2
    min_move: float = 0.01

@dataclass
class SeriesOptionsBase:
    """Base options for all series types."""
    price_scale_id: str = 'right'
    visible: bool = True
    price_format: PriceFormatOptions = field(default_factory=PriceFormatOptions)

@dataclass
class CandlestickSeriesOptions(SeriesOptionsBase):
    """Options specific to candlestick series."""
    up_color: str = '#26a69a'
    down_color: str = '#ef5350'
    border_visible: bool = True
    wick_visible: bool = True
    border_color: str = '#2b2b43'
    wick_color: str = '#737375'

@dataclass
class HistogramSeriesOptions(SeriesOptionsBase):
    """Options specific to histogram series."""
    color: str = '#26a69a'
    base: float = 0

@dataclass
class ChartOptions:
    """Main chart configuration options."""
    width: int = 800
    height: int = 600
    layout: Dict[str, Any] = field(default_factory=lambda: {
        'background': ColorOptions().background,
        'text_color': ColorOptions().text,
    })
    grid: Dict[str, Any] = field(default_factory=lambda: {
        'vert_lines': {'color': ColorOptions().grid},
        'horz_lines': {'color': ColorOptions().grid},
    })
    crosshair: CrosshairOptions = field(default_factory=CrosshairOptions)
    time_scale: TimeScaleOptions = field(default_factory=TimeScaleOptions)
    handle_scroll: HandleOptions = field(default_factory=HandleOptions)
    handle_scale: HandleOptions = field(default_factory=HandleOptions)

    def to_dict(self) -> Dict[str, Any]:
        """Convert options to dictionary format for JavaScript."""
        return {
            'width': self.width,
            'height': self.height,
            'layout': self.layout,
            'grid': self.grid,
            'crosshair': {
                'mode': self.crosshair.mode,
                'vertLine': {
                    'color': self.crosshair.vert_line.color,
                    'width': self.crosshair.vert_line.width,
                    'style': self.crosshair.vert_line.style,
                    'visible': self.crosshair.vert_line.visible,
                    'labelVisible': self.crosshair.vert_line.label_visible,
                    'labelBackgroundColor': self.crosshair.vert_line.label_background_color,
                },
                'horzLine': {
                    'color': self.crosshair.horz_line.color,
                    'width': self.crosshair.horz_line.width,
                    'style': self.crosshair.horz_line.style,
                    'visible': self.crosshair.horz_line.visible,
                    'labelVisible': self.crosshair.horz_line.label_visible,
                    'labelBackgroundColor': self.crosshair.horz_line.label_background_color,
                },
            },
            'timeScale': {
                'timeVisible': self.time_scale.time_visible,
                'secondsVisible': self.time_scale.seconds_visible,
                'borderColor': self.time_scale.border_color,
                'rightOffset': self.time_scale.right_offset,
                'barSpacing': self.time_scale.bar_spacing,
                'fixLeftEdge': self.time_scale.fix_left_edge,
                'lockVisibleTimeRangeOnResize': self.time_scale.lock_visible_time_range_on_resize,
                'rightBarStaysOnScroll': self.time_scale.right_bar_stays_on_scroll,
                'borderVisible': self.time_scale.border_visible,
                'visible': self.time_scale.visible,
            },
            'handleScroll': {
                'mouseWheel': self.handle_scroll.mouse_wheel,
                'pressedMouseMove': self.handle_scroll.pressed_mouse_move,
                'horzTouchDrag': self.handle_scroll.horz_touch_drag,
                'vertTouchDrag': self.handle_scroll.vert_touch_drag,
            },
            'handleScale': {
                'mouseWheel': self.handle_scale.mouse_wheel,
                'pressedMouseMove': self.handle_scale.pressed_mouse_move,
                'pinch': self.handle_scale.pinch,
                'axisPressedMouseMove': self.handle_scale.axis_pressed_mouse_move,
            },
        }
