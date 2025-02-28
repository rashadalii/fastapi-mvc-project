from typing import Dict, Any, Optional
import time
from app.config import get_settings

settings = get_settings()

class CacheService:
    """Service for caching data with expiration."""
    
    def __init__(self):
        """Initialize the cache service."""
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache if it exists and is not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Any: Cached value or None if not found or expired
        """
        # Check if key exists in cache
        if key not in self._cache:
            return None
            
        cache_entry = self._cache[key]
        
        # Check if entry is expired
        if cache_entry["expiry"] < time.time():
            # Remove expired entry
            del self._cache[key]
            return None
            
        return cache_entry["data"]
    
    def set(self, key: str, value: Any, expiry_seconds: Optional[int] = None) -> None:
        """
        Set a value in the cache with expiration.
        
        Args:
            key: Cache key
            value: Value to cache
            expiry_seconds: Expiration time in seconds (default from settings)
        """
        if expiry_seconds is None:
            expiry_seconds = settings.CACHE_EXPIRY_SECONDS
            
        self._cache[key] = {
            "data": value,
            "expiry": time.time() + expiry_seconds
        }
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if deleted, False if not found
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False
        
    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()

# Create a singleton instance
cache = CacheService()