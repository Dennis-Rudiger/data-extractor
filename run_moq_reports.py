import os
import json

def generate_branch_reports():
    with open('generate_moq_report.py', 'r', encoding='utf-8-sig') as f:
        master_code = f.read()
        
    replacements = {
        "def load_data():\n    with open('moq_analysis.json', 'r') as f:\n        return json.load(f)": "def load_data():\n    with open(FILE_IN, 'r') as f:\n        return json.load(f)",
        "BOMAS HARDWARE — MOQ REPORT": "BRANCH_TITLE HARDWARE — MOQ REPORT",
        "BOMAS Hardware Store": "BRANCH_NAME Hardware Store",
        "48 Working Days": "76 Working Days",
        "4 weeks × 6 days": "13 weeks × 6 days",
        "24 working days": "76 working days",
        "÷ 24": "÷ 76",
        "Jan-Feb 2026": "Feb-Apr 2026",
        "Jan 1 - Feb 28, 2026": "Feb 1 - Apr 30, 2026",
        "comparison = build_jan_feb_comparison()": "comparison = None",
        "'moq_report.pdf'": "FILE_OUT_PDF",
        "'moq_report.docx'": "FILE_OUT_DOCX"
    }

    for branch in ['Bomas', 'Karen']:
        code = master_code
        for k, v in replacements.items():
            code = code.replace(k, v)
            
        code = code.replace("FILE_IN", f"'moq_analysis_{branch.lower()}_feb_apr.json'")
        code = code.replace("BRANCH_TITLE", branch.upper())
        code = code.replace("BRANCH_NAME", branch)
        code = code.replace("FILE_OUT_PDF", f"'moq_report_{branch.lower()}_feb_apr.pdf'")
        code = code.replace("FILE_OUT_DOCX", f"'moq_report_{branch.lower()}_feb_apr.docx'")
        
        script_name = f'run_{branch.lower()}.py'
        with open(script_name, 'w', encoding='utf-8') as f:
            f.write("# -*- coding: utf-8 -*-\n" + code)
            
        print(f"Generating reports for {branch}...")
        os.system(f"python {script_name}")
        
if __name__ == '__main__':
    generate_branch_reports()