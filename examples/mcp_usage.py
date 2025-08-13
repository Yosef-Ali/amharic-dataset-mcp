#!/usr/bin/env python3
"""
Example usage of Amharic Dataset MCP Tools

This script demonstrates how to use the Amharic Dataset MCP tools
for collecting, enhancing, and scoring Amharic text data.
"""

import asyncio
import json
from amharic_dataset_mcp import AmharicMCPServer


async def main():
    """Demonstrate the Amharic MCP tools"""
    print("Amharic Dataset MCP Tools Example")
    print("=" * 40)
    
    # Initialize the MCP server
    server = AmharicMCPServer()
    print("✓ MCP Server initialized successfully")
    
    # The server is now ready to be used with any MCP-compatible client
    # For example, with Claude Desktop or other MCP clients
    
    print("\nAvailable tools:")
    print("- collect_amharic_data: Collect authentic Amharic data from Ethiopian sources")
    print("- enhance_amharic_quality: Enhance Amharic text quality using RAG techniques")
    print("- score_amharic_quality: Score Amharic text quality across multiple dimensions")
    print("- store_amharic_data: Store Amharic data in database with quality metrics")
    print("- batch_process_dataset: Process entire Amharic dataset through complete pipeline")
    
    print("\nTo use these tools with an MCP client:")
    print("1. Install the package: pip install amharic-dataset-mcp")
    print("2. Run the server: python -m amharic_dataset_mcp.server.main")
    print("3. Connect with an MCP client like Claude Desktop")
    
    print("\nExample tool usage:")
    print("collect_amharic_data(sources=['bbc_amharic'], max_items=50)")
    print("enhance_amharic_quality(texts=['እንደምን አደርክ አንተስ እንዴት ነህ'])")
    print("score_amharic_quality(text='እንደምን አደርክ? ደህና ነኝ።')")


if __name__ == "__main__":
    asyncio.run(main())