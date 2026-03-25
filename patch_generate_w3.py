import pathlib

content = pathlib.Path('generate_march_w1_analysis.py').read_text(encoding='utf-8')

# Global Replace
content = content.replace('w1', 'w3')
content = content.replace('W1', 'W3')
content = content.replace('Week 1', 'Week 3')
content = content.replace('WEEK 1', 'WEEK 3')
content = content.replace('week1', 'week3')
content = content.replace('March 2-7, 2026', 'March 16-21, 2026')
content = content.replace('WEEK_NUM = 1', 'WEEK_NUM = 3')
content = content.replace('0.25', '0.75') # expected 75% end of wk3
content = content.replace('25%', '75%')

pathlib.Path('generate_march_w3_analysis.py').write_text(content, encoding='utf-8')

