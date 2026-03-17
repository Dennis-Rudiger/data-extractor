import pathlib
p = pathlib.Path('generate_branch_reports.py')
content = p.read_text(encoding='utf-8')

old_main = '''for branch in ['bomas', 'karen']:'''
new_main = '''import generate_moq_report

for branch in ['bomas', 'karen']:
    if branch == 'bomas':
        generate_moq_report.JAN_FILE = 'stock_movement_jan.json'
        generate_moq_report.FEB_FILE = 'stock_movement_feb.json'
    else:
        generate_moq_report.JAN_FILE = 'stock_movement_karen_jan.json'
        generate_moq_report.FEB_FILE = 'stock_movement_karen_feb.json'
'''
content = content.replace(old_main, new_main)
p.write_text(content, encoding='utf-8')
