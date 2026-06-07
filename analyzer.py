"""
Analysis engine for Bac Bo Analyzer Bot
Analyzes patterns, trends, and provides recommendations
"""

from typing import List, Dict, Tuple
from collections import Counter, deque
import numpy as np

class BaccaratAnalyzer:
    """Analyzes Baccarat game patterns and trends"""
    
    def __init__(self, min_results: int = 5):
        self.min_results = min_results
        self.result_names = {'B': 'Banco', 'P': 'Jogador', 'T': 'Empate'}
    
    def analyze_patterns(self, results: List[str]) -> Dict:
        """
        Analyze patterns in results
        
        Args:
            results: List of results (B, P, T)
        
        Returns:
            Dictionary with pattern analysis
        """
        if len(results) < self.min_results:
            return {"error": f"Need at least {self.min_results} results"}
        
        patterns = {
            "alternating": self._detect_alternating(results),
            "repeating": self._detect_repeating(results),
            "streaks": self._detect_streaks(results),
            "pairs": self._detect_pairs(results)
        }
        
        return patterns
    
    def _detect_alternating(self, results: List[str]) -> Dict:
        """Detect alternating patterns (B-P-B-P or similar)"""
        if len(results) < 2:
            return {"found": False, "sequences": []}
        
        alternating_sequences = []
        current_seq = [results[0]]
        
        for i in range(1, len(results)):
            if results[i] != results[i-1]:
                current_seq.append(results[i])
            else:
                if len(current_seq) >= 3:
                    alternating_sequences.append(current_seq)
                current_seq = [results[i]]
        
        if len(current_seq) >= 3:
            alternating_sequences.append(current_seq)
        
        return {
            "found": len(alternating_sequences) > 0,
            "sequences": alternating_sequences,
            "count": len(alternating_sequences)
        }
    
    def _detect_repeating(self, results: List[str]) -> Dict:
        """Detect repeating patterns"""
        pattern_lengths = [2, 3, 4]
        found_patterns = []
        
        for length in pattern_lengths:
            for i in range(len(results) - length * 2 + 1):
                pattern = tuple(results[i:i+length])
                next_pattern = tuple(results[i+length:i+length*2])
                
                if pattern == next_pattern:
                    found_patterns.append({
                        "pattern": list(pattern),
                        "length": length,
                        "position": i
                    })
        
        return {
            "found": len(found_patterns) > 0,
            "patterns": found_patterns,
            "count": len(found_patterns)
        }
    
    def _detect_streaks(self, results: List[str]) -> Dict:
        """Detect consecutive same results (streaks)"""
        streaks = []
        current_result = results[0]
        current_count = 1
        
        for i in range(1, len(results)):
            if results[i] == current_result:
                current_count += 1
            else:
                if current_count >= 2:
                    streaks.append({
                        "result": self.result_names[current_result],
                        "count": current_count
                    })
                current_result = results[i]
                current_count = 1
        
        if current_count >= 2:
            streaks.append({
                "result": self.result_names[current_result],
                "count": current_count
            })
        
        return {
            "found": len(streaks) > 0,
            "streaks": streaks,
            "longest": max([s["count"] for s in streaks]) if streaks else 0
        }
    
    def _detect_pairs(self, results: List[str]) -> Dict:
        """Detect pair patterns (B-P or P-T pairs)"""
        pairs = []
        
        for i in range(len(results) - 1):
            pair = (results[i], results[i+1])
            pairs.append(pair)
        
        pair_counts = Counter(pairs)
        most_common = pair_counts.most_common(5)
        
        return {
            "total_pairs": len(pairs),
            "unique_pairs": len(pair_counts),
            "most_common": [
                {
                    "pair": [self.result_names[p[0]], self.result_names[p[1]]],
                    "count": count
                }
                for p, count in most_common
            ]
        }
    
    def predict_next(self, results: List[str]) -> Dict:
        """
        Predict next result based on patterns
        
        Args:
            results: List of recent results
        
        Returns:
            Prediction with confidence
        """
        if len(results) < 2:
            return {"prediction": "B", "confidence": 0, "reason": "Insufficient data"}
        
        # Check for patterns in last 10 results
        recent = results[-10:] if len(results) >= 10 else results
        
        # Predict based on last result
        last_result = results[-1]
        counter = Counter(recent)
        
        # Get least common (should win next by probability)
        least_common = counter.most_common()[-1]
        
        # Simple strategy: predict opposite of last
        opposite = {'B': 'P', 'P': 'B', 'T': 'B'}
        
        return {
            "prediction": opposite[last_result],
            "reason": f"Opposite of last result ({self.result_names[last_result]})",
            "confidence": 45
        }
    
    def get_statistics(self, results: List[str]) -> Dict:
        """Get detailed statistics"""
        if not results:
            return {"error": "No results"}
        
        total = len(results)
        counter = Counter(results)
        
        return {
            "total_results": total,
            "banker": {
                "count": counter.get('B', 0),
                "percentage": round((counter.get('B', 0) / total) * 100, 2)
            },
            "player": {
                "count": counter.get('P', 0),
                "percentage": round((counter.get('P', 0) / total) * 100, 2)
            },
            "tie": {
                "count": counter.get('T', 0),
                "percentage": round((counter.get('T', 0) / total) * 100, 2)
            }
        }
    
    def generate_recommendation(self, results: List[str]) -> str:
        """Generate a recommendation based on analysis"""
        if len(results) < self.min_results:
            return "Não há dados suficientes para análise"
        
        stats = self.get_statistics(results)
        prediction = self.predict_next(results)
        
        banker_pct = stats["banker"]["percentage"]
        player_pct = stats["player"]["percentage"]
        tie_pct = stats["tie"]["percentage"]
        
        recommendation = "📊 **Recomendação Baseada em Análise:**\n\n"
        
        # Analyze probabilities
        if banker_pct > 55:
            recommendation += "🏦 **Banco** está em alta (acima de 55%)\n"
        elif player_pct > 55:
            recommendation += "👤 **Jogador** está em alta (acima de 55%)\n"
        
        # Add prediction
        rec_name = self.result_names[prediction["prediction"]]
        recommendation += f"🎯 Próximo provável: {rec_name}\n"
        recommendation += f"💡 Razão: {prediction['reason']}\n"
        
        return recommendation