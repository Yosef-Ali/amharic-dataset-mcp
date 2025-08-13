"""
MCP Server for Amharic Dataset Tools

This module implements the Model Context Protocol server that exposes
Amharic dataset tools as MCP tools for integration with various AI models.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Sequence

from mcp import McpError, Tool
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent
from pydantic import BaseModel

from ..tools.collector import AmharicDataCollector
from ..tools.enhancer import AmharicRAGEnhancer  
from ..tools.scorer import AmharicQualityScorer
from ..database.manager import AmharicDataManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AmharicMCPServer:
    """MCP Server for Amharic dataset processing tools"""
    
    def __init__(self):
        """Initialize the MCP server with Amharic tools"""
        self.server = Server("amharic-dataset-mcp")
        self.collector = AmharicDataCollector()
        self.enhancer = AmharicRAGEnhancer()
        self.scorer = AmharicQualityScorer()
        self.db_manager = None  # Initialized when needed
        
        # Register MCP tools
        self._register_tools()
        
        logger.info("Amharic Dataset MCP Server initialized")
    
    def _register_tools(self):
        """Register all Amharic dataset tools with MCP server"""
        
        # Data Collection Tool
        @self.server.call_tool()
        async def collect_amharic_data(
            sources: Optional[List[str]] = None,
            max_items: int = 100,
            quality_threshold: float = 0.6
        ) -> List[TextContent]:
            """
            Collect authentic Amharic data from Ethiopian sources.
            
            Args:
                sources: List of source names (bbc_amharic, voa_amharic, etc.)
                max_items: Maximum number of items to collect  
                quality_threshold: Minimum quality score to accept
            
            Returns:
                List of collected authentic Amharic data items
            """
            try:
                logger.info(f"Collecting Amharic data: {max_items} items from {sources}")
                
                # Use default sources if none specified
                if sources is None:
                    sources = ["bbc_amharic", "voa_amharic", "authentic_conversation"]
                
                # Simulate collection for demo (in production would scrape real sources)
                collected_data = await self._simulate_data_collection(sources, max_items)
                
                # Filter by quality threshold
                high_quality = [
                    item for item in collected_data 
                    if item.get('estimated_quality', 0.5) >= quality_threshold
                ]
                
                result = {
                    "collected": len(collected_data),
                    "high_quality": len(high_quality),
                    "sources": sources,
                    "data": high_quality[:10]  # Return sample for display
                }
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, ensure_ascii=False, indent=2)
                )]
                
            except Exception as e:
                logger.error(f"Error collecting Amharic data: {e}")
                raise McpError(f"Data collection failed: {e}")
        
        # Quality Enhancement Tool  
        @self.server.call_tool()
        async def enhance_amharic_quality(
            texts: List[str],
            context_category: str = "general"
        ) -> List[TextContent]:
            """
            Enhance Amharic text quality using RAG-based corrections.
            
            Args:
                texts: List of Amharic texts to enhance
                context_category: Context category for enhancement (news, conversation, etc.)
            
            Returns:
                Enhanced texts with improvement details
            """
            try:
                logger.info(f"Enhancing {len(texts)} Amharic texts")
                
                enhanced_results = []
                for text in texts:
                    enhancement = self.enhancer.enhance_amharic_text(text, context_category)
                    enhanced_results.append(enhancement)
                
                result = {
                    "enhanced_count": len(enhanced_results),
                    "total_changes": sum(len(r.get('changes_made', [])) for r in enhanced_results),
                    "results": enhanced_results
                }
                
                return [TextContent(
                    type="text", 
                    text=json.dumps(result, ensure_ascii=False, indent=2)
                )]
                
            except Exception as e:
                logger.error(f"Error enhancing Amharic quality: {e}")
                raise McpError(f"Quality enhancement failed: {e}")
        
        # Quality Scoring Tool
        @self.server.call_tool()
        async def score_amharic_quality(
            text: str,
            detailed_analysis: bool = True
        ) -> List[TextContent]:
            """
            Score Amharic text quality across multiple dimensions.
            
            Args:
                text: Amharic text to score
                detailed_analysis: Whether to include detailed component analysis
            
            Returns:
                Quality score and analysis details
            """
            try:
                logger.info(f"Scoring Amharic text quality")
                
                quality_result = self.scorer.calculate_overall_quality_score(text)
                
                if not detailed_analysis:
                    # Return simplified result
                    result = {
                        "text": text,
                        "quality_score": quality_result["overall_score"],
                        "quality_category": quality_result["quality_category"],
                        "recommendations": quality_result["recommendations"]
                    }
                else:
                    # Return full analysis
                    result = quality_result
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, ensure_ascii=False, indent=2)  
                )]
                
            except Exception as e:
                logger.error(f"Error scoring Amharic quality: {e}")
                raise McpError(f"Quality scoring failed: {e}")
        
        # Database Storage Tool
        @self.server.call_tool()
        async def store_amharic_data(
            data: List[Dict[str, Any]],
            database_url: str = "sqlite:///amharic_dataset.db"
        ) -> List[TextContent]:
            """
            Store Amharic data in database with quality metrics.
            
            Args:
                data: List of Amharic data items to store
                database_url: Database connection URL
            
            Returns:
                Storage confirmation and statistics
            """
            try:
                logger.info(f"Storing {len(data)} Amharic items in database")
                
                # Initialize database manager if needed
                if self.db_manager is None or self.db_manager.engine.url != database_url:
                    self.db_manager = AmharicDataManager.from_url(database_url)
                
                # Store data
                stored_count = self.db_manager.store_authentic_data(data)
                
                # Get updated statistics
                stats = self.db_manager.get_statistics()
                
                result = {
                    "stored_items": stored_count,
                    "database_url": database_url,
                    "total_items": stats["total_items"],
                    "sources": stats["sources"]
                }
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, ensure_ascii=False, indent=2)
                )]
                
            except Exception as e:
                logger.error(f"Error storing Amharic data: {e}")
                raise McpError(f"Data storage failed: {e}")
        
        # Batch Processing Tool
        @self.server.call_tool()
        async def batch_process_dataset(
            input_data: List[Dict[str, Any]],
            quality_threshold: float = 0.6,
            enhance_quality: bool = True
        ) -> List[TextContent]:
            """
            Process entire Amharic dataset through complete pipeline.
            
            Args:
                input_data: Raw Amharic dataset to process
                quality_threshold: Minimum quality score to retain
                enhance_quality: Whether to apply RAG enhancement
            
            Returns:
                Processed dataset with quality metrics
            """
            try:
                logger.info(f"Batch processing {len(input_data)} Amharic items")
                
                processed_data = []
                stats = {
                    "input_count": len(input_data),
                    "enhanced_count": 0,
                    "high_quality_count": 0,
                    "filtered_out": 0
                }
                
                for item in input_data:
                    # Enhance quality if requested
                    if enhance_quality and 'text' in item:
                        enhancement = self.enhancer.enhance_amharic_text(
                            item['text'], 
                            item.get('category', 'general')
                        )
                        item['text'] = enhancement['enhanced_text']
                        item['rag_enhanced'] = True
                        item['rag_changes'] = enhancement['changes_made']
                        if enhancement['changes_made']:
                            stats['enhanced_count'] += 1
                    
                    # Score quality
                    if 'text' in item:
                        quality_result = self.scorer.calculate_overall_quality_score(item['text'])
                        item.update({
                            'quality_score': quality_result['overall_score'],
                            'quality_category': quality_result['quality_category'],
                            'quality_components': quality_result['component_scores']
                        })
                        
                        # Filter by quality threshold
                        if quality_result['overall_score'] >= quality_threshold:
                            processed_data.append(item)
                            stats['high_quality_count'] += 1
                        else:
                            stats['filtered_out'] += 1
                    else:
                        processed_data.append(item)
                
                result = {
                    "statistics": stats,
                    "processed_data": processed_data[:5],  # Sample for display
                    "total_output_items": len(processed_data)
                }
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, ensure_ascii=False, indent=2)
                )]
                
            except Exception as e:
                logger.error(f"Error in batch processing: {e}")
                raise McpError(f"Batch processing failed: {e}")
    
    async def _simulate_data_collection(self, sources: List[str], max_items: int) -> List[Dict[str, Any]]:
        """Simulate data collection for demonstration"""
        # In production, this would scrape real Ethiopian websites
        sample_data = [
            {
                'text': 'የኢትዮጵያ መንግስት አዲስ የትምህርት ፖሊሲ አወጣ። ይህ ፖሊሲ በሁሉም ክልሎች ይተገበራል።',
                'source': 'bbc_amharic',
                'category': 'education', 
                'estimated_quality': 0.85
            },
            {
                'text': 'እንደምን አደርክ? ደህና ነኝ፣ እግዚአብሔር ይመስገን። አንተስ እንዴት ነህ?',
                'source': 'authentic_conversation',
                'category': 'greeting',
                'estimated_quality': 0.95
            },
            {
                'text': 'ጠዋት ትምህርት ቤት ስሄድ እናቴ ምሳ አዘጋጀችልኝ። በጣም ጣፋጭ ወጥ ነበር።',
                'source': 'authentic_conversation', 
                'category': 'food',
                'estimated_quality': 0.90
            }
        ]
        
        # Replicate and vary data to reach max_items
        collected_data = []
        for i in range(min(max_items, 100)):  # Limit for demo
            base_item = sample_data[i % len(sample_data)].copy()
            base_item['id'] = f"item_{i+1}"
            collected_data.append(base_item)
        
        return collected_data
    
    async def serve(self):
        """Start the MCP server"""
        logger.info("Starting Amharic Dataset MCP Server...")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, 
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point for MCP server"""
    server = AmharicMCPServer()
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())