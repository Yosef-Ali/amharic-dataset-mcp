"""
Amharic Quality Scorer

This module provides tools for scoring the quality of Amharic text data
across multiple linguistic and cultural dimensions.
"""

import re
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class AmharicQualityScorer:
    """Scorer for Amharic text quality across multiple dimensions"""
    
    def __init__(self):
        """Initialize the Amharic quality scorer"""
        # Quality scoring weights
        self.weights = {
            "amharic_character_ratio": 0.3,
            "sentence_structure": 0.2,
            "authenticity": 0.25,
            "complexity": 0.15,
            "coherence": 0.1
        }
        
        # Authentic Amharic words and phrases
        self.authentic_indicators = {
            "religious_expressions": ["እግዚአብሔር", "እግዚአብሔር ይመስገን", "እግዚአብሔር ይባርክ"],
            "cultural_terms": ["እንቁላል", "እንደምን", "አንተስ", "እንዴት", "ጤና", "ደህና"],
            "traditional_greetings": ["እንደምን አደርክ", "ጤና ይስጥልኝ"]
        }
        
        # Common quality issues
        self.quality_issues = {
            "excessive_foreign_terms": ["ዶክተር", "ዩኒቨርሲቲ", "ኮምፒተር", "ቴሌቪዥን"],
            "incomplete_sentences": [r"እንደምን\s*$", r"አንተስ\s*$"],
            "punctuation_issues": [r"[።!?]$", r"[፣;:]"]
        }
        
        logger.info("Amharic Quality Scorer initialized")
    
    def calculate_amharic_character_ratio(self, text: str) -> float:
        """
        Calculate the ratio of Amharic characters in text
        
        Args:
            text: Text to analyze
            
        Returns:
            Ratio of Amharic characters (0.0 to 1.0)
        """
        if not text:
            return 0.0
        
        # Count Amharic characters (Ethiopian Unicode range U+1200-U+137F)
        amharic_chars = len(re.findall(r'[\\u1200-\\u137F]', text))
        total_chars = len(text.replace(' ', '').replace('\\n', ''))
        
        if total_chars == 0:
            return 0.0
        
        return amharic_chars / total_chars
    
    def evaluate_sentence_structure(self, text: str) -> Dict:
        """
        Evaluate sentence structure quality
        
        Args:
            text: Text to evaluate
            
        Returns:
            Dictionary with structure evaluation metrics
        """
        sentences = re.split(r'[።!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return {
                "avg_sentence_length": 0,
                "properly_terminated": 0,
                "structure_score": 0.0
            }
        
        # Average sentence length in characters
        avg_length = sum(len(s) for s in sentences) / len(sentences)
        
        # Check for proper sentence termination
        properly_terminated = len([s for s in sentences if re.search(r'[።!?]$', s + ' ')])
        termination_ratio = properly_terminated / len(sentences) if sentences else 0
        
        # Score based on optimal sentence length (50-200 chars is good for Amharic)
        if avg_length < 30:
            length_score = avg_length / 30
        elif avg_length <= 200:
            length_score = 1.0
        else:
            length_score = max(0, 1.0 - (avg_length - 200) / 300)
        
        structure_score = (length_score * 0.7) + (termination_ratio * 0.3)
        
        return {
            "avg_sentence_length": avg_length,
            "properly_terminated": termination_ratio,
            "structure_score": structure_score
        }
    
    def assess_authenticity(self, text: str) -> float:
        """
        Assess the authenticity of Amharic text
        
        Args:
            text: Text to assess
            
        Returns:
            Authenticity score (0.0 to 1.0)
        """
        score = 0.0
        max_score = 0.0
        
        # Check for authentic expressions
        for category, expressions in self.authentic_indicators.items():
            category_score = 0.0
            max_category_score = len(expressions) * 0.1
            
            for expression in expressions:
                if expression in text:
                    category_score += 0.1
            
            score += category_score
            max_score += max_category_score
        
        # Penalize for foreign terms
        foreign_penalty = 0.0
        for term in self.quality_issues["excessive_foreign_terms"]:
            if term in text:
                foreign_penalty += 0.05
        
        score = max(0.0, score - foreign_penalty)
        max_score = max(max_score, 1.0)
        
        return min(1.0, score / max_score) if max_score > 0 else 0.0
    
    def evaluate_complexity(self, text: str) -> Dict:
        """
        Evaluate text complexity
        
        Args:
            text: Text to evaluate
            
        Returns:
            Dictionary with complexity metrics
        """
        if not text:
            return {"avg_word_length": 0, "complexity_score": 0.0}
        
        # Split into words (Amharic words are typically space-separated)
        words = text.split()
        words = [w.strip() for w in words if w.strip()]
        
        if not words:
            return {"avg_word_length": 0, "complexity_score": 0.0}
        
        # Average word length
        avg_word_length = sum(len(w) for w in words) / len(words)
        
        # Complexity score (optimal Amharic word length is around 3-6 characters)
        if avg_word_length <= 2:
            complexity_score = avg_word_length / 2
        elif avg_word_length <= 6:
            complexity_score = 1.0
        else:
            complexity_score = max(0, 1.0 - (avg_word_length - 6) / 10)
        
        return {
            "avg_word_length": avg_word_length,
            "complexity_score": complexity_score
        }
    
    def calculate_overall_quality_score(self, text: str) -> Dict:
        """
        Calculate overall quality score for Amharic text
        
        Args:
            text: Amharic text to score
            
        Returns:
            Dictionary with detailed quality analysis
        """
        logger.info("Calculating overall quality score for Amharic text")
        
        # Calculate component scores
        amharic_ratio = self.calculate_amharic_character_ratio(text)
        structure_metrics = self.evaluate_sentence_structure(text)
        authenticity_score = self.assess_authenticity(text)
        complexity_metrics = self.evaluate_complexity(text)
        
        # Calculate weighted overall score
        weighted_score = (
            amharic_ratio * self.weights["amharic_character_ratio"] +
            structure_metrics["structure_score"] * self.weights["sentence_structure"] +
            authenticity_score * self.weights["authenticity"] +
            complexity_metrics["complexity_score"] * self.weights["complexity"] +
            0.8 * self.weights["coherence"]  # Default coherence for now
        )
        
        # Determine quality category
        if weighted_score >= 0.8:
            quality_category = "excellent"
        elif weighted_score >= 0.6:
            quality_category = "good"
        elif weighted_score >= 0.4:
            quality_category = "fair"
        else:
            quality_category = "poor"
        
        # Generate recommendations
        recommendations = []
        if amharic_ratio < 0.7:
            recommendations.append("Increase Amharic character ratio")
        if structure_metrics["structure_score"] < 0.6:
            recommendations.append("Improve sentence structure")
        if authenticity_score < 0.5:
            recommendations.append("Use more authentic Amharic expressions")
        if complexity_metrics["complexity_score"] < 0.5:
            recommendations.append("Adjust text complexity")
        
        result = {
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "overall_score": round(weighted_score, 3),
            "quality_category": quality_category,
            "component_scores": {
                "amharic_character_ratio": round(amharic_ratio, 3),
                "sentence_structure": round(structure_metrics["structure_score"], 3),
                "authenticity": round(authenticity_score, 3),
                "complexity": round(complexity_metrics["complexity_score"], 3),
                "coherence": 0.8  # Placeholder
            },
            "component_metrics": {
                "sentence_structure_details": structure_metrics,
                "complexity_details": complexity_metrics
            },
            "recommendations": recommendations
        }
        
        logger.info(f"Quality score calculated: {weighted_score:.3f}")
        return result