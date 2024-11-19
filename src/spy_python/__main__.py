"""Main entry point for the SPY Python application"""
from .config.logging import get_logger
from .web_app import run_web_app

logger = get_logger()

def main():
    """Main function"""
    try:
        logger.info("Starting SPY Python web application")
        run_web_app(debug=True)
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
