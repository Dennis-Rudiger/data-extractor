import os
import sys

def modify_and_run(branch, branch_title):
    with open('generate_moq_report.py', 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. load_data
    text = text.replace(
        "def load_data():\n    with open('moq_analysis.json', 'r') as f:\n        return json.load(f)",
        f"def load_data():\n    with open('moq_analysis_{branch.lower()}_feb_apr.json', 'r') as f:\n        return json.load(f)"
    )

    text = text.replace("BOMAS HARDWARE — MOQ REPORT", f"{branch_title} HARDWARE — MOQ REPORT")
    text = text.replace("BOMAS Hardware Store", f"{branch} Hardware Store")
    text = text.replace("48 Working Days", "76 Working Days")
    text = text.replace("4 weeks × 6 days", "Feb to Apr")
    text = text.replace("24 working days", "76 working days")
    text = text.replace("÷ 24", "÷ 76")
    text = text.replace("Jan-Feb 2026", "Feb-Apr 2026")
    text = text.replace("Jan 1 - Feb 28, 2026", "Feb 1 - Apr 30, 2026")

    # Disable Jan-Feb comparison since we're generating for Feb-Apr
    text = text.replace("comparison = build_jan_feb_comparison()", "comparison = None")

    # Output file names
    text = text.replace("'moq_report.pdf'", f"'moq_report_{branch.lower()}_feb_apr.pdf'")
    text = text.replace("'moq_report.docx'", f"'moq_report_{branch.lower()}_feb_apr.docx'")

    with open(f'temp_gen_moq_{branch.lower()}.py', 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Running generation for {branch}...")
    os.system(f"python temp_gen_moq_{branch.lower()}.py")

if __name__ == '__main__':
    modify_and_run('Bomas', 'BOMAS')
    modify_and_run('Karen', 'KAREN')
