import json
import shutil
import re
import generate_moq_report
from generate_moq_report import MOQReport, MOQReportWord

for branch in ['bomas', 'karen']:
    if branch == 'bomas':
        generate_moq_report.JAN_FILE = 'stock_movement_jan.json'
        generate_moq_report.FEB_FILE = 'stock_movement_feb.json'
    else:
        generate_moq_report.JAN_FILE = 'stock_movement_karen_jan.json'
        generate_moq_report.FEB_FILE = 'stock_movement_karen_feb.json'

    # Overwrite the default config
    with open(f'{branch}_average_moq.json', 'r') as f:
        data = json.load(f)
    with open('moq_analysis.json', 'w') as f:
        json.dump(data, f)
        
    print(f'Generating reports for {branch.upper()}...')
    
    # Generate PDF
    pdf_report = MOQReport(f'{branch}_average_moq.pdf')
    pdf_report.generate()
    
    # Generate Word
    word_report = MOQReportWord(f'{branch}_average_moq.docx')
    word_report.generate()
