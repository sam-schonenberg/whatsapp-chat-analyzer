"""Parse WhatsApp chat export files."""
import re
from datetime import datetime
from typing import List, Dict


class WhatsAppParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.messages = []
    
    def parse(self) -> List[Dict]:
        """Parse WhatsApp chat file and return list of messages."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Multiple WhatsApp format patterns to try
        patterns = [
            # [DD/MM/YYYY, HH:MM:SS] Name: Message
            (r'^\[(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}:\d{2})\]\s([^:]+):\s(.+)$', 
             [("%d/%m/%Y", "%H:%M:%S"), ("%d/%m/%y", "%H:%M:%S")]),
            
            # DD/MM/YYYY, H:MM am/pm - Name: Message
            (r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}\s(?:am|pm))\s-\s([^:]+):\s(.+)$',
             [("%d/%m/%Y", "%I:%M %p"), ("%d/%m/%y", "%I:%M %p")]),
            
            # DD/MM/YYYY, HH:MM - Name: Message
            (r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2})\s-\s([^:]+):\s(.+)$',
             [("%d/%m/%Y", "%H:%M"), ("%d/%m/%y", "%H:%M")]),
            
            # [DD.MM.YY, HH:MM:SS] Name: Message (German format)
            (r'^\[(\d{1,2}\.\d{1,2}\.\d{2,4}),\s(\d{1,2}:\d{2}:\d{2})\]\s([^:]+):\s(.+)$',
             [("%d.%m.%Y", "%H:%M:%S"), ("%d.%m.%y", "%H:%M:%S")]),
        ]
        
        current_message = None
        
        for line in lines:
            line = line.rstrip('\n')
            
            # Skip empty lines
            if not line.strip():
                continue
            
            matched = False
            
            # Try each pattern
            for pattern, date_formats in patterns:
                match = re.match(pattern, line)
                
                if match:
                    date_str, time_str, sender, message = match.groups()
                    
                    # Skip system messages
                    if 'end-to-end encrypted' in message.lower() or \
                       'changed their phone number' in message.lower() or \
                       'added you' in message.lower() or \
                       'created group' in message.lower():
                        matched = True
                        break
                    
                    # Try to parse datetime
                    parsed = False
                    for date_fmt, time_fmt in date_formats:
                        try:
                            dt = datetime.strptime(f"{date_str} {time_str}", f"{date_fmt} {time_fmt}")
                            parsed = True
                            
                            # Save previous message if exists
                            if current_message:
                                self.messages.append(current_message)
                            
                            # Start new message
                            current_message = {
                                'datetime': dt,
                                'sender': sender.strip(),
                                'message': message.strip()
                            }
                            
                            matched = True
                            break
                        except ValueError:
                            continue
                    
                    if matched:
                        break
            
            # If line didn't match any pattern, it's a continuation of previous message
            if not matched and current_message:
                current_message['message'] += '\n' + line
        
        # Don't forget the last message
        if current_message:
            self.messages.append(current_message)
        
        return self.messages