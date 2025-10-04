"""Main entry point for WhatsApp chat analyzer with GUI."""
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
import threading
from src.parser import WhatsAppParser
from src.analyzer import ChatAnalyzer
from src.visualizer import ChatVisualizer


class WhatsAppAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Chat Analyzer")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.chat_file = None
        self.chat_files = []
        self.messages = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="WhatsApp Chat Analyzer", 
            font=("Arial", 18, "bold"),
            fg="#25D366"
        )
        title_label.pack(pady=15)
        
        # File selection frame
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(file_frame, text="Chat Files:", font=("Arial", 10)).pack(side="left")
        
        self.file_label = tk.Label(
            file_frame, 
            text="No files selected", 
            font=("Arial", 9),
            fg="gray"
        )
        self.file_label.pack(side="left", padx=10)
        
        select_btn = tk.Button(
            file_frame,
            text="Browse",
            command=self.select_files,
            bg="#25D366",
            fg="white",
            font=("Arial", 9, "bold"),
            cursor="hand2"
        )
        select_btn.pack(side="right")
        
        # Phrase input frame
        phrase_frame = tk.Frame(self.root)
        phrase_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(phrase_frame, text="Search Phrases (separate with commas):", font=("Arial", 10)).pack(anchor="w")
        
        self.phrase_entry = tk.Entry(phrase_frame, font=("Arial", 11), width=50)
        self.phrase_entry.pack(fill="x", pady=5)
        
        tk.Label(phrase_frame, text="Example: hello, good morning, lol", font=("Arial", 8), fg="gray").pack(anchor="w")
        
        # Case sensitive checkbox
        self.case_sensitive_var = tk.BooleanVar()
        case_check = tk.Checkbutton(
            phrase_frame,
            text="Case sensitive",
            variable=self.case_sensitive_var,
            font=("Arial", 9)
        )
        case_check.pack(anchor="w")
        
        # Analyze button
        analyze_btn = tk.Button(
            self.root,
            text="Analyze",
            command=self.analyze,
            bg="#128C7E",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            width=20,
            height=2
        )
        analyze_btn.pack(pady=15)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate',
            length=300
        )
        
        # Results text area
        results_label = tk.Label(
            self.root,
            text="Results:",
            font=("Arial", 10, "bold")
        )
        results_label.pack(anchor="w", padx=20)
        
        self.results_text = scrolledtext.ScrolledText(
            self.root,
            width=80,
            height=15,
            font=("Courier", 9),
            wrap=tk.WORD
        )
        self.results_text.pack(pady=5, padx=20, fill="both", expand=True)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 9),
            fg="gray",
            anchor="w"
        )
        self.status_label.pack(side="bottom", fill="x", padx=5, pady=5)
    
    def select_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select WhatsApp Chat Export(s)",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_paths:
            self.chat_files = list(file_paths)
            file_count = len(self.chat_files)
            
            if file_count == 1:
                file_name = os.path.basename(self.chat_files[0])
                self.file_label.config(text=file_name, fg="black")
            else:
                self.file_label.config(text=f"{file_count} files selected", fg="black")
            
            self.update_status(f"Loaded: {file_count} file(s)")
            
            # Parse immediately
            self.parse_files()
    
    def parse_files(self):
        try:
            self.update_status("Parsing chat files...")
            all_messages = []
            seen_messages = set()  # To detect duplicates
            
            for i, file_path in enumerate(self.chat_files, 1):
                self.update_status(f"Parsing file {i}/{len(self.chat_files)}...")
                
                parser = WhatsAppParser(file_path)
                messages = parser.parse()
                
                # Add messages while checking for duplicates
                for msg in messages:
                    # Create unique identifier: datetime + sender + message
                    msg_id = (msg['datetime'], msg['sender'], msg['message'])
                    
                    if msg_id not in seen_messages:
                        seen_messages.add(msg_id)
                        all_messages.append(msg)
            
            self.messages = sorted(all_messages, key=lambda x: x['datetime'])
            
            if self.messages:
                duplicate_count = sum(len(WhatsAppParser(f).parse()) for f in self.chat_files) - len(self.messages)
                status_msg = f"✓ Parsed {len(self.messages)} unique messages"
                if duplicate_count > 0:
                    status_msg += f" ({duplicate_count} duplicates removed)"
                
                self.update_status(status_msg)
                self.results_text.delete(1.0, tk.END)
                result_text = f"Successfully parsed {len(self.messages)} unique messages from {len(self.chat_files)} file(s)."
                if duplicate_count > 0:
                    result_text += f"\n{duplicate_count} duplicate messages were removed."
                result_text += "\n\nEnter phrase(s) and click Analyze."
                self.results_text.insert(1.0, result_text)
            else:
                messagebox.showwarning("Warning", "No messages found. Check file format.")
                self.update_status("No messages found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse files:\n{str(e)}")
            self.update_status("Error parsing files")
    
    def analyze(self):
        if not self.chat_files:
            messagebox.showwarning("Warning", "Please select chat file(s) first.")
            return
        
        if not self.messages:
            messagebox.showwarning("Warning", "No messages parsed. Check file format.")
            return
        
        phrase_input = self.phrase_entry.get().strip()
        if not phrase_input:
            messagebox.showwarning("Warning", "Please enter at least one phrase to search for.")
            return
        
        # Run analysis in separate thread to prevent UI freezing
        thread = threading.Thread(target=self.run_analysis, args=(phrase_input,))
        thread.daemon = True
        thread.start()
    
    def run_analysis(self, phrase_input):
        try:
            self.progress.pack(pady=5)
            self.progress.start()
            self.update_status("Analyzing...")
            
            # Split phrases by comma
            phrases = [p.strip() for p in phrase_input.split(',') if p.strip()]
            
            if not phrases:
                self.root.after(0, messagebox.showwarning, "Warning", "No valid phrases found.")
                return
            
            case_sensitive = self.case_sensitive_var.get()
            analyzer = ChatAnalyzer(self.messages)
            
            # Clear results
            self.root.after(0, self.results_text.delete, 1.0, tk.END)
            
            all_results = ""
            all_analyses = []
            
            # Analyze each phrase
            for i, phrase in enumerate(phrases, 1):
                self.update_status(f"Analyzing phrase {i}/{len(phrases)}: {phrase}")
                
                analysis = analyzer.count_phrase(phrase, case_sensitive)
                all_analyses.append(analysis)
                summary = analyzer.get_summary(phrase, case_sensitive)
                
                all_results += summary + "\n"
                
                # Create visualizations
                visualizer = ChatVisualizer(analysis)
                
                os.makedirs('output', exist_ok=True)
                
                safe_phrase = "".join(c if c.isalnum() else "_" for c in phrase)
                monthly_chart = f"output/{safe_phrase}_monthly.png"
                timeline_chart = f"output/{safe_phrase}_timeline.png"
                
                visualizer.plot_monthly_usage(monthly_chart)
                visualizer.plot_timeline(timeline_chart)
                
                all_results += f"Visualizations saved:\n• {monthly_chart}\n• {timeline_chart}\n"
                all_results += "\n" + "="*60 + "\n\n"
            
            # Create master graph if multiple phrases
            if len(all_analyses) > 1:
                self.update_status("Creating master graph...")
                try:
                    master_chart = "output/master_combined_graph.png"
                    ChatVisualizer.plot_master_graph(all_analyses, master_chart)
                    all_results += f"\n{'='*60}\n"
                    all_results += f"MASTER GRAPH (ALL PHRASES COMBINED):\n• {master_chart}\n"
                    all_results += f"{'='*60}\n"
                except Exception as e:
                    print(f"Error creating master graph: {e}")
                    all_results += f"\nError creating master graph: {str(e)}\n"
            
            # Update results
            self.root.after(0, self.results_text.insert, 1.0, all_results)
            
            success_msg = f"Analysis complete for {len(phrases)} phrase(s)!"
            if len(all_analyses) > 1:
                success_msg += "\nMaster graph created combining all phrases."
            
            self.root.after(0, self.update_status, f"✓ {success_msg}")
            self.root.after(0, messagebox.showinfo, "Success", success_msg + "\nCheck the output folder for graphs.")
            
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", f"Analysis failed:\n{str(e)}")
            self.root.after(0, self.update_status, "Error during analysis")
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, self.progress.pack_forget)
    
    def update_status(self, message):
        self.status_label.config(text=message)


def main():
    root = tk.Tk()
    app = WhatsAppAnalyzerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()