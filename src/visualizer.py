"""Create visualizations from analyzed data."""
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for threading
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from typing import Dict, List
from collections import Counter, defaultdict


class ChatVisualizer:
    def __init__(self, analysis: Dict):
        self.analysis = analysis
    
    def plot_monthly_usage(self, output_path: str = None):
        """Create a bar chart showing monthly usage of the phrase."""
        monthly_counts = self.analysis['monthly_counts']
        
        if not monthly_counts:
            print("No data to plot.")
            return
        
        months = list(monthly_counts.keys())
        counts = list(monthly_counts.values())
        
        plt.figure(figsize=(12, 6))
        plt.bar(months, counts, color='#25D366', edgecolor='black', alpha=0.7)
        
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Number of Times Said', fontsize=12)
        plt.title(f"Monthly Usage of '{self.analysis['phrase']}'", fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Monthly chart saved to {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_timeline(self, output_path: str = None):
        """Create a timeline showing exactly when the phrase was said."""
        occurrences = self.analysis['occurrences']
        
        if not occurrences:
            print("No data to plot.")
            return
        
        dates = [occ['datetime'] for occ in occurrences]
        
        # Count occurrences per day
        daily_counts = Counter([d.date() for d in dates])
        plot_dates = list(daily_counts.keys())
        plot_counts = list(daily_counts.values())
        
        plt.figure(figsize=(14, 6))
        plt.scatter(plot_dates, plot_counts, c='#25D366', s=50, alpha=0.6, edgecolors='black')
        plt.plot(plot_dates, plot_counts, color='#128C7E', alpha=0.3, linewidth=1)
        
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Times Said Per Day', fontsize=12)
        plt.title(f"Timeline of '{self.analysis['phrase']}'", fontsize=14, fontweight='bold')
        plt.gcf().autofmt_xdate()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Timeline chart saved to {output_path}")
        else:
            plt.show()
        
        plt.close()
    
    @staticmethod
    def plot_master_graph(analyses: List[Dict], output_path: str = None):
        """Create a master graph combining all phrases' monthly counts."""
        if not analyses:
            print("No data to plot.")
            return
        
        # Collect all unique months
        all_months = set()
        for analysis in analyses:
            all_months.update(analysis['monthly_counts'].keys())
        
        all_months = sorted(list(all_months))
        
        if not all_months:
            print("No monthly data available.")
            return
        
        # Prepare data for stacked bar chart
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Colors for different phrases
        colors = ['#25D366', '#128C7E', '#075E54', '#34B7F1', '#ECE5DD', '#FF6B6B', '#4ECDC4', '#FFE66D']
        
        bottom = [0] * len(all_months)
        
        for i, analysis in enumerate(analyses):
            phrase = analysis['phrase']
            counts = [analysis['monthly_counts'].get(month, 0) for month in all_months]
            
            color = colors[i % len(colors)]
            ax.bar(all_months, counts, bottom=bottom, label=phrase, 
                   color=color, edgecolor='black', alpha=0.8)
            
            # Update bottom for stacking
            bottom = [b + c for b, c in zip(bottom, counts)]
        
        ax.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total Count', fontsize=12, fontweight='bold')
        ax.set_title('Master Graph - Combined Monthly Usage of All Phrases', fontsize=14, fontweight='bold')
        ax.legend(loc='upper left', framealpha=0.9)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Master graph saved to {output_path}")
        else:
            plt.show()
        
        plt.close()