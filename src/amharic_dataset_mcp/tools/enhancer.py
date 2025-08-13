"""
Amharic RAG Enhancer

This module provides tools for enhancing the quality of Amharic text data
using Retrieval-Augmented Generation (RAG) techniques with authentic
Ethiopian linguistic patterns and cultural context.
"""

import re
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class AmharicRAGEnhancer:
    """Enhancer for Amharic text quality using RAG techniques"""
    
    def __init__(self):
        """Initialize the Amharic RAG enhancer"""
        # Amharic linguistic patterns and rules
        self.amharic_patterns = {
            "consonant_variations": {
                "ሀ": ["ሐ", "ኀ"],  # ha variations
                "ሰ": ["ሠ"],      # sa variations
                "ጸ": ["ፀ"],      # tsa variations
            },
            "vowel_omissions": [
                "እንደምን", "አንተስ", "እንዴት"
            ],
            "common_phrases": {
                "እንደምን አደርክ": "እንደምን አደርክ?",
                "አንተስ እንዴት ነህ": "አንተስ እንዴት ነህ?",
                "እግዚአብሔር ይመስገን": "እግዚአብሔር ይመስገን፣"
            }
        }
        
        # Authentic Amharic replacements (preferring native over borrowed words)
        self.authentic_replacements = {
            # Replace borrowed terms with authentic Amharic
            "ዶክተር": "ሐኪም",
            "ሆስፒታል": "መድሃኔ ሕማም",
            "ዩኒቨርሲቲ": "ትምህርት ቤት",
            "ኮምፒተር": "ኮምፒተር",  # Keep as is
            "ቴሌቪዥን": "ቴሌቪዥን",  # Keep as is
        }
        
        logger.info("Amharic RAG Enhancer initialized")
    
    def identify_quality_issues(self, text: str) -> List[Dict]:
        """
        Identify potential quality issues in Amharic text
        
        Args:
            text: Amharic text to analyze
            
        Returns:
            List of identified issues with locations
        """
        issues = []
        
        # Check for punctuation issues
        if not re.search(r'[።!?]$', text.strip()):
            issues.append({
                "type": "punctuation",
                "description": "Missing sentence-ending punctuation",
                "position": len(text),
                "suggestion": "Add appropriate punctuation (።, !, or ?)"
            })
        
        # Check for common phrase patterns
        for pattern, suggestion in self.amharic_patterns["common_phrases"].items():
            if pattern in text and suggestion not in text:
                issues.append({
                    "type": "phrase_completion",
                    "description": f"Incomplete common phrase: {pattern}",
                    "position": text.find(pattern),
                    "suggestion": f"Consider using: {suggestion}"
                })
        
        # Check for vowel omissions
        for omission in self.amharic_patterns["vowel_omissions"]:
            if omission in text:
                issues.append({
                    "type": "vowel_omission",
                    "description": f"Possible vowel omission: {omission}",
                    "position": text.find(omission),
                    "suggestion": "Verify if vowel is intentionally omitted or missing"
                })
        
        return issues
    
    def apply_authenticity_enhancements(self, text: str) -> str:
        """
        Apply enhancements to make text more authentically Amharic
        
        Args:
            text: Text to enhance
            
        Returns:
            Enhanced text with authentic Amharic elements
        """
        enhanced_text = text
        
        # Apply authentic replacements
        for borrowed, authentic in self.authentic_replacements.items():
            enhanced_text = re.sub(r'\b' + re.escape(borrowed) + r'\b', authentic, enhanced_text)
        
        # Apply common phrase corrections
        for pattern, correction in self.amharic_patterns["common_phrases"].items():
            enhanced_text = enhanced_text.replace(pattern, correction)
        
        return enhanced_text
    
    def enhance_amharic_text(self, text: str, context_category: str = "general") -> Dict:
        """
        Enhance Amharic text quality using RAG-based techniques
        
        Args:
            text: Amharic text to enhance
            context_category: Context category for enhancement
            
        Returns:
            Dictionary with enhanced text and change details
        """
        logger.info(f"Enhancing Amharic text with context: {context_category}")
        
        original_text = text
        changes_made = []
        
        # Identify issues
        issues = self.identify_quality_issues(text)
        
        # Apply enhancements
        enhanced_text = self.apply_authenticity_enhancements(text)
        
        # Track changes
        if enhanced_text != original_text:
            changes_made.append({
                "type": "authenticity_enhancement",
                "description": "Applied authentic Amharic replacements",
                "original": original_text,
                "enhanced": enhanced_text
            })
        
        # Add sentence-ending punctuation if missing
        if not re.search(r'[።!?]$', enhanced_text.strip()) and enhanced_text.strip():
            enhanced_text = enhanced_text.strip() + "።"
            changes_made.append({
                "type": "punctuation",
                "description": "Added sentence-ending punctuation",
                "original": original_text,
                "enhanced": enhanced_text
            })
        
        result = {
            "original_text": original_text,
            "enhanced_text": enhanced_text,
            "context_category": context_category,
            "changes_made": changes_made,
            "quality_issues_identified": issues,
            "enhancement_score": len(changes_made) / (len(original_text) or 1)  # Simple ratio
        }
        
        logger.info(f"Enhanced text. Changes made: {len(changes_made)}")
        return result