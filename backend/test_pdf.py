import pdfplumber
import re

pdf_path = r'c:\Users\zamee\OneDrive\Documentos\GitHub\AI-Patient-Record-Intelligence\backend\uploads\UMNwriteup.pdf'
pdf = pdfplumber.open(pdf_path)
text = ''.join([page.extract_text() or '' for page in pdf.pages])
pdf.close()

print("=== TESTING DATE EXTRACTION ===")
date_patterns = [
    r'Date of (?:Examination|Visit|Encounter|Service)[:\s]+([A-Za-z]+\s+\d{1,2},\s+\d{4})',
    r'Date of (?:Examination|Visit|Encounter|Service)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
    r'^Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
    r'Date[:\s]+([A-Za-z]+\s+\d{1,2},\s+\d{4})'
]
for pattern in date_patterns:
    date_match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if date_match:
        print(f"Pattern: {pattern}")
        print(f"Match: {date_match.group(1)}")
        break
else:
    print("NO DATE FOUND")

print("\n=== TESTING REFERRAL SOURCE ===")
source_match = re.search(r'Referral Source[:\s]+([A-Za-z\s]+)', text, re.IGNORECASE)
if source_match:
    print(f"Referral Source: {source_match.group(1).strip()}")
else:
    print("NO SOURCE FOUND")


