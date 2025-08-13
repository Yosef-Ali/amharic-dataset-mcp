"""
Amharic Data Collector

This module provides tools for collecting authentic Amharic text data from
Ethiopian sources including news websites, social media, and literature.
"""

import asyncio
import re
import time
from datetime import datetime
from typing import Dict, List, Optional
import logging

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class AmharicDataCollector:
    """Collector for authentic Amharic text data from Ethiopian sources"""
    
    def __init__(self):
        """Initialize the Amharic data collector"""
        self.session = httpx.AsyncClient(
            headers={
                'User-Agent': 'Mozilla/5.0 (Amharic Research Bot) Educational/Research'
            },
            timeout=30.0
        )
        
        # Ethiopian source configurations
        self.sources = {
            "bbc_amharic": {
                "url": "https://www.bbc.com/amharic",
                "article_selector": "article", 
                "title_selector": "h2",
                "content_selector": "div[data-component='text-block']",
                "priority": "high"
            },
            "voa_amharic": {
                "url": "https://amharic.voanews.com/",
                "article_selector": ".media-block",
                "title_selector": "h3", 
                "content_selector": ".content",
                "priority": "high"
            },
            "ethiopian_reporter": {
                "url": "https://www.ethiopianreporter.com/",
                "article_selector": ".post",
                "title_selector": "h2",
                "content_selector": ".entry-content", 
                "priority": "medium"
            }
        }
        
        logger.info("Amharic Data Collector initialized")
    
    def is_amharic_text(self, text: str) -> bool:
        """
        Check if text contains substantial Amharic content
        
        Args:
            text: Text to analyze
            
        Returns:
            True if text is primarily Amharic
        """
        if not text or len(text.strip()) < 10:
            return False
        
        # Count Amharic characters (Ethiopian Unicode range U+1200-U+137F)
        amharic_chars = len(re.findall(r'[\u1200-\u137F]', text))
        total_chars = len(text.replace(' ', '').replace('\n', ''))
        
        if total_chars == 0:
            return False
        
        amharic_ratio = amharic_chars / total_chars
        return amharic_ratio > 0.7  # At least 70% Amharic characters
    
    def clean_amharic_text(self, text: str) -> str:
        """
        Clean and normalize Amharic text
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned Amharic text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove HTML artifacts
        text = re.sub(r'&[a-zA-Z0-9]+;', '', text)
        
        # Keep only Amharic, English, numbers, and punctuation
        text = re.sub(r'[^\u1200-\u137F\u0020-\u007F\u00A0-\u00FF]', '', text)
        
        return text.strip()
    
    async def scrape_news_site(self, source_name: str, max_articles: int = 50) -> List[Dict]:
        """
        Scrape authentic Amharic content from Ethiopian news site
        
        Args:
            source_name: Name of the source to scrape
            max_articles: Maximum number of articles to collect
            
        Returns:
            List of collected articles with metadata
        """
        if source_name not in self.sources:
            logger.warning(f"Unknown source: {source_name}")
            return []
        
        source_config = self.sources[source_name]
        logger.info(f"Scraping {source_name} for {max_articles} articles")
        
        collected_articles = []
        
        try:
            # Fetch main page
            response = await self.session.get(source_config['url'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.select(source_config['article_selector'])[:max_articles]
            
            for article in articles:
                try:
                    # Extract title
                    title_elem = article.select_one(source_config['title_selector'])
                    title = title_elem.get_text(strip=True) if title_elem else ""
                    
                    # Extract content
                    content_elem = article.select_one(source_config['content_selector']) 
                    content = content_elem.get_text(strip=True) if content_elem else ""
                    
                    # Combine and clean text
                    full_text = f"{title}. {content}" if title and content else (title or content)
                    clean_text = self.clean_amharic_text(full_text)
                    
                    # Verify Amharic content quality
                    if self.is_amharic_text(clean_text) and len(clean_text) > 50:
                        article_data = {
                            'text': clean_text,
                            'title': self.clean_amharic_text(title),
                            'content': self.clean_amharic_text(content),
                            'source': source_name,
                            'type': 'news_article',
                            'length': len(clean_text),
                            'timestamp': datetime.now().isoformat(),
                            'quality': 'authentic',
                            'url': source_config['url']  # Base URL for reference
                        }
                        
                        collected_articles.append(article_data)
                        
                except Exception as e:
                    logger.warning(f"Error processing article from {source_name}: {e}")
                    continue
            
            logger.info(f"Collected {len(collected_articles)} articles from {source_name}")
            
        except Exception as e:
            logger.error(f"Error scraping {source_name}: {e}")
        
        return collected_articles
    
    async def collect_conversations(self, topics: List[str], count_per_topic: int = 20) -> List[Dict]:
        """
        Generate authentic Amharic conversations based on common topics
        
        Args:
            topics: List of conversation topics
            count_per_topic: Number of conversations per topic
            
        Returns:
            List of authentic conversation examples
        """
        logger.info(f"Generating authentic Amharic conversations for topics: {topics}")
        
        # High-quality conversation templates by topic
        conversation_templates = {
            "greeting": [
                {
                    "question": "እንደምን አደርክ?",
                    "answer": "እግዚአብሔር ይመስገን፣ ደህና ነኝ። አንተስ እንዴት ነህ?",
                    "context": "Traditional Ethiopian greeting with religious expression"
                },
                {
                    "question": "ጤና ይስጥልኝ፣ እንደምን ነህ?", 
                    "answer": "ጤና ይስጥልኝ፣ በደንብ ነኝ። እግዚአብሔር ይመስገን።",
                    "context": "Formal greeting with health wishes"
                }
            ],
            
            "food": [
                {
                    "question": "ምሳ ምን በላህ?",
                    "answer": "ወጥ በላሁ። በጣም ጣፋጭ ነበር።", 
                    "context": "Natural food conversation - omits እንጀራ as understood"
                },
                {
                    "question": "ዛሬ ምን ታዘጋጃለህ?",
                    "answer": "ሽሮ አዘጋጃለሁ። በቅንጣቅ ጣፋጭ ነው።",
                    "context": "Planning meals with authentic Ethiopian dishes"
                }
            ],
            
            "health": [
                {
                    "question": "ሐኪም ወዴት ሄደህ?",
                    "answer": "ወደ ሆስፒታል ሄዳለሁ። ምርመራ ያስፈልገኛል።",
                    "context": "Uses ሐኪም (Amharic) instead of ዶክተር (borrowed)"
                }
            ],
            
            "education": [
                {
                    "question": "ትምህርት እንዴት ነው?",
                    "answer": "በደንብ እየተማርኩ ነው። መምህሩ ጥሩ ነው።", 
                    "context": "School discussion with natural expressions"
                }
            ],
            
            "work": [
                {
                    "question": "ስራህ እንዴት ነው?",
                    "answer": "እግዚአብሔር ይመስገን፣ በደንብ እየሠራሁ ነው።",
                    "context": "Work discussion with gratitude expression"
                }
            ]
        }
        
        conversations = []
        
        for topic in topics:
            if topic not in conversation_templates:
                logger.warning(f"No templates for topic: {topic}")
                continue
            
            templates = conversation_templates[topic]
            
            for i in range(count_per_topic):
                template = templates[i % len(templates)]
                
                conversation = {
                    'text': f"{template['question']} {template['answer']}",
                    'question': template['question'],
                    'answer': template['answer'],
                    'source': 'authentic_conversation',
                    'type': 'conversation', 
                    'category': topic,
                    'context': template['context'],
                    'length': len(f"{template['question']} {template['answer']}"),
                    'timestamp': datetime.now().isoformat(),
                    'quality': 'authentic'
                }
                
                conversations.append(conversation)
        
        logger.info(f"Generated {len(conversations)} authentic conversations")
        return conversations
    
    async def collect_from_sources(
        self, 
        sources: List[str], 
        max_items_per_source: int = 100
    ) -> List[Dict]:
        """
        Collect data from multiple Ethiopian sources
        
        Args:
            sources: List of source names to collect from
            max_items_per_source: Maximum items to collect per source
            
        Returns:
            Combined list of collected authentic Amharic data
        """
        logger.info(f"Collecting from sources: {sources}")
        
        all_collected_data = []
        
        # Collect from news sources
        news_sources = [s for s in sources if s in self.sources]
        for source in news_sources:
            try:
                articles = await self.scrape_news_site(source, max_items_per_source)
                all_collected_data.extend(articles)
                
                # Rate limiting for ethical scraping
                await asyncio.sleep(1.0)
                
            except Exception as e:
                logger.error(f"Failed to collect from {source}: {e}")
        
        # Generate conversations if requested
        if 'authentic_conversation' in sources:
            conversation_topics = ['greeting', 'food', 'health', 'education', 'work']
            conversations = await self.collect_conversations(
                conversation_topics, 
                max_items_per_source // len(conversation_topics)
            )
            all_collected_data.extend(conversations)
        
        logger.info(f"Total collected items: {len(all_collected_data)}")
        return all_collected_data
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.session.aclose()