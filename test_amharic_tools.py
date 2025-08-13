#!/usr/bin/env python3
"""
Test script for Amharic Dataset MCP Tools
"""

import asyncio
import json
from amharic_dataset_mcp import (
    AmharicDataCollector, 
    AmharicRAGEnhancer, 
    AmharicQualityScorer,
    AmharicDataManager
)


async def test_collector():
    """Test the Amharic data collector"""
    print("Testing Amharic Data Collector...")
    collector = AmharicDataCollector()
    
    # Test with a simple authentic Amharic text
    sample_text = "እንደምን አደርክ? ደህና ነኝ፣ እግዚአብሔር ይመስገን።"
    
    # Test text validation
    is_amharic = collector.is_amharic_text(sample_text)
    print(f"Is Amharic text: {is_amharic}")
    
    # Test text cleaning
    cleaned = collector.clean_amharic_text(sample_text)
    print(f"Cleaned text: {cleaned}")
    
    print("Collector test completed!")


def test_enhancer():
    """Test the Amharic RAG enhancer"""
    print("Testing Amharic RAG Enhancer...")
    enhancer = AmharicRAGEnhancer()
    
    # Test with a sample text
    sample_text = "እንደምን አደርክ አንተስ እንዴት ነህ"
    
    # Enhance the text
    result = enhancer.enhance_amharic_text(sample_text)
    print(f"Original: {result['original_text']}")
    print(f"Enhanced: {result['enhanced_text']}")
    print(f"Changes made: {len(result['changes_made'])}")
    
    print("Enhancer test completed!")


def test_scorer():
    """Test the Amharic quality scorer"""
    print("Testing Amharic Quality Scorer...")
    scorer = AmharicQualityScorer()
    
    # Test with a sample text
    sample_text = "እንደምን አደርክ? ደህና ነኝ፣ እግዚአብሔር ይመስገን። እንዴት ነህ?"
    
    # Score the text
    result = scorer.calculate_overall_quality_score(sample_text)
    print(f"Text preview: {result['text_preview']}")
    print(f"Overall score: {result['overall_score']}")
    print(f"Quality category: {result['quality_category']}")
    print(f"Component scores: {result['component_scores']}")
    
    print("Scorer test completed!")


def test_database():
    """Test the Amharic database manager"""
    print("Testing Amharic Database Manager...")
    db_manager = AmharicDataManager("sqlite:///test_amharic_dataset.db")
    
    # Test with sample data
    sample_data = [{
        'text': 'እንደምን አደርክ? ደህና ነኝ፣ እግዚአብሔር ይመስገን።',
        'source': 'test',
        'category': 'greeting',
        'quality_score': 0.9,
        'quality_category': 'excellent'
    }]
    
    # Store data
    stored_count = db_manager.store_authentic_data(sample_data)
    print(f"Stored {stored_count} items")
    
    # Get statistics
    stats = db_manager.get_statistics()
    print(f"Database statistics: {stats}")
    
    print("Database test completed!")


async def main():
    """Run all tests"""
    print("Running Amharic Dataset MCP Tools Tests")
    
    # Run tests
    await test_collector()
    test_enhancer()
    test_scorer()
    test_database()
    
    print("All tests completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())