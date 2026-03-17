import pathlib
import re

content = pathlib.Path('generate_moq_report.py').read_text(encoding='utf-8')

# Change build_jan_feb_comparison signature and logic to use global files
content = content.replace(\"def build_jan_feb_comparison():\", \"JAN_FILE = 'stock_movement_jan.json'\\nFEB_FILE = 'stock_movement_feb.json'\\n\\ndef build_jan_feb_comparison():\")
content = content.replace(\"'stock_movement_jan.json'\", \"JAN_FILE\")
content = content.replace(\"'stock_movement_feb.json'\", \"FEB_FILE\")

# Wait, maybe don't blindly replace strings, let's substitute more accurately.
