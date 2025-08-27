"""
GCP Configuration for Financial Analysis Assistant.

This module handles configuration for Google Cloud Platform services
including Firestore, Redis, Cloud Storage, and Secret Manager.
"""
import os
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class GCPConfig:
    """Configuration for GCP services."""
    project_id: str
    region: str = "us-central1"
    environment: str = "dev"
    
    # Firestore
    firestore_database: str = "(default)"
    
    # Redis
    redis_host: Optional[str] = None
    redis_port: int = 6379
    redis_password: Optional[str] = None
    
    # Cloud Storage
    storage_bucket: Optional[str] = None
    
    # Secret Manager
    google_api_key_secret: Optional[str] = None
    alpha_vantage_key_secret: Optional[str] = None
    polygon_key_secret: Optional[str] = None
    
    @classmethod
    def from_environment(cls) -> 'GCPConfig':
        """Create configuration from environment variables."""
        project_id = os.getenv('PROJECT_ID')
        if not project_id:
            raise ValueError("PROJECT_ID environment variable is required")
        
        environment = os.getenv('ENVIRONMENT', 'dev')
        
        return cls(
            project_id=project_id,
            region=os.getenv('REGION', 'us-central1'),
            environment=environment,
            
            # Firestore
            firestore_database=os.getenv('FIRESTORE_DATABASE', '(default)'),
            
            # Redis
            redis_host=os.getenv('REDIS_HOST'),
            redis_port=int(os.getenv('REDIS_PORT', 6379)),
            redis_password=os.getenv('REDIS_PASSWORD'),
            
            # Cloud Storage
            storage_bucket=os.getenv('STORAGE_BUCKET'),
            
            # Secret Manager
            google_api_key_secret=os.getenv('GOOGLE_API_KEY_SECRET', f'google-api-key-{environment}'),
            alpha_vantage_key_secret=os.getenv('ALPHA_VANTAGE_KEY_SECRET', f'alpha-vantage-key-{environment}'),
            polygon_key_secret=os.getenv('POLYGON_KEY_SECRET', f'polygon-key-{environment}'),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'project_id': self.project_id,
            'region': self.region,
            'environment': self.environment,
            'firestore_database': self.firestore_database,
            'redis_host': self.redis_host,
            'redis_port': self.redis_port,
            'storage_bucket': self.storage_bucket,
            'google_api_key_secret': self.google_api_key_secret,
            'alpha_vantage_key_secret': self.alpha_vantage_key_secret,
            'polygon_key_secret': self.polygon_key_secret,
        }


class GCPServiceManager:
    """Manager for GCP service clients."""
    
    def __init__(self, config: GCPConfig):
        self.config = config
        self._firestore_client = None
        self._storage_client = None
        self._secret_client = None
        
    @property
    def firestore_client(self):
        """Get Firestore client (lazy initialization)."""
        if self._firestore_client is None:
            try:
                from google.cloud import firestore
                self._firestore_client = firestore.Client(
                    project=self.config.project_id,
                    database=self.config.firestore_database
                )
                logger.info("Firestore client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Firestore client: {e}")
                raise
        return self._firestore_client
    
    @property
    def storage_client(self):
        """Get Cloud Storage client (lazy initialization)."""
        if self._storage_client is None:
            try:
                from google.cloud import storage
                self._storage_client = storage.Client(project=self.config.project_id)
                logger.info("Cloud Storage client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Cloud Storage client: {e}")
                raise
        return self._storage_client
    
    @property
    def secret_client(self):
        """Get Secret Manager client (lazy initialization)."""
        if self._secret_client is None:
            try:
                from google.cloud import secretmanager
                self._secret_client = secretmanager.SecretManagerServiceClient()
                logger.info("Secret Manager client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Secret Manager client: {e}")
                raise
        return self._secret_client
    
    def get_secret(self, secret_name: str) -> Optional[str]:
        """Get secret value from Secret Manager."""
        try:
            name = f"projects/{self.config.project_id}/secrets/{secret_name}/versions/latest"
            response = self.secret_client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except Exception as e:
            logger.warning(f"Failed to get secret {secret_name}: {e}")
            return None
    
    def get_api_keys(self) -> Dict[str, Optional[str]]:
        """Get all API keys from Secret Manager or environment."""
        api_keys = {}
        
        # Try to get from Secret Manager first
        if self.config.google_api_key_secret:
            api_keys['google_api_key'] = self.get_secret(self.config.google_api_key_secret)
        
        if self.config.alpha_vantage_key_secret:
            api_keys['alpha_vantage_key'] = self.get_secret(self.config.alpha_vantage_key_secret)
        
        if self.config.polygon_key_secret:
            api_keys['polygon_key'] = self.get_secret(self.config.polygon_key_secret)
        
        # Fallback to environment variables
        if not api_keys.get('google_api_key'):
            api_keys['google_api_key'] = os.getenv('GOOGLE_API_KEY')
        
        if not api_keys.get('alpha_vantage_key'):
            api_keys['alpha_vantage_key'] = os.getenv('ALPHA_VANTAGE_API_KEY')
        
        if not api_keys.get('polygon_key'):
            api_keys['polygon_key'] = os.getenv('POLYGON_API_KEY')
        
        return api_keys
    
    def get_storage_bucket(self):
        """Get the configured storage bucket."""
        if not self.config.storage_bucket:
            return None
        
        try:
            return self.storage_client.bucket(self.config.storage_bucket)
        except Exception as e:
            logger.error(f"Failed to get storage bucket: {e}")
            return None


# Global configuration instance
_gcp_config = None
_gcp_service_manager = None


def get_gcp_config() -> Optional[GCPConfig]:
    """Get the global GCP configuration."""
    global _gcp_config
    
    if _gcp_config is None:
        try:
            _gcp_config = GCPConfig.from_environment()
        except Exception as e:
            logger.warning(f"GCP configuration not available: {e}")
            return None
    
    return _gcp_config


def get_gcp_service_manager() -> Optional[GCPServiceManager]:
    """Get the global GCP service manager."""
    global _gcp_service_manager
    
    if _gcp_service_manager is None:
        config = get_gcp_config()
        if config:
            _gcp_service_manager = GCPServiceManager(config)
    
    return _gcp_service_manager


def is_gcp_available() -> bool:
    """Check if GCP services are available."""
    return get_gcp_config() is not None