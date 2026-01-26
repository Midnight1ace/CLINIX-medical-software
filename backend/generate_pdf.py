from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def create_pdf(text_file, pdf_file):
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    with open(text_file, 'r') as f:
        content = f.read()

    # Split content into paragraphs
    paragraphs = content.split('\n\n')
    for para in paragraphs:
        if para.strip():
            if para.startswith('**') and para.endswith('**'):
                # Bold title
                p = Paragraph(para.strip('*'), styles['Heading2'])
            else:
                p = Paragraph(para, styles['Normal'])
            story.append(p)
            story.append(Spacer(1, 12))

    doc.build(story)

if __name__ == "__main__":
    create_pdf('uploads/sample_H_P.txt', 'uploads/sample_H_P.pdf')