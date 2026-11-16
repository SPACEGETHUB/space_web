#!/usr/bin/env python3
import os

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    
    pdf_path = os.path.expanduser("~/space_web/handbook/SPACE_Master_Handbook.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        spaceAfter=12,
        alignment=1
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=8
    )
    
    story.append(Paragraph("S.P.A.C.E. MASTER OPERATIONAL HANDBOOK", title_style))
    story.append(Paragraph("<b>Architect:</b> Michael C. Sims | <b>Enterprise:</b> Systematic Properties An Artisan Collective Enterprise", body_style))
    story.append(Spacer(1, 15))
    
    md_path = os.path.expanduser("~/space_web/handbook/SPACE_MASTER_HANDBOOK.md")
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    story.append(Spacer(1, 10))
                    story.append(Paragraph(f"<b>{line[2:]}</b>", styles['Heading2']))
                elif line.startswith("## "):
                    story.append(Spacer(1, 8))
                    story.append(Paragraph(f"<b>{line[3:]}</b>", styles['Heading3']))
                elif line.startswith("- "):
                    story.append(Paragraph(f"• {line[2:]}", body_style))
                elif line:
                    story.append(Paragraph(line, body_style))
                    
    doc.build(story)
    print(f"[✓] [Vector 6] Master Handbook PDF successfully compiled: {pdf_path}")
except ImportError:
    print("[!] ReportLab not installed. Markdown master handbook successfully generated and ready.")
