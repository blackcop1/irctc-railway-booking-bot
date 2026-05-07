"""Captcha solving using 2Captcha API"""

import requests
import time
from typing import Optional
from ..utils.logger import setup_logger
from ..utils.constants import CAPTCHA_TIMEOUT, CAPTCHA_MAX_RETRIES

logger = setup_logger(__name__)


class CaptchaSolver:
    """Solve captchas using 2Captcha API"""

    TWOCAPTCHA_UPLOAD_URL = "http://2captcha.com/api/upload"
    TWOCAPTCHA_RESULT_URL = "http://2captcha.com/api/res"

    def __init__(self, api_key: str, timeout: int = CAPTCHA_TIMEOUT):
        """Initialize captcha solver
        
        Args:
            api_key: 2Captcha API key
            timeout: Captcha solving timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
    
    def solve_image_captcha(self, image_path: str) -> Optional[str]:
        """Solve image-based captcha
        
        Args:
            image_path: Path to captcha image or image URL
        
        Returns:
            Captcha solution or None if failed
        """
        try:
            # Upload captcha image
            if image_path.startswith('http'):
                # Image URL
                payload = {
                    'key': self.api_key,
                    'url': image_path,
                    'json': 1,
                }
                response = requests.post(self.TWOCAPTCHA_UPLOAD_URL, data=payload, timeout=10)
            else:
                # Local file
                with open(image_path, 'rb') as f:
                    files = {'captchafile': f}
                    payload = {
                        'key': self.api_key,
                        'json': 1,
                    }
                    response = requests.post(self.TWOCAPTCHA_UPLOAD_URL, data=payload, files=files, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Failed to upload captcha: {response.text}")
                return None
            
            result = response.json()
            if result.get('is_ok') != 1:
                logger.error(f"Captcha upload error: {result.get('error')}")
                return None
            
            captcha_id = result.get('captcha')
            logger.info(f"Captcha uploaded with ID: {captcha_id}")
            
            # Poll for result
            return self._poll_for_result(captcha_id)
        
        except Exception as e:
            logger.error(f"Error solving captcha: {e}")
            return None
    
    def _poll_for_result(self, captcha_id: int) -> Optional[str]:
        """Poll 2Captcha for captcha solution
        
        Args:
            captcha_id: Captcha ID from upload response
        
        Returns:
            Captcha solution or None if failed
        """
        start_time = time.time()
        
        while time.time() - start_time < self.timeout:
            try:
                payload = {
                    'key': self.api_key,
                    'action': 'get',
                    'captcha': captcha_id,
                    'json': 1,
                }
                
                response = requests.get(self.TWOCAPTCHA_RESULT_URL, params=payload, timeout=10)
                result = response.json()
                
                if result.get('is_ok') != 1:
                    if result.get('error') == 'CAPCHA_NOT_READY':
                        # Captcha not ready yet, wait and retry
                        time.sleep(2)
                        continue
                    else:
                        logger.error(f"Captcha solving error: {result.get('error')}")
                        return None
                
                solution = result.get('captcha')
                logger.info(f"Captcha solved: {solution}")
                return solution
            
            except Exception as e:
                logger.error(f"Error polling captcha result: {e}")
                time.sleep(2)
        
        logger.error(f"Timeout waiting for captcha solution (ID: {captcha_id})")
        return None
    
    def get_balance(self) -> Optional[float]:
        """Get current account balance
        
        Returns:
            Account balance or None if failed
        """
        try:
            payload = {
                'key': self.api_key,
                'action': 'getbalance',
                'json': 1,
            }
            
            response = requests.get(self.TWOCAPTCHA_RESULT_URL, params=payload, timeout=10)
            result = response.json()
            
            if result.get('is_ok') == 1:
                balance = float(result.get('captcha', 0))
                logger.info(f"Account balance: ${balance}")
                return balance
            else:
                logger.error(f"Failed to get balance: {result.get('error')}")
                return None
        
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return None
