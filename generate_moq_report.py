import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch, cm
from datetime import datetime

def load_data():
    with open('moq_analysis.json', 'r') as f:
        return json.load(f)

class MOQReport:
    def __init__(self, filename='moq_report.pdf'):
        self.filename = filename
        self.page_width, self.page_height = A4
        self.margin = 0.5 * inch
        self.usable_width = self.page_width - 2 * self.margin
        self.setup_styles()
        
    def setup_styles(self):
        self.styles = {
            'title': ParagraphStyle('Title', fontSize=14, textColor=colors.HexColor('#1a5276'), 
                                    alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=2),
            'subtitle': ParagraphStyle('Subtitle', fontSize=9, textColor=colors.HexColor('#566573'), 
                                       alignment=TA_CENTER, spaceAfter=6),
            'heading': ParagraphStyle('Heading', fontSize=11, textColor=colors.HexColor('#1a5276'), 
                                      fontName='Helvetica-Bold', spaceAfter=4, spaceBefore=8),
            'small': ParagraphStyle('Small', fontSize=7, textColor=colors.HexColor('#7f8c8d'), spaceAfter=2),
        }
    
    def header_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 9)
        canvas.setFillColor(colors.HexColor('#1a5276'))
        canvas.drawString(self.margin, self.page_height - 0.35*inch, 'MOQ REPORT - JANUARY 2026 (24 Working Days) | Formula: 6 x Daily Consumption')
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor('#7f8c8d'))
        canvas.drawRightString(self.page_width - self.margin, self.page_height - 0.35*inch, f'Page {doc.page}')
        canvas.setStrokeColor(colors.HexColor('#1a5276'))
        canvas.setLineWidth(0.5)
        canvas.line(self.margin, self.page_height - 0.45*inch, self.page_width - self.margin, self.page_height - 0.45*inch)
        canvas.restoreState()
    
    def get_table_style(self, header_color='#2c3e50'):
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(header_color)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ALIGN', (0, 0), (1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, 0), 5),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ('TOPPADDING', (0, 1), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#d5d8dc')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ])
    
    def generate(self):
        data = load_data()
        
        doc = BaseDocTemplate(self.filename, pagesize=A4,
                             topMargin=0.55*inch, bottomMargin=0.4*inch,
                             leftMargin=self.margin, rightMargin=self.margin)
        
        frame = Frame(self.margin, 0.4*inch, self.usable_width, self.page_height - 0.95*inch, id='main')
        template = PageTemplate(id='main', frames=frame, onPage=self.header_footer)
        doc.addPageTemplates([template])
        
        elements = []
        
        # PAGE 1: SUMMARY
        elements.append(Paragraph('INVENTORY MOVEMENT ANALYSIS', self.styles['title']))
        elements.append(Paragraph(f"Period: 24 Working Days (4 weeks x 6 days) | Formula: Daily Avg = Qty Out / 24 | MOQ = Daily Avg x 6", self.styles['subtitle']))
        
        summary = data['summary']
        metrics = [
            ['Total Items', 'Fast Movers', 'Slow Movers', 'Total Qty Out', 'Weekly MOQ'],
            [f"{summary['total_items']:,}", f"{summary['fast_movers']:,}", f"{summary['slow_movers']:,}", 
             f"{summary['total_qty_out']:,.0f}", f"{summary['total_weekly_moq']:,}"]
        ]
        t = Table(metrics, colWidths=[1.2*inch, 1.1*inch, 1.1*inch, 1.2*inch, 1.1*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16a085')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#d5f5e3')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 8))
        
        elements.append(Paragraph('MOQ BY CATEGORY', self.styles['heading']))
        cat_data = [['Category', 'Items', 'Fast', 'Slow', 'Qty Out', 'Weekly MOQ']]
        sorted_cats = sorted(data['categories'].items(), key=lambda x: x[1]['total_qty_out'], reverse=True)
        
        for cat_name, cat_info in sorted_cats:
            if cat_info['total_qty_out'] > 0:
                cat_data.append([cat_name[:22], str(cat_info['total_items']), str(cat_info['fast_movers']), 
                                str(cat_info['slow_movers']), f"{cat_info['total_qty_out']:,.0f}", 
                                f"{cat_info['total_weekly_moq']:,}"])
        
        cat_data.append(['TOTAL', str(summary['total_items']), str(summary['fast_movers']), str(summary['slow_movers']),
                        f"{summary['total_qty_out']:,.0f}", f"{summary['total_weekly_moq']:,}"])
        
        t = Table(cat_data, colWidths=[2.0*inch, 0.6*inch, 0.55*inch, 0.55*inch, 1.0*inch, 1.0*inch])
        style = self.get_table_style('#2c3e50')
        style.add('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#27ae60'))
        style.add('TEXTCOLOR', (0, -1), (-1, -1), colors.white)
        style.add('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
        t.setStyle(style)
        elements.append(t)
        elements.append(PageBreak())
        
        # PAGE 2: TOP 50 FAST MOVERS
        elements.append(Paragraph('TOP 50 FAST MOVING ITEMS', self.styles['heading']))
        fast_data = [['#', 'Code', 'Description', 'Qty Out', 'Daily', 'Wkly MOQ']]
        for i, item in enumerate(data['fast_movers'][:50], 1):
            fast_data.append([str(i), item['item_code'], item['item_description'][:35],
                f"{item['qty_out']:,.0f}", f"{item['daily_average']:.1f}", 
                f"{item['weekly_moq']:,}"])
        
        t = Table(fast_data, colWidths=[0.35*inch, 0.8*inch, 2.8*inch, 0.8*inch, 0.6*inch, 0.8*inch])
        t.setStyle(self.get_table_style('#e67e22'))
        elements.append(t)
        elements.append(PageBreak())
        
        # PAGE 3: SLOW MOVERS
        elements.append(Paragraph(f'SLOW MOVING ITEMS ({summary["slow_movers"]} items with ZERO sales)', self.styles['heading']))
        elements.append(Paragraph('Stock received but no movement out - review for promotions or discontinuation.', self.styles['small']))
        
        slow_data = [['#', 'Code', 'Description', 'Qty In', 'Category']]
        for i, item in enumerate(data['slow_movers'][:60], 1):
            cat = 'UNKNOWN'
            for cat_name, cat_info in data['categories'].items():
                if any(p['item_code'] == item['item_code'] for p in cat_info['products']):
                    cat = cat_name
                    break
            slow_data.append([str(i), item['item_code'], item['item_description'][:35], f"{item['qty_in']:,.0f}", cat[:20]])
        
        t = Table(slow_data, colWidths=[0.3*inch, 0.75*inch, 2.6*inch, 0.7*inch, 1.65*inch])
        t.setStyle(self.get_table_style('#c0392b'))
        elements.append(t)
        if summary['slow_movers'] > 60:
            elements.append(Paragraph(f"+ {summary['slow_movers'] - 60} more slow-moving items", self.styles['small']))
        elements.append(PageBreak())
        
        # PAGES 4+: CATEGORY DETAILS
        elements.append(Paragraph('DETAILED MOQ BY CATEGORY', self.styles['title']))
        elements.append(Spacer(1, 6))
        
        for cat_name, cat_info in sorted_cats:
            if cat_info['total_qty_out'] == 0:
                continue
            
            header_text = f"{cat_name}  |  {cat_info['total_items']} Items  |  Fast: {cat_info['fast_movers']}  |  Slow: {cat_info['slow_movers']}  |  Weekly MOQ: {cat_info['total_weekly_moq']:,}"
            header_table = Table([[header_text]], colWidths=[self.usable_width])
            header_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(header_table)
            
            products = [p for p in cat_info['products'] if p['qty_out'] > 0][:20]
            if not products:
                elements.append(Spacer(1, 6))
                continue
            
            prod_data = [['Code', 'Description', 'Qty In', 'Qty Out', 'Daily', 'Wkly MOQ']]
            for p in products:
                prod_data.append([p['item_code'], p['item_description'][:32], f"{p['qty_in']:,.0f}", 
                    f"{p['qty_out']:,.0f}", f"{p['daily_average']:.1f}", f"{p['weekly_moq']:,}"])
            
            prod_table = Table(prod_data, colWidths=[0.8*inch, 2.6*inch, 0.7*inch, 0.7*inch, 0.55*inch, 0.8*inch])
            prod_table.setStyle(self.get_table_style('#5d6d7e'))
            elements.append(prod_table)
            
            remaining = len([p for p in cat_info['products'] if p['qty_out'] > 0]) - len(products)
            if remaining > 0:
                elements.append(Paragraph(f"+ {remaining} more items with movement", self.styles['small']))
            elements.append(Spacer(1, 8))
        
        doc.build(elements)
        print(f'Report generated: {self.filename}')

if __name__ == '__main__':
    report = MOQReport('moq_report.pdf')
    report.generate()
