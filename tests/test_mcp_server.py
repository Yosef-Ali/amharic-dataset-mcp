"""
Test suite for Amharic Dataset MCP Server

This module contains comprehensive tests for the MCP server functionality
including tool registration, data collection, quality enhancement, and storage.
"""

import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from mcp.types import TextContent

from amharic_dataset_mcp.server.main import AmharicMCPServer


@pytest.fixture
def mcp_server():
    """Create MCP server instance for testing"""
    return AmharicMCPServer()


@pytest.fixture
def sample_amharic_data():
    """Sample Amharic data for testing"""
    return [
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
        }
    ]


@pytest.mark.asyncio
class TestAmharicMCPServer:
    """Test suite for Amharic MCP Server"""
    
    async def test_server_initialization(self, mcp_server):
        """Test that MCP server initializes correctly"""
        assert mcp_server.server is not None
        assert mcp_server.collector is not None
        assert mcp_server.enhancer is not None
        assert mcp_server.scorer is not None
    
    async def test_collect_amharic_data_tool(self, mcp_server):
        """Test the collect_amharic_data MCP tool"""
        # Get the tool function
        tool_func = None
        for tool in mcp_server.server._tools.values():
            if tool.name == "collect_amharic_data":
                tool_func = tool.func
                break
        
        assert tool_func is not None, "collect_amharic_data tool should be registered"
        
        # Test tool execution
        result = await tool_func(
            sources=["bbc_amharic", "authentic_conversation"],
            max_items=5,
            quality_threshold=0.6
        )
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        
        # Parse result JSON
        result_data = json.loads(result[0].text)
        assert "collected" in result_data
        assert "high_quality" in result_data
        assert "sources" in result_data
        assert "data" in result_data
    
    async def test_enhance_amharic_quality_tool(self, mcp_server):
        """Test the enhance_amharic_quality MCP tool"""
        # Get the tool function
        tool_func = None
        for tool in mcp_server.server._tools.values():
            if tool.name == "enhance_amharic_quality":
                tool_func = tool.func
                break
        
        assert tool_func is not None, "enhance_amharic_quality tool should be registered"
        
        # Test enhancement
        test_texts = [
            "እንጀራ በወጥ በላሁ። በእሳት ላይ ማቁሰል ይጀምራሉ።",
            "እንደምን አደርክ? ደህና ነው።"
        ]
        
        result = await tool_func(
            texts=test_texts,
            context_category="conversation"
        )
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        
        # Parse result JSON
        result_data = json.loads(result[0].text)
        assert "enhanced_count" in result_data
        assert "total_changes" in result_data
        assert "results" in result_data
        assert len(result_data["results"]) == len(test_texts)
    
    async def test_score_amharic_quality_tool(self, mcp_server):
        """Test the score_amharic_quality MCP tool"""
        # Get the tool function
        tool_func = None
        for tool in mcp_server.server._tools.values():
            if tool.name == "score_amharic_quality":
                tool_func = tool.func
                break
        
        assert tool_func is not None, "score_amharic_quality tool should be registered"
        
        # Test quality scoring
        test_text = "እንደምን አደርክ? ደህና ነኝ፣ እግዚአብሔር ይመስገን። አንተስ እንዴት ነህ?"
        
        result = await tool_func(
            text=test_text,
            detailed_analysis=True
        )
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        
        # Parse result JSON
        result_data = json.loads(result[0].text)
        assert "overall_score" in result_data
        assert "quality_category" in result_data
        assert "component_scores" in result_data
        assert "detailed_analysis" in result_data
    
    async def test_store_amharic_data_tool(self, mcp_server, sample_amharic_data):
        """Test the store_amharic_data MCP tool"""
        # Get the tool function
        tool_func = None
        for tool in mcp_server.server._tools.values():
            if tool.name == "store_amharic_data":
                tool_func = tool.func
                break
        
        assert tool_func is not None, "store_amharic_data tool should be registered"
        
        # Mock database manager
        with patch('amharic_dataset_mcp.database.manager.AmharicDataManager') as mock_db_class:
            mock_db = AsyncMock()
            mock_db.store_authentic_data.return_value = len(sample_amharic_data)
            mock_db.get_statistics.return_value = {
                "total_items": len(sample_amharic_data),
                "sources": {"bbc_amharic": 1, "authentic_conversation": 1}
            }
            mock_db_class.from_url.return_value = mock_db
            
            # Test data storage
            result = await tool_func(
                data=sample_amharic_data,
                database_url="sqlite:///test.db"
            )
            
            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], TextContent)
            
            # Parse result JSON
            result_data = json.loads(result[0].text)
            assert "stored_items" in result_data
            assert "database_url" in result_data
            assert "total_items" in result_data
            assert "sources" in result_data
    
    async def test_batch_process_dataset_tool(self, mcp_server, sample_amharic_data):
        """Test the batch_process_dataset MCP tool"""
        # Get the tool function
        tool_func = None
        for tool in mcp_server.server._tools.values():
            if tool.name == "batch_process_dataset":
                tool_func = tool.func
                break
        
        assert tool_func is not None, "batch_process_dataset tool should be registered"
        
        # Test batch processing
        result = await tool_func(
            input_data=sample_amharic_data,
            quality_threshold=0.6,
            enhance_quality=True
        )
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        
        # Parse result JSON  
        result_data = json.loads(result[0].text)
        assert "statistics" in result_data
        assert "processed_data" in result_data
        assert "total_output_items" in result_data
        
        # Check statistics
        stats = result_data["statistics"]
        assert "input_count" in stats
        assert "high_quality_count" in stats
        assert "filtered_out" in stats
    
    async def test_error_handling(self, mcp_server):
        """Test error handling in MCP tools"""
        # Get a tool function
        tool_func = None
        for tool in mcp_server.server._tools.values():
            if tool.name == "score_amharic_quality":
                tool_func = tool.func
                break
        
        # Test with invalid input
        with pytest.raises(Exception):
            await tool_func(text="", detailed_analysis=True)


