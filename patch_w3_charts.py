import pathlib
content = pathlib.Path('generate_march_w3_analysis.py').read_text(encoding='utf-8')

# 1. Add trend chart generation function after create_rep_bar_chart
anchor_func = "def create_rep_bar_chart"
trend_func = '''
def create_weekly_trend_chart(output_dir="charts/march_w3"):
    os.makedirs(output_dir, exist_ok=True)
    names = [r[0] for r in sorted_reps]
    w1_vals = [w1_rep.get(n, 0) / 1000000 for n in names]
    w2_vals = [w2_rep.get(n, 0) / 1000000 for n in names]
    w3_vals = [r[1]['total_sales'] / 1000000 for r in sorted_reps]

    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(names))
    width = 0.25

    ax.bar(x - width, w1_vals, width, label='Week 1', color='#bdc3c7', edgecolor='white')
    ax.bar(x, w2_vals, width, label='Week 2', color='#7f8c8d', edgecolor='white')
    ax.bar(x + width, w3_vals, width, label='Week 3', color='#3498db', edgecolor='white')

    ax.set_ylabel('Sales (Millions KES)')
    ax.set_title('Sales Trend by Rep (W1 vs W2 vs W3)', fontweight='bold')
    ax.set_xticks(x)
    # Fix the tick warning here
    # ax.set_xticklabels(names, rotation=25, ha='right', fontsize=9)
    ax.set_xticks(x, names, rotation=25, ha='right', fontsize=9)
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    fn = f"{output_dir}/weekly_trends.png"
    plt.savefig(fn, dpi=120, bbox_inches='tight', facecolor='white')
    plt.close()
    return fn

def create_rep_bar_chart
'''
content = content.replace("def create_rep_bar_chart", trend_func, 1)

# 2. Make sure trend chart is generated
anchor_gen = "chart_files = {"
chart_files_addition = '''    chart_files = {
        'trend': create_weekly_trend_chart(),
'''
content = content.replace(anchor_gen, chart_files_addition)

# 3. Add to PDF
anchor_pdf = "if os.path.exists(chart_files['rep_bar']):"
pdf_addition = '''    if os.path.exists(chart_files['trend']):
        elements.append(Paragraph("SALES TREND (W1 vs W2 vs W3)", heading_s))
        elements.append(Image(chart_files['trend'], width=7*inch, height=3*inch))
        elements.append(Spacer(1, 15))
        
    if os.path.exists(chart_files['rep_bar']):
'''
content = content.replace(anchor_pdf, pdf_addition)

# 4. Add to Word
anchor_word = "for chart_key in ['rep_bar', 'margin'"
word_replace = "for chart_key in ['trend', 'rep_bar', 'margin'"
content = content.replace(anchor_word, word_replace)

# Disable matplotlib warning globally for xticks
content = content.replace("ax.set_xticklabels(names,", "ax.set_xticks(x, names,")
content = content.replace("ax.set_xticklabels(cats,", "ax.set_xticks(x, cats,")

pathlib.Path('generate_march_w3_analysis.py').write_text(content, encoding='utf-8')
