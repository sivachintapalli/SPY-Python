"""
JavaScript bridge for Lightweight Charts.
"""
import json
from typing import Dict, Any, Optional

class JSBridge:
    """Bridge between Python and JavaScript for Lightweight Charts."""
    
    @staticmethod
    def create_chart(chart_config: Dict[str, Any]) -> str:
        """Generate JavaScript code to create a chart."""
        return f"""
        const chart = LightweightCharts.createChart(
            document.getElementById('{chart_config["container"]}'),
            {json.dumps(chart_config["options"])}
        );
        window.charts = window.charts || {{}};
        window.charts['{chart_config["chart_id"]}'] = chart;
        """

    @staticmethod
    def add_series(chart_id: str, series_type: str, series_id: str, 
                  options: Dict[str, Any], data: Optional[list] = None) -> str:
        """Generate JavaScript code to add a series to a chart."""
        series_creation = {
            'candlestick': 'addCandlestickSeries',
            'line': 'addLineSeries',
            'histogram': 'addHistogramSeries'
        }

        js_code = f"""
        const chart = window.charts['{chart_id}'];
        const series = chart.{series_creation[series_type]}({json.dumps(options)});
        window.series = window.series || {{}};
        window.series['{series_id}'] = series;
        """

        if data:
            js_code += f"series.setData({json.dumps(data)});"

        return js_code

    @staticmethod
    def update_series(series_id: str, data_point: Dict[str, Any]) -> str:
        """Generate JavaScript code to update a series with new data."""
        return f"""
        const series = window.series['{series_id}'];
        series.update({json.dumps(data_point)});
        """

    @staticmethod
    def set_visible_range(chart_id: str, from_time: int, to_time: int) -> str:
        """Generate JavaScript code to set the visible time range."""
        return f"""
        const chart = window.charts['{chart_id}'];
        chart.timeScale().setVisibleRange({{
            from: {from_time},
            to: {to_time}
        }});
        """

    @staticmethod
    def subscribe_crosshair_move(chart_id: str, subscription_id: str) -> str:
        """Generate JavaScript code to subscribe to crosshair movement."""
        return f"""
        const chart = window.charts['{chart_id}'];
        chart.subscribeCrosshairMove(param => {{
            window.pywebview.api.handle_crosshair_move('{subscription_id}', param);
        }});
        """

    @staticmethod
    def remove_series(chart_id: str, series_id: str) -> str:
        """Generate JavaScript code to remove a series."""
        return f"""
        const chart = window.charts['{chart_id}'];
        const series = window.series['{series_id}'];
        chart.removeSeries(series);
        delete window.series['{series_id}'];
        """

    @staticmethod
    def apply_options(chart_id: str, options: Dict[str, Any]) -> str:
        """Generate JavaScript code to apply new options to a chart."""
        return f"""
        const chart = window.charts['{chart_id}'];
        chart.applyOptions({json.dumps(options)});
        """

    @staticmethod
    def take_screenshot(chart_id: str) -> str:
        """Generate JavaScript code to take a screenshot of the chart."""
        return f"""
        const chart = window.charts['{chart_id}'];
        return chart.takeScreenshot();
        """

    @staticmethod
    def resize(chart_id: str, width: int, height: int) -> str:
        """Generate JavaScript code to resize the chart."""
        return f"""
        const chart = window.charts['{chart_id}'];
        chart.resize({width}, {height});
        """
