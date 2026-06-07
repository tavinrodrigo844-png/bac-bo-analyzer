"""
Database management for Bac Bo Analyzer Bot
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    """Simple JSON-based database for storing game results"""
    
    def __init__(self, filename: str = "baccarat_data.db"):
        self.filename = filename
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load data from file or create new database"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading database: {e}")
                return {"results": [], "stats": {}}
        return {"results": [], "stats": {}}
    
    def _save_data(self):
        """Save data to file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving database: {e}")
    
    def add_result(self, result: str, timestamp: Optional[str] = None) -> bool:
        """
        Add a result to the database
        
        Args:
            result: 'B' (Banker), 'P' (Player), or 'T' (Tie)
            timestamp: Optional timestamp (defaults to current time)
        
        Returns:
            True if successful, False otherwise
        """
        if result not in ['B', 'P', 'T']:
            return False
        
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        self.data["results"].append({
            "result": result,
            "timestamp": timestamp
        })
        
        self._save_data()
        return True
    
    def get_results(self, limit: Optional[int] = None) -> List[str]:
        """
        Get results from database
        
        Args:
            limit: Maximum number of recent results to return
        
        Returns:
            List of results (B, P, or T)
        """
        results = [r["result"] for r in self.data["results"]]
        
        if limit:
            return results[-limit:]
        return results
    
    def get_full_results(self, limit: Optional[int] = None) -> List[Dict]:
        """Get full result data with timestamps"""
        if limit:
            return self.data["results"][-limit:]
        return self.data["results"]
    
    def clear_results(self) -> bool:
        """Clear all results from database"""
        self.data["results"] = []
        self._save_data()
        return True
    
    def get_statistics(self) -> Dict:
        """Calculate and return statistics"""
        results = self.get_results()
        
        if not results:
            return {
                "total": 0,
                "banker": 0,
                "player": 0,
                "tie": 0,
                "banker_percent": 0,
                "player_percent": 0,
                "tie_percent": 0
            }
        
        total = len(results)
        banker_count = results.count('B')
        player_count = results.count('P')
        tie_count = results.count('T')
        
        return {
            "total": total,
            "banker": banker_count,
            "player": player_count,
            "tie": tie_count,
            "banker_percent": round((banker_count / total) * 100, 2),
            "player_percent": round((player_count / total) * 100, 2),
            "tie_percent": round((tie_count / total) * 100, 2)
        }
    
    def get_streak(self) -> Dict:
        """Get current streak information"""
        results = self.get_results()
        
        if not results:
            return {"current": None, "count": 0}
        
        current = results[-1]
        count = 1
        
        for i in range(len(results) - 2, -1, -1):
            if results[i] == current:
                count += 1
            else:
                break
        
        return {"current": current, "count": count}
    
    def export_results(self) -> str:
        """Export results as formatted string"""
        results = self.get_full_results()
        
        if not results:
            return "No results to export"
        
        export = "Baccarat Results Export\n"
        export += "=" * 40 + "\n"
        
        for i, r in enumerate(results, 1):
            result_name = {'B': 'Banker', 'P': 'Player', 'T': 'Tie'}[r['result']]
            export += f"{i}. {result_name} - {r['timestamp']}\n"
        
        return export