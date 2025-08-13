"""
Amharic Data Manager

This module provides database management tools for storing and retrieving
authentic Amharic dataset items with quality metrics.
"""

import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

Base = declarative_base()


class AmharicDataItem(Base):
    """Database model for Amharic data items"""
    __tablename__ = 'amharic_data_items'
    
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    source = Column(String(100))
    category = Column(String(50))
    quality_score = Column(Float)
    quality_category = Column(String(20))
    length = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column(Text)  # Store additional metadata as JSON


class AmharicDataManager:
    """Manager for Amharic dataset storage and retrieval"""
    
    def __init__(self, database_url: str = "sqlite:///amharic_dataset.db"):
        """Initialize the database manager"""
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables
        Base.metadata.create_all(bind=self.engine)
        
        logger.info(f"Amharic Data Manager initialized with database: {database_url}")
    
    @classmethod
    def from_url(cls, database_url: str) -> 'AmharicDataManager':
        """
        Create AmharicDataManager from database URL
        
        Args:
            database_url: Database connection URL
            
        Returns:
            AmharicDataManager instance
        """
        return cls(database_url)
    
    def store_authentic_data(self, data_items: List[Dict[str, Any]]) -> int:
        """
        Store authentic Amharic data items in database
        
        Args:
            data_items: List of Amharic data items to store
            
        Returns:
            Number of items successfully stored
        """
        session = self.SessionLocal()
        stored_count = 0
        
        try:
            for item in data_items:
                # Create database model instance
                db_item = AmharicDataItem(
                    text=item.get('text', ''),
                    source=item.get('source'),
                    category=item.get('category'),
                    quality_score=item.get('quality_score'),
                    quality_category=item.get('quality_category'),
                    length=len(item.get('text', '')),
                    metadata_json=json.dumps({
                        'title': item.get('title'),
                        'context': item.get('context'),
                        'type': item.get('type'),
                        'estimated_quality': item.get('estimated_quality'),
                        'rag_enhanced': item.get('rag_enhanced', False),
                        'rag_changes': item.get('rag_changes', [])
                    })
                )
                
                session.add(db_item)
                stored_count += 1
            
            session.commit()
            logger.info(f"Stored {stored_count} Amharic data items in database")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error storing Amharic data: {e}")
            raise
        finally:
            session.close()
        
        return stored_count
    
    def retrieve_high_quality_data(
        self, 
        min_quality_score: float = 0.7,
        limit: int = 100,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve high-quality Amharic data items from database
        
        Args:
            min_quality_score: Minimum quality score threshold
            limit: Maximum number of items to retrieve
            category: Optional category filter
            
        Returns:
            List of high-quality Amharic data items
        """
        session = self.SessionLocal()
        
        try:
            query = session.query(AmharicDataItem).filter(
                AmharicDataItem.quality_score >= min_quality_score
            )
            
            if category:
                query = query.filter(AmharicDataItem.category == category)
            
            db_items = query.order_by(AmharicDataItem.timestamp.desc()).limit(limit).all()
            
            # Convert to dictionary format
            items = []
            for db_item in db_items:
                metadata = {}
                if db_item.metadata_json:
                    try:
                        metadata = json.loads(db_item.metadata_json)
                    except json.JSONDecodeError:
                        pass
                
                item = {
                    'id': db_item.id,
                    'text': db_item.text,
                    'source': db_item.source,
                    'category': db_item.category,
                    'quality_score': db_item.quality_score,
                    'quality_category': db_item.quality_category,
                    'length': db_item.length,
                    'timestamp': db_item.timestamp.isoformat() if db_item.timestamp else None,
                    **metadata
                }
                items.append(item)
            
            logger.info(f"Retrieved {len(items)} high-quality Amharic data items")
            return items
            
        except Exception as e:
            logger.error(f"Error retrieving Amharic data: {e}")
            raise
        finally:
            session.close()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics
        
        Returns:
            Dictionary with database statistics
        """
        session = self.SessionLocal()
        
        try:
            total_items = session.query(AmharicDataItem).count()
            
            # Get source distribution
            source_stats = session.query(
                AmharicDataItem.source, 
                AmharicDataItem.category
            ).distinct().all()
            
            sources = list(set([s[0] for s in source_stats if s[0]]))
            categories = list(set([c[1] for c in source_stats if c[1]]))
            
            # Get quality distribution
            avg_quality = session.query(AmharicDataItem.quality_score).filter(
                AmharicDataItem.quality_score.isnot(None)
            ).scalar()
            
            result = {
                "total_items": total_items,
                "sources": sources,
                "categories": categories,
                "average_quality_score": float(avg_quality) if avg_quality else 0.0
            }
            
            logger.info(f"Database statistics: {total_items} total items")
            return result
            
        except Exception as e:
            logger.error(f"Error getting database statistics: {e}")
            return {
                "total_items": 0,
                "sources": [],
                "categories": [],
                "average_quality_score": 0.0
            }
        finally:
            session.close()
    
    def close(self):
        """Close database connections"""
        self.engine.dispose()
        logger.info("Amharic Data Manager connections closed")