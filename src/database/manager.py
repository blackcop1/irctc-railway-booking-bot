"""Database manager for IRCTC booking bot"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pathlib import Path
from typing import Optional
from ..utils.logger import setup_logger
from ..utils.constants import DATABASE_PATH
from .models import Base

logger = setup_logger(__name__)


class DatabaseManager:
    """Manage database operations"""

    def __init__(self, db_path: str = DATABASE_PATH):
        """Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.engine = None
        self.SessionLocal = None
    
    def initialize(self) -> None:
        """Initialize database and create tables"""
        try:
            # Create database directory if needed
            db_dir = Path(self.db_path).parent
            db_dir.mkdir(parents=True, exist_ok=True)
            
            # Create engine
            self.engine = create_engine(
                f'sqlite:///{self.db_path}',
                echo=False,
                connect_args={"check_same_thread": False}
            )
            
            # Create tables
            Base.metadata.create_all(self.engine)
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info(f"Database initialized at {self.db_path}")
        
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get database session
        
        Returns:
            Database session
        """
        if not self.SessionLocal:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        
        return self.SessionLocal()
    
    def close(self) -> None:
        """Close database connections"""
        try:
            if self.engine:
                self.engine.dispose()
                logger.info("Database connections closed")
        
        except Exception as e:
            logger.error(f"Error closing database: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


class DatabaseOperations:
    """Common database operations"""

    def __init__(self, session: Session):
        """Initialize database operations
        
        Args:
            session: Database session
        """
        self.session = session
    
    def add(self, obj) -> None:
        """Add object to database
        
        Args:
            obj: Database model object
        """
        try:
            self.session.add(obj)
            self.session.commit()
            logger.debug(f"Added {type(obj).__name__} to database")
        
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to add object: {e}")
            raise
    
    def update(self, obj) -> None:
        """Update object in database
        
        Args:
            obj: Database model object
        """
        try:
            self.session.merge(obj)
            self.session.commit()
            logger.debug(f"Updated {type(obj).__name__} in database")
        
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to update object: {e}")
            raise
    
    def delete(self, obj) -> None:
        """Delete object from database
        
        Args:
            obj: Database model object
        """
        try:
            self.session.delete(obj)
            self.session.commit()
            logger.debug(f"Deleted {type(obj).__name__} from database")
        
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to delete object: {e}")
            raise
    
    def query(self, model) -> any:
        """Query database
        
        Args:
            model: Database model class
        
        Returns:
            Query object
        """
        return self.session.query(model)
    
    def close(self) -> None:
        """Close session"""
        try:
            self.session.close()
            logger.debug("Database session closed")
        
        except Exception as e:
            logger.error(f"Error closing session: {e}")
