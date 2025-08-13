"""
Amharic Dataset MCP Tools

Production-ready MCP (Model Context Protocol) tools for authentic Amharic dataset 
collection, enhancement, and quality scoring.

This package provides:
- Authentic data collection from Ethiopian sources
- RAG-based quality enhancement 
- Multi-dimensional quality scoring
- Database integration and storage
- Scalable batch processing

Author: Amharic Language AI Team
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Amharic Language AI Team"
__email__ = "amharic-ai@example.com"
__license__ = "MIT"

from .tools.collector import AmharicDataCollector
from .tools.enhancer import AmharicRAGEnhancer
from .tools.scorer import AmharicQualityScorer
from .database.manager import AmharicDataManager
from .server.main import AmharicMCPServer

__all__ = [
    "AmharicDataCollector",
    "AmharicRAGEnhancer", 
    "AmharicQualityScorer",
    "AmharicDataManager",
    "AmharicMCPServer"
]