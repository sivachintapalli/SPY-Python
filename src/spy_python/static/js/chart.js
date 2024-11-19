// Chart initialization and management
class ChartManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.chart = LightweightCharts.createChart(this.container, {
            layout: {
                background: { color: '#1E1E1E' },
                textColor: '#DDD',
            },
            grid: {
                vertLines: { color: '#2B2B2B' },
                horzLines: { color: '#2B2B2B' },
            },
            crosshair: {
                mode: LightweightCharts.CrosshairMode.Normal,
                vertLine: {
                    width: 1,
                    color: '#758696',
                    style: LightweightCharts.LineStyle.Solid,
                    labelBackgroundColor: '#758696',
                },
                horzLine: {
                    width: 1,
                    color: '#758696',
                    style: LightweightCharts.LineStyle.Solid,
                    labelBackgroundColor: '#758696',
                },
            },
            timeScale: {
                timeVisible: true,
                secondsVisible: false,
            },
        });

        // Create main price series
        this.mainSeries = this.chart.addCandlestickSeries({
            upColor: '#4CAF50',
            downColor: '#FF5252',
            borderVisible: false,
            wickUpColor: '#4CAF50',
            wickDownColor: '#FF5252',
        });

        // Create volume series
        this.volumeSeries = this.chart.addHistogramSeries({
            color: '#26a69a',
            priceFormat: {
                type: 'volume',
            },
            priceScaleId: '',
            scaleMargins: {
                top: 0.8,
                bottom: 0,
            },
        });

        // Create oscillator series
        this.oscillatorSeries = this.chart.addLineSeries({
            color: 'rgba(255, 255, 255, 0.5)',
            lineWidth: 2,
            priceScaleId: 'oscillator',
            scaleMargins: {
                top: 0.1,
                bottom: 0.1,
            },
        });

        // Set up legend
        this.setupLegend();

        // Initialize data
        this.fetchAndUpdateData();
    }

    setupLegend() {
        const legend = document.createElement('div');
        legend.className = 'legend';
        this.container.appendChild(legend);

        this.legend = {
            container: legend,
            items: {
                ohlc: document.createElement('div'),
                volume: document.createElement('div'),
                oscillator: document.createElement('div')
            }
        };

        // Add items to legend
        for (const key in this.legend.items) {
            this.legend.items[key].className = 'legend-item';
            this.legend.container.appendChild(this.legend.items[key]);
        }

        // Subscribe to crosshair moves
        this.chart.subscribeCrosshairMove(this.handleCrosshairMove.bind(this));
    }

    handleCrosshairMove(param) {
        if (!param.time || param.point.x < 0 || param.point.x > this.container.clientWidth || param.point.y < 0 || param.point.y > this.container.clientHeight) {
            this.legend.items.ohlc.innerHTML = '';
            this.legend.items.volume.innerHTML = '';
            this.legend.items.oscillator.innerHTML = '';
            return;
        }

        const price = param.seriesData.get(this.mainSeries);
        const volume = param.seriesData.get(this.volumeSeries);
        const oscillator = param.seriesData.get(this.oscillatorSeries);

        if (price) {
            const color = price.close >= price.open ? '#4CAF50' : '#FF5252';
            this.legend.items.ohlc.innerHTML = `
                <div style="color: ${color}">
                    O: ${price.open.toFixed(2)}
                    H: ${price.high.toFixed(2)}
                    L: ${price.low.toFixed(2)}
                    C: ${price.close.toFixed(2)}
                </div>
            `;
        }

        if (volume) {
            const formattedVolume = this.formatVolume(volume.value);
            this.legend.items.volume.innerHTML = `
                <div>Volume: ${formattedVolume}</div>
            `;
        }

        if (oscillator) {
            this.legend.items.oscillator.innerHTML = `
                <div>Oscillator: ${oscillator.value.toFixed(2)}</div>
            `;
        }
    }

    formatVolume(volume) {
        if (volume >= 1000000) {
            return (volume / 1000000).toFixed(2) + 'M';
        }
        if (volume >= 1000) {
            return (volume / 1000).toFixed(2) + 'K';
        }
        return volume.toString();
    }

    async fetchAndUpdateData() {
        try {
            const response = await fetch('/api/chart-data');
            const data = await response.json();

            // Update candlestick series
            this.mainSeries.setData(data.candlesticks);

            // Update volume series
            this.volumeSeries.setData(data.volume);

            // Update oscillator series
            this.oscillatorSeries.setData(data.oscillator);

            // Add markers
            if (data.markers) {
                this.mainSeries.setMarkers(data.markers);
            }

            // Fit content
            this.chart.timeScale().fitContent();

        } catch (error) {
            console.error('Error fetching chart data:', error);
        }
    }
}

// Initialize chart when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chartManager = new ChartManager('chart');
});
