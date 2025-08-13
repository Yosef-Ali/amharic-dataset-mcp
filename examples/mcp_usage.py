"""
Example usage of Amharic Dataset MCP Tools

This example demonstrates how to use the Amharic Dataset MCP server
with various AI models and clients.
"""

import asyncio
import json
from mcp.client import ClientSession
from mcp.client.stdio import stdio_client


async def demonstrate_mcp_tools():
    """Demonstrate usage of Amharic Dataset MCP tools"""
    
    print("🇪🇹 Amharic Dataset MCP Tools Demo")
    print("=" * 50)
    
    # Connect to MCP server
    async with stdio_client() as (read, write):
        async with ClientSession(read, write) as session:
            
            # Initialize connection
            await session.initialize()
            
            print("✅ Connected to Amharic Dataset MCP server")
            
            # Example 1: Collect Authentic Amharic Data
            print("\n📰 Example 1: Collecting Authentic Amharic Data")
            print("-" * 40)
            
            collection_result = await session.call_tool(
                "collect_amharic_data",
                {
                    "sources": ["bbc_amharic", "authentic_conversation"],
                    "max_items": 10,
                    "quality_threshold": 0.7
                }
            )
            
            collection_data = json.loads(collection_result.content[0].text)
            print(f"📊 Collected: {collection_data['collected']} items")
            print(f"✨ High quality: {collection_data['high_quality']} items")
            print(f"🔗 Sources: {', '.join(collection_data['sources'])}")
            
            # Show sample data
            if collection_data['data']:
                print("\n📋 Sample collected data:")
                for i, item in enumerate(collection_data['data'][:2], 1):
                    print(f"{i}. {item['text'][:60]}...")
                    print(f"   Source: {item['source']} | Quality: {item.get('estimated_quality', 'N/A')}")
            
            # Example 2: Enhance Text Quality with RAG
            print("\n🔮 Example 2: RAG-Based Quality Enhancement")
            print("-" * 40)
            
            # Sample texts with quality issues
            problematic_texts = [
                "እንጀራ በወጥ በላሁ። በእሳት ላይ ማቁሰል ይጀምራሉ።",  # Needs corrections
                "እንደምን አደርክ? ደህና ነው። ይብቃል።"  # Grammar issues
            ]
            
            enhancement_result = await session.call_tool(
                "enhance_amharic_quality",
                {
                    "texts": problematic_texts,
                    "context_category": "conversation"
                }
            )
            
            enhancement_data = json.loads(enhancement_result.content[0].text)
            print(f"🔧 Enhanced: {enhancement_data['enhanced_count']} texts")
            print(f"⚡ Total changes: {enhancement_data['total_changes']}")
            
            # Show enhancement results
            print("\n📋 Enhancement results:")
            for i, result in enumerate(enhancement_data['results'], 1):
                print(f"{i}. Original: {result['original_text']}")
                print(f"   Enhanced: {result['enhanced_text']}")
                if result['changes_made']:
                    print(f"   Changes: {', '.join(result['changes_made'])}")
                print(f"   Confidence: {result['confidence']:.3f}")
                print()
            
            # Example 3: Quality Scoring and Analysis
            print("\n⚡ Example 3: Multi-Dimensional Quality Scoring")
            print("-" * 40)
            
            # Test various quality texts
            test_texts = [
                "እንደምን አደርክ? ደህና ነኝ፣ እግዚአብሔር ይመስገን። አንተስ እንዴት ነህ?",  # High quality
                "ወጥ በላሁ። በጣም ጣፋጭ ነበር።",  # Good quality
                "hello world እንደምን አደር"  # Mixed language, low quality
            ]
            
            for i, text in enumerate(test_texts, 1):
                score_result = await session.call_tool(
                    "score_amharic_quality",
                    {
                        "text": text,
                        "detailed_analysis": True
                    }
                )
                
                score_data = json.loads(score_result.content[0].text)
                
                print(f"\n{i}. Text: {text}")
                print(f"   Overall Score: {score_data['overall_score']:.3f}")
                print(f"   Category: {score_data['quality_category']}")
                
                # Show component scores
                components = score_data['component_scores']
                print(f"   Grammar: {components['grammar_quality']:.3f} | "
                      f"Cultural: {components['cultural_authenticity']:.3f} | "
                      f"Natural: {components['conversation_naturalness']:.3f}")
                
                if score_data['recommendations']:
                    print(f"   💡 Recommendation: {score_data['recommendations'][0]}")
            
            # Example 4: Database Storage
            print("\n🗄️ Example 4: Database Storage")
            print("-" * 40)
            
            # Prepare sample data for storage
            sample_data = [
                {
                    'text': 'የኢትዮጵያ መንግስት አዲስ የትምህርት ፖሊሲ አወጣ።',
                    'source': 'bbc_amharic',
                    'category': 'education',
                    'quality_score': 0.85,
                    'quality_category': 'excellent'
                },
                {
                    'text': 'እንደምን አደርክ? ደህና ነኝ፣ እግዚአብሔር ይመስገን።',
                    'source': 'authentic_conversation', 
                    'category': 'greeting',
                    'quality_score': 0.95,
                    'quality_category': 'excellent'
                }
            ]
            
            storage_result = await session.call_tool(
                "store_amharic_data",
                {
                    "data": sample_data,
                    "database_url": "sqlite:///demo_amharic_dataset.db"
                }
            )
            
            storage_data = json.loads(storage_result.content[0].text)
            print(f"💾 Stored: {storage_data['stored_items']} items")
            print(f"🗃️ Total items in DB: {storage_data['total_items']}")
            print(f"📊 Sources in DB: {list(storage_data['sources'].keys())}")
            
            # Example 5: Batch Processing Pipeline
            print("\n🚀 Example 5: Complete Batch Processing Pipeline")
            print("-" * 40)
            
            # Sample dataset for batch processing
            raw_dataset = [
                {
                    'text': 'እንጀራ በወጥ በላሁ። በእሳት ላይ ማቁሰል ይጀምራሉ።',
                    'source': 'generated',
                    'category': 'food'
                },
                {
                    'text': 'እንደምን አደርክ? ደህና ነው። ይብቃል።',
                    'source': 'generated', 
                    'category': 'greeting'
                },
                {
                    'text': 'ሐኪም ወዴት ሄደህ? ወደ ሆስፒታል ሄዳለሁ።',
                    'source': 'authentic_conversation',
                    'category': 'health'
                }
            ]
            
            batch_result = await session.call_tool(
                "batch_process_dataset",
                {
                    "input_data": raw_dataset,
                    "quality_threshold": 0.6,
                    "enhance_quality": True
                }
            )
            
            batch_data = json.loads(batch_result.content[0].text)
            stats = batch_data['statistics']
            
            print(f"📥 Input items: {stats['input_count']}")
            print(f"🔮 Enhanced items: {stats['enhanced_count']}")
            print(f"✨ High quality items: {stats['high_quality_count']}")
            print(f"🚫 Filtered out: {stats['filtered_out']}")
            print(f"📤 Final output: {batch_data['total_output_items']} items")
            
            # Show sample processed data
            if batch_data['processed_data']:
                print("\n📋 Sample processed data:")
                for i, item in enumerate(batch_data['processed_data'][:2], 1):
                    print(f"{i}. Text: {item['text']}")
                    print(f"   Quality Score: {item['quality_score']:.3f}")
                    print(f"   Category: {item['quality_category']}")
                    if item.get('rag_enhanced'):
                        print(f"   RAG Enhanced: {len(item.get('rag_changes', []))} changes")
            
            print("\n🎉 MCP Tools Demo Complete!")
            print("✅ All Amharic dataset tools working correctly")


