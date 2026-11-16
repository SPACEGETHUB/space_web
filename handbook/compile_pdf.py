import os
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    
    pdf_path = os.path.expanduser("~/space_web/handbook/SPACE_Master_Handbook.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    story = [Paragraph("<b>S.P.A.C.E. MASTER HANDBOOK</b>", styles['Heading1']), Spacer(1, 10)]
    
    md_path = os.path.expanduser("~/space_web/handbook/SPACE_MASTER_HANDBOOK.md")
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    story.append(Paragraph(f"<b>{line[2:]}</b>", styles['Heading2']))
                elif line.startswith("- "):
                    story.append(Paragraph(f"• {line[2:]}", styles['Normal']))
    doc.build(story)
    print(f"[✓] PDF Handbook successfully compiled at: {pdf_path}")
except Exception as e:
    print(f"[!] PDF compilation notice (Markdown fallback active): {e}")
