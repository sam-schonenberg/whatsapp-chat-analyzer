# WhatsApp Chat Analyzer

A Python application with GUI to analyze exported WhatsApp chats and visualize phrase usage patterns over time.

## Features

- 📊 **Monthly Usage Analysis** - Track how often specific phrases appear each month
- 📈 **Timeline Visualization** - See exactly when phrases were used most frequently
- 🔍 **Multiple Phrase Support** - Analyze multiple phrases simultaneously
- 📉 **Master Graph** - Combined visualization of all phrases
- 🔄 **Multiple File Support** - Merge and analyze multiple chat exports
- 🎯 **Case Sensitivity Option** - Choose between case-sensitive and case-insensitive searches
- 🖥️ **User-Friendly GUI** - Easy-to-use graphical interface

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd whatsapp-chat-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Export your WhatsApp chat**
   - Open WhatsApp and go to the chat you want to analyze
   - Tap on the three dots (⋮) > More > Export chat
   - Choose "Without Media"
   - Save the `.txt` file

2. **Run the application**
   ```bash
   python main.py
   ```

3. **Analyze your chat**
   - Click **Browse** to select one or more exported chat files
   - Enter phrase(s) to search for (separate multiple phrases with commas)
   - Optionally enable **Case sensitive** matching
   - Click **Analyze**

4. **View results**
   - Results appear in the application window
   - Graphs are saved to the `output/` directory:
     - `<phrase>_monthly.png` - Monthly bar chart
     - `<phrase>_timeline.png` - Timeline scatter plot
     - `master_combined_graph.png` - Combined stacked bar chart (for multiple phrases)

## Examples

**Single phrase analysis:**
```
hello
```

**Multiple phrases:**
```
good morning, lol, thank you
```

## Supported Chat Formats

The parser supports multiple WhatsApp export formats:
- `[DD/MM/YYYY, HH:MM:SS] Name: Message`
- `DD/MM/YYYY, H:MM am/pm - Name: Message`
- `DD/MM/YYYY, HH:MM - Name: Message`
- `[DD.MM.YY, HH:MM:SS] Name: Message` (German format)

## Project Structure

```
whatsapp-chat-analyzer/
├── data/              # Place your exported chat files here (gitignored)
├── output/            # Generated graphs are saved here (gitignored)
├── src/
│   ├── __init__.py
│   ├── parser.py      # WhatsApp chat file parser
│   ├── analyzer.py    # Message analysis and phrase counting
│   └── visualizer.py  # Graph generation with matplotlib
├── main.py            # GUI application entry point
├── requirements.txt   # Python dependencies
├── .gitignore
└── README.md
```

## Requirements

- Python 3.7+
- matplotlib
- pandas
- tkinter (usually included with Python)

## Notes

- System messages (e.g., "Messages are end-to-end encrypted") are automatically filtered out
- Duplicate messages across multiple files are automatically removed
- Multi-line messages are properly handled

## License

This project is open source and available for personal use.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.