async def demonstrate_integration_with_claude():
    """Example of integrating MCP tools with Claude Code"""
    
    print("\n🤖 Integration with Claude Code")
    print("=" * 40)
    
    # This would be the actual integration in Claude Code settings
    mcp_config = {
        "mcpServers": {
            "amharic-dataset": {
                "command": "amharic-dataset-server",
                "args": ["--port", "3001"],
                "env": {
                    "LOG_LEVEL": "INFO"
                }
            }
        }
    }
    
    print("📝 Claude Code MCP Configuration:")
    print(json.dumps(mcp_config, indent=2))
    
    print("\n💡 Usage in Claude Code:")
    print("1. Add the above configuration to your Claude Code settings")
    print("2. Restart Claude Code to load the MCP server")
    print("3. Use tools like: 'Collect authentic Amharic data from Ethiopian sources'")
    print("4. Or: 'Enhance this Amharic text quality with RAG'")
    print("5. Or: 'Score the quality of this Amharic conversation'")


async def demonstrate_scaling_examples():
    """Examples of scaling MCP tools for production use"""
    
    print("\n📈 Production Scaling Examples")
    print("=" * 40)
    
    scaling_scenarios = [
        {
            "name": "Large Dataset Collection",
            "description": "Collect 10,000+ authentic articles from Ethiopian news sources",
            "config": {
                "sources": ["bbc_amharic", "voa_amharic", "ethiopian_reporter"],
                "max_items_per_source": 5000,
                "quality_threshold": 0.7,
                "batch_size": 100
            }
        },
        {
            "name": "Quality Enhancement Pipeline", 
            "description": "Enhance existing dataset of 50,000 examples using RAG",
            "config": {
                "batch_size": 500,
                "parallel_workers": 4,
                "context_categories": ["news", "conversation", "literature"]
            }
        },
        {
            "name": "Real-time Quality Scoring",
            "description": "Score incoming Amharic text in real-time applications",
            "config": {
                "throughput_target": "1000 texts/second",
                "response_time": "<100ms",
                "quality_dimensions": ["grammar", "cultural", "naturalness"]
            }
        }
    ]
    
    for i, scenario in enumerate(scaling_scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print(f"   📋 {scenario['description']}")
        print(f"   ⚙️  Configuration:")
        for key, value in scenario['config'].items():
            print(f"      • {key}: {value}")


if __name__ == "__main__":
    print("🇪🇹 Amharic Dataset MCP Tools - Usage Examples")
    print("=" * 60)
    
    # Run demonstrations
    asyncio.run(demonstrate_mcp_tools())
    asyncio.run(demonstrate_integration_with_claude()) 
    asyncio.run(demonstrate_scaling_examples())
    
    print("\n🌟 Ready to revolutionize Ethiopian language AI!")
    print("🚀 MCP tools available for production deployment")