@pytest.mark.asyncio
class TestMCPIntegration:
    """Integration tests for MCP server"""
    
    async def test_complete_pipeline(self, mcp_server):
        """Test complete data processing pipeline through MCP"""
        # Step 1: Collect data
        collect_func = None
        enhance_func = None
        score_func = None
        
        # Get tool functions
        for tool in mcp_server.server._tools.values():
            if tool.name == "collect_amharic_data":
                collect_func = tool.func
            elif tool.name == "enhance_amharic_quality":
                enhance_func = tool.func
            elif tool.name == "score_amharic_quality": 
                score_func = tool.func
        
        assert all([collect_func, enhance_func, score_func])
        
        # Execute pipeline
        collection_result = await collect_func(
            sources=["authentic_conversation"],
            max_items=3,
            quality_threshold=0.5
        )
        
        collection_data = json.loads(collection_result[0].text)
        assert collection_data["collected"] > 0
        
        # Extract texts for enhancement
        sample_texts = [item["text"] for item in collection_data["data"][:2]]
        
        # Step 2: Enhance quality
        if sample_texts:
            enhance_result = await enhance_func(
                texts=sample_texts,
                context_category="conversation"
            )
            
            enhance_data = json.loads(enhance_result[0].text)
            assert enhance_data["enhanced_count"] == len(sample_texts)
            
            # Step 3: Score quality
            enhanced_text = enhance_data["results"][0]["enhanced_text"]
            score_result = await score_func(
                text=enhanced_text,
                detailed_analysis=True
            )
            
            score_data = json.loads(score_result[0].text)
            assert "overall_score" in score_data
            assert 0.0 <= score_data["overall_score"] <= 1.0
    
    async def test_concurrent_tool_usage(self, mcp_server):
        """Test concurrent usage of multiple MCP tools"""
        score_func = None
        for tool in mcp_server.server._tools.values():
            if tool.name == "score_amharic_quality":
                score_func = tool.func
                break
        
        assert score_func is not None
        
        # Test concurrent scoring of multiple texts
        test_texts = [
            "እንደምን አደርክ? ደህና ነኝ፣ እግዚአብሔር ይመስገን።",
            "ወጥ በላሁ። በጣም ጣፋጭ ነበር።",
            "ሐኪም ወዴት ሄደህ? ወደ ሆስፒታል ሄዳለሁ።"
        ]
        
        # Execute scoring concurrently
        tasks = [
            score_func(text=text, detailed_analysis=False)
            for text in test_texts
        ]
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == len(test_texts)
        for result in results:
            assert isinstance(result, list)
            assert len(result) == 1
            score_data = json.loads(result[0].text)
            assert "quality_score" in score_data


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])