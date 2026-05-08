"""Main application entry point for IRCTC Railway Booking Bot"""

import asyncio
import sys
import os
from pathlib import Path
from typing import Optional
from src.utils.logger import setup_logger
from src.services import IRCTCBookingService

# Setup logging
logger = setup_logger(__name__)

# Set timeout configuration
os.environ.setdefault('DEFAULT_PAGE_TIMEOUT', '60')
os.environ.setdefault('BOOKING_TIMEOUT', '60')


async def main(
    username: str,
    password: str,
    captcha_api_key: str,
    from_station: str,
    to_station: str,
    travel_date: str,
    class_type: str = "SL",
    quota: str = "GN",
    headless: bool = False,
) -> bool:
    """Main booking workflow
    
    Args:
        username: IRCTC username
        password: IRCTC password
        captcha_api_key: 2Captcha API key
        from_station: Departure station code
        to_station: Destination station code
        travel_date: Travel date (DD-MM-YYYY)
        class_type: Class type code
        quota: Quota type
        headless: Run browser in headless mode
    
    Returns:
        True if booking successful, False otherwise
    """
    try:
        logger.info("Starting IRCTC Railway Booking Bot")
        logger.info(f"Booking route: {from_station} -> {to_station}")
        logger.info(f"Travel date: {travel_date}, Class: {class_type}, Quota: {quota}")
        
        # Initialize booking service
        async with IRCTCBookingService(
            username=username,
            password=password,
            captcha_api_key=captcha_api_key,
            headless=headless,
            use_ntp_sync=True,
        ) as service:
            
            # Login to IRCTC
            logger.info("Step 1: Logging in to IRCTC...")
            if not await service.login():
                logger.error("Failed to login to IRCTC")
                return False
            
            logger.info("✓ Successfully logged in")
            
            # Search for trains
            logger.info("Step 2: Searching for trains...")
            trains = await service.search_trains(
                from_station=from_station,
                to_station=to_station,
                travel_date=travel_date,
                passenger_count=1,
                class_type=class_type,
            )
            
            if not trains:
                logger.warning("No trains found for the given criteria")
                return False
            
            logger.info(f"✓ Found {len(trains)} trains")
            
            # Wait for Tatkal window if needed
            if quota == "TQ":
                logger.info("Step 3: Waiting for Tatkal booking window...")
                await service.wait_for_tatkal_window(class_type=class_type)
                logger.info("✓ Tatkal window opened")
            
            # Book first available train
            if trains:
                train = trains[0]
                logger.info(f"Step 4: Booking {train['train_number']} ({train['train_name']})...")
                
                passengers = [
                    {
                        "name": "Test Passenger",
                        "age": "30",
                        "gender": "M",
                        "berth_preference": "LB",
                    }
                ]
                
                pnr = await service.book_train(
                    train_number=train['train_number'],
                    passengers=passengers,
                    from_station=from_station,
                    to_station=to_station,
                    travel_date=travel_date,
                    class_type=class_type,
                    quota=quota,
                )
                
                if pnr:
                    logger.info(f"✓ Booking successful! PNR: {pnr}")
                    return True
                else:
                    logger.error("Booking failed")
                    return False
            
            return False
    
    except KeyboardInterrupt:
        logger.info("Booking cancelled by user")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return False


