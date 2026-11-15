# build_html_doc.py - Generates an identical 35-page print-optimized HTML artifact

def create_html_report(output_path):
    # We will generate a rich HTML document that mirrors the 35 pages of the docx document
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SIMATS Engineering - ITA1439 Ethical Hacking CO3 Assignment 3</title>
<style>
  @page {
    size: A4 portrait;
    margin: 20mm 15mm 20mm 15mm;
    @top-center {
      content: "SIMATS ENGINEERING | ITA1439 ETHICAL HACKING | CO3 - ASSIGNMENT 3";
      font-family: Calibri, sans-serif;
      font-size: 8pt;
      color: #64748B;
      border-bottom: 1px solid #CBD5E1;
    }
    @bottom-center {
      content: "Automated Scan-Data Pipeline & Processing Library | Page " counter(page);
      font-family: Calibri, sans-serif;
      font-size: 8pt;
      color: #64748B;
      border-top: 1px solid #CBD5E1;
    }
  }

  body {
    font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.35;
    color: #1F2937;
    margin: 0;
    padding: 0;
    background: #525659;
  }

  .page-container {
    background: #FFFFFF;
    width: 210mm;
    min-height: 297mm;
    margin: 20px auto;
    padding: 20mm;
    box-sizing: border-box;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    position: relative;
    page-break-after: always;
  }

  @media print {
    body { background: none; }
    .page-container {
      width: 100%;
      min-height: auto;
      margin: 0;
      padding: 0;
      box-shadow: none;
    }
  }

  .header-rule {
    display: flex;
    justify-content: space-between;
    border-bottom: 2px solid #1B365D;
    padding-bottom: 4px;
    margin-bottom: 15px;
    font-size: 8pt;
    font-weight: bold;
    color: #1B365D;
    text-transform: uppercase;
  }

  .footer-rule {
    position: absolute;
    bottom: 15mm;
    left: 20mm;
    right: 20mm;
    display: flex;
    justify-content: space-between;
    border-top: 1px solid #CBD5E1;
    padding-top: 5px;
    font-size: 8pt;
    color: #64748B;
  }

  h1.doc-title {
    color: #1B365D;
    font-size: 24pt;
    text-align: center;
    margin: 15px 0 5px 0;
    font-weight: 800;
    letter-spacing: 0.5px;
  }
  .doc-subtitle {
    color: #475569;
    font-size: 11pt;
    text-align: center;
    font-style: italic;
    margin-bottom: 20px;
  }

  h1 {
    color: #1B365D;
    font-size: 15pt;
    border-bottom: 2px solid #1B365D;
    padding-bottom: 4px;
    margin-top: 10px;
    margin-bottom: 10px;
    font-weight: bold;
  }

  h2 {
    color: #2C4D75;
    font-size: 12pt;
    margin-top: 12px;
    margin-bottom: 6px;
    font-weight: bold;
  }

  h3 {
    color: #334155;
    font-size: 10.5pt;
    margin-top: 8px;
    margin-bottom: 4px;
    font-weight: bold;
  }

  p {
    margin: 4px 0 8px 0;
    text-align: justify;
  }

  ul {
    margin: 4px 0 8px 20px;
    padding: 0;
  }
  li {
    margin-bottom: 4px;
    text-align: justify;
  }

  /* Table styling: All 4 border lines clearly visible */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 14px 0;
    font-size: 8.5pt;
    border: 2px solid #1B365D !important; /* 4 borders prominent */
  }

  th {
    background-color: #1B365D;
    color: #FFFFFF;
    font-weight: bold;
    padding: 6px 8px;
    text-align: left;
    border: 1px solid #1B365D;
    border-bottom: 2px solid #0F172A;
  }

  td {
    padding: 5px 8px;
    border: 1px solid #CBD5E1;
    color: #1F2937;
  }

  tr:nth-child(even) td {
    background-color: #F8FAFC;
  }
  tr:nth-child(odd) td {
    background-color: #FFFFFF;
  }

  pre, code {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8pt;
  }

  pre {
    background-color: #F1F5F9;
    border-left: 4px solid #1B365D;
    border-top: 1px solid #E2E8F0;
    border-right: 1px solid #E2E8F0;
    border-bottom: 1px solid #E2E8F0;
    padding: 8px 10px;
    margin: 6px 0 10px 0;
    overflow-x: auto;
    line-height: 1.25;
    color: #0F172A;
  }

  .callout {
    background-color: #EFF6FF;
    border-left: 4px solid #2563EB;
    border-top: 1px solid #BFDBFE;
    border-right: 1px solid #BFDBFE;
    border-bottom: 1px solid #BFDBFE;
    padding: 8px 12px;
    margin: 8px 0;
    font-size: 9.5pt;
    color: #1E3A8A;
  }
  .callout strong {
    color: #1E40AF;
  }

  .badge-tag {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 7.5pt;
    font-weight: bold;
  }
  .badge-crit { background: #FEE2E2; color: #991B1B; }
  .badge-high { background: #FFEDD5; color: #9A3412; }
  .badge-pass { background: #DCFCE7; color: #166534; }
</style>
</head>
<body>
'''

    # We will build 35 pages matching the exact 35 pages in DocxBuilder
    pages_html = []

    # Read from python objects or generate programmatically
    # Let's import the builder and render each page into HTML
    import doc_engine
    b = doc_engine.DocxBuilder()
    from pages_q1_q2 import build_pages_1_to_13
    from pages_q3_q4 import build_pages_14_to_23
    from pages_q5_q6 import build_pages_24_to_30
    from pages_q7 import build_pages_31_to_35

    # Run builders
    build_pages_1_to_13(b)
    build_pages_14_to_23(b)
    build_pages_24_to_30(b)
    build_pages_31_to_35(b)

    # Let's inspect how many pages were generated
    print(f"DocxBuilder has {b.page_count} pages.")
    
    # Let's write out the HTML content by extracting text and structures
    # A dedicated script converts paragraphs into clean HTML page containers
    from html_converter import convert_paragraphs_to_html
    body_content = convert_paragraphs_to_html(b.paragraphs)

    full_html = html_content + body_content + "\n</body>\n</html>"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generated standalone HTML file: {output_path}")

