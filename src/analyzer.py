"""Analyze parsed WhatsApp messages."""
from collections import defaultdict, Counter
from datetime import datetime
from typing import List, Dict


class ChatAnalyzer:
    def __init__(self, messages: List[Dict]):
        self.messages = messages
    
    def count_phrase(self, phrase: str, case_sensitive: bool = False) -> Dict:
        """Count occurrences of a phrase per month and track when it was said."""
        phrase_lower = phrase if case_sensitive else phrase.lower()
        
        # Monthly counts
        monthly_counts = defaultdict(int)
        
        # Detailed occurrences (date and time)
        occurrences = []
        
        for msg in self.messages:
            message_text = msg['message'] if case_sensitive else msg['message'].lower()
            
            if phrase_lower in message_text:
                # Count occurrences in this message
                count = message_text.count(phrase_lower)
                
                # Get year-month key
                year_month = msg['datetime'].strftime('%Y-%m')
                monthly_counts[year_month] += count
                
                # Store each occurrence
                for _ in range(count):
                    occurrences.append({
                        'datetime': msg['datetime'],
                        'sender': msg['sender']
                    })
        
        # Sort monthly counts by date
        sorted_monthly = dict(sorted(monthly_counts.items()))
        
        return {
            'phrase': phrase,
            'total_count': sum(monthly_counts.values()),
            'monthly_counts': sorted_monthly,
            'occurrences': sorted(occurrences, key=lambda x: x['datetime'])
        }
    
    def get_summary(self, phrase: str, case_sensitive: bool = False) -> str:
        """Generate a text summary of phrase usage."""
        analysis = self.count_phrase(phrase, case_sensitive)
        
        summary = f"Summary for phrase: '{phrase}'\n"
        summary += f"{'='*50}\n"
        summary += f"Total occurrences: {analysis['total_count']}\n\n"
        
        summary += "Monthly breakdown:\n"
        for month, count in analysis['monthly_counts'].items():
            summary += f"  {month}: {count} times\n"
        
        return summary