def load_config(config_file: Optional[str] = None) -> dict:
    """Load configuration from file or environment
    
    Args:
        config_file: Path to configuration file (YAML/JSON)
    
    Returns:
        Configuration dictionary
    """
    config = {
        "username": "",
        "password": "",
        "captcha_api_key": "",
        "from_station": "",
        "to_station": "",
        "travel_date": "",
        "class_type": "SL",
        "quota": "GN",
        "headless": False,
    }
    
    # Load from environment variables
    config["username"] = os.getenv("IRCTC_USERNAME", config["username"])
    config["password"] = os.getenv("IRCTC_PASSWORD", config["password"])
    config["captcha_api_key"] = os.getenv("CAPTCHA_API_KEY", config["captcha_api_key"])
    config["from_station"] = os.getenv("FROM_STATION", config["from_station"])
    config["to_station"] = os.getenv("TO_STATION", config["to_station"])
    config["travel_date"] = os.getenv("TRAVEL_DATE", config["travel_date"])
    config["class_type"] = os.getenv("CLASS_TYPE", config["class_type"])
    config["quota"] = os.getenv("QUOTA", config["quota"])
    config["headless"] = os.getenv("HEADLESS", "false").lower() == "true"
    
    # Load from config file if provided
    if config_file and Path(config_file).exists():
        try:
            import json
            with open(config_file) as f:
                file_config = json.load(f)
                config.update(file_config)
            logger.info(f"Configuration loaded from {config_file}")
        except Exception as e:
            logger.warning(f"Failed to load config file: {e}")
    
    return config


async def run(config: dict) -> int:
    """Run the booking bot with configuration
    
    Args:
        config: Configuration dictionary
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Validate required fields
    required_fields = ["username", "password", "captcha_api_key", "from_station", "to_station", "travel_date"]
    missing_fields = [field for field in required_fields if not config.get(field)]
    
    if missing_fields:
        logger.error(f"Missing required configuration: {', '.join(missing_fields)}")
        return 1
    
    # Run booking workflow
    success = await main(
        username=config["username"],
        password=config["password"],
        captcha_api_key=config["captcha_api_key"],
        from_station=config["from_station"],
        to_station=config["to_station"],
        travel_date=config["travel_date"],
        class_type=config.get("class_type", "SL"),
        quota=config.get("quota", "GN"),
        headless=config.get("headless", False),
    )
    
    return 0 if success else 1


if __name__ == "__main__":
    # Load .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # Parse command line arguments
    import argparse
    
    parser = argparse.ArgumentParser(
        description="IRCTC Railway Booking Bot - Automated ticket booking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using .env file
  python main.py
  
  # Using command line arguments
  python main.py --username myuser --password mypass --captcha-key mykey --from NDLS --to MMCT --date 15-05-2026
  
  # Using config file
  python main.py --config config.json
  
  # Tatkal booking
  python main.py --from NDLS --to MMCT --date 15-05-2026 --quota TQ
        """
    )
    
    parser.add_argument("--config", help="Configuration file path (JSON)")
    parser.add_argument("--username", help="IRCTC username")
    parser.add_argument("--password", help="IRCTC password")
    parser.add_argument("--captcha-key", dest="captcha_api_key", help="2Captcha API key")
    parser.add_argument("--from", dest="from_station", help="Departure station code (e.g., NDLS)")
    parser.add_argument("--to", dest="to_station", help="Destination station code (e.g., MMCT)")
    parser.add_argument("--date", dest="travel_date", help="Travel date (DD-MM-YYYY format)")
    parser.add_argument("--class", dest="class_type", default="SL", help="Class type: SL, AC2, AC3, 1A, 2A, 3A (default: SL)")
    parser.add_argument("--quota", default="GN", help="Quota type: GN, TQ, PT, RL (default: GN)")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode (no GUI)")
    
    args = parser.parse_args()
    
    # Load configuration from file first
    config = load_config(args.config)
    
    # Override with command line arguments
    if args.username:
        config["username"] = args.username
    if args.password:
        config["password"] = args.password
    if args.captcha_api_key:
        config["captcha_api_key"] = args.captcha_api_key
    if args.from_station:
        config["from_station"] = args.from_station
    if args.to_station:
        config["to_station"] = args.to_station
    if args.travel_date:
        config["travel_date"] = args.travel_date
    if args.class_type:
        config["class_type"] = args.class_type
    if args.quota:
        config["quota"] = args.quota
    if args.headless:
        config["headless"] = True
    
    # Run the bot
    try:
        exit_code = asyncio.run(run(config))
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
