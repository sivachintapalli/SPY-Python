"""Comprehensive Logging Configuration for SPY Python"""
import sys
from datetime import datetime
import json
from pathlib import Path
from loguru import logger
import os

class SPYLogger:
    """Advanced logging configuration for SPY Python application"""
    
    def __init__(self):
        # Create logs directory structure
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for different log types
        self.error_dir = self.logs_dir / "errors"
        self.data_dir = self.logs_dir / "data"
        self.chart_dir = self.logs_dir / "charts"
        self.performance_dir = self.logs_dir / "performance"
        
        for directory in [self.error_dir, self.data_dir, self.chart_dir, self.performance_dir]:
            directory.mkdir(exist_ok=True)
        
        # Remove default logger
        logger.remove()
        
        # Add handlers for different logging purposes
        self._configure_console_logging()
        self._configure_error_logging()
        self._configure_data_logging()
        self._configure_chart_logging()
        self._configure_performance_logging()
    
    def _configure_console_logging(self):
        """Configure console logging with color formatting"""
        format_str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        format_str += "<level>{level: <8}</level> | "
        format_str += "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        format_str += "<level>{message}</level>"
        
        logger.add(
            sys.stderr,
            format=format_str,
            level="INFO",
            colorize=True,
            backtrace=True,
            diagnose=True
        )
    
    def _configure_error_logging(self):
        """Configure error logging with detailed error information"""
        error_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
        error_format += "{name}:{function}:{line} | "
        error_format += "Error: {message} | "
        error_format += "Exception: {exception}"
        
        logger.add(
            self.error_dir / "error_{time:YYYY-MM-DD}.log",
            format=error_format,
            level="ERROR",
            rotation="1 day",
            retention="30 days",
            backtrace=True,
            diagnose=True
        )
    
    def _configure_data_logging(self):
        """Configure data operation logging"""
        data_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
        data_format += "{name}:{function}:{line} | "
        data_format += "Data Operation: {message}"
        
        logger.add(
            self.data_dir / "data_{time:YYYY-MM-DD}.log",
            format=data_format,
            filter=lambda record: "data_service" in record["name"],
            level="DEBUG",
            rotation="1 day",
            retention="30 days"
        )
    
    def _configure_chart_logging(self):
        """Configure chart operation logging"""
        chart_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
        chart_format += "{name}:{function}:{line} | "
        chart_format += "Chart Operation: {message}"
        
        logger.add(
            self.chart_dir / "chart_{time:YYYY-MM-DD}.log",
            format=chart_format,
            filter=lambda record: "chart_service" in record["name"],
            level="DEBUG",
            rotation="1 day",
            retention="30 days"
        )
    
    def _configure_performance_logging(self):
        """Configure performance logging"""
        perf_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
        perf_format += "{name}:{function}:{line} | "
        perf_format += "Performance: {message}"
        
        logger.add(
            self.performance_dir / "performance_{time:YYYY-MM-DD}.log",
            format=perf_format,
            filter=lambda record: record["extra"].get("type") == "performance",
            level="DEBUG",
            rotation="1 day",
            retention="30 days"
        )
    
    @staticmethod
    def log_data_operation(operation: str, details: dict):
        """Log data operations with structured details"""
        logger.bind(type="data").debug(
            f"{operation} | " + json.dumps(details, default=str)
        )
    
    @staticmethod
    def log_chart_operation(operation: str, details: dict):
        """Log chart operations with structured details"""
        logger.bind(type="chart").debug(
            f"{operation} | " + json.dumps(details, default=str)
        )
    
    @staticmethod
    def log_performance(operation: str, start_time: datetime, end_time: datetime, details: dict):
        """Log performance metrics"""
        duration = (end_time - start_time).total_seconds()
        details["duration_seconds"] = duration
        logger.bind(type="performance").debug(
            f"{operation} | Duration: {duration:.3f}s | " + json.dumps(details, default=str)
        )
    
    @staticmethod
    def log_error(error: Exception, context: dict = None):
        """Log errors with context"""
        if context is None:
            context = {}
        logger.bind(type="error").exception(
            f"Error occurred | Context: {json.dumps(context, default=str)}",
            exception=error
        )

# Initialize logger
spy_logger = SPYLogger()

def get_logger():
    """Get configured logger instance"""
    return logger
