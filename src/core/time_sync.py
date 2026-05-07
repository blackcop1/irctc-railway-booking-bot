"""NTP-based time synchronization for accurate booking window timing"""

import ntplib
import time
from datetime import datetime, timedelta
from typing import Optional, List
from ..utils.logger import setup_logger
from ..utils.constants import NTP_SERVERS

logger = setup_logger(__name__)


class TimeSync:
    """Synchronize system time with NTP servers for precise booking timing"""

    def __init__(self, ntp_servers: Optional[List[str]] = None, sync_interval: int = 5):
        """Initialize time synchronizer
        
        Args:
            ntp_servers: List of NTP server addresses
            sync_interval: Sync interval in seconds (default: 5)
        """
        self.ntp_servers = ntp_servers or NTP_SERVERS
        self.sync_interval = sync_interval
        self.time_offset = 0.0
        self.last_sync_time = None
        self.is_synced = False
    
    def sync(self) -> bool:
        """Synchronize with NTP server
        
        Returns:
            True if sync successful, False otherwise
        """
        client = ntplib.NTPClient()
        
        for server in self.ntp_servers:
            try:
                logger.info(f"Syncing time with NTP server: {server}")
                response = client.request(server, version=3, timeout=5)
                
                # Calculate time offset
                self.time_offset = response.tx_time - time.time()
                self.last_sync_time = datetime.now()
                self.is_synced = True
                
                logger.info(f"Successfully synced with {server}. Offset: {self.time_offset:.3f}s")
                return True
            except Exception as e:
                logger.warning(f"Failed to sync with {server}: {e}")
                continue
        
        logger.error("Failed to sync with any NTP server")
        return False
    
    def get_synced_time(self) -> datetime:
        """Get current time with NTP offset applied
        
        Returns:
            Current synced datetime
        """
        if not self.is_synced:
            logger.warning("Time not synced. Using system time.")
            return datetime.now()
        
        return datetime.fromtimestamp(time.time() + self.time_offset)
    
    def get_time_until_event(self, target_time: datetime) -> timedelta:
        """Calculate time remaining until target event
        
        Args:
            target_time: Target datetime for the event
        
        Returns:
            Timedelta until target time
        """
        current_time = self.get_synced_time()
        delta = target_time - current_time
        return delta
    
    def wait_until(self, target_time: datetime) -> bool:
        """Wait until target time
        
        Args:
            target_time: Target datetime
        
        Returns:
            True when target time is reached
        """
        while True:
            current_time = self.get_synced_time()
            if current_time >= target_time:
                logger.info(f"Target time {target_time} reached")
                return True
            
            # Sleep for 10ms to avoid busy waiting
            time.sleep(0.01)
    
    def needs_resync(self) -> bool:
        """Check if resync is needed based on sync interval
        
        Returns:
            True if resync is needed
        """
        if not self.is_synced or self.last_sync_time is None:
            return True
        
        elapsed = (datetime.now() - self.last_sync_time).total_seconds()
        return elapsed > self.sync_interval
    
    def get_offset_ms(self) -> int:
        """Get current time offset in milliseconds
        
        Returns:
            Time offset in milliseconds
        """
        return int(self.time_offset * 1000)
    
    def __repr__(self) -> str:
        sync_status = "synced" if self.is_synced else "not synced"
        return f"TimeSync(offset={self.time_offset:.3f}s, status={sync_status})"
