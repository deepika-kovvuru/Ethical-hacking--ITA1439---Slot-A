import zipfile
import html
import os

class DocxBuilder:
    def __init__(self):
        self.paragraphs = []
        self.page_count = 1

    def escape(self, text):
        if not text:
            return ""
        return (str(text)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))

    def add_title(self, text, subtitle=None):
        p = f'''<w:p>
  <w:pPr>
    <w:jc w:val="center"/>
    <w:spacing w:before="360" w:after="120" w:line="320" w:lineRule="auto"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:b/>
      <w:sz w:val="44"/>
      <w:color w:val="1B365D"/>
    </w:rPr>
    <w:t>{self.escape(text)}</w:t>
  </w:r>
</w:p>'''
        self.paragraphs.append(p)
        if subtitle:
            p_sub = f'''<w:p>
  <w:pPr>
    <w:jc w:val="center"/>
    <w:spacing w:before="60" w:after="240" w:line="260" w:lineRule="auto"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:i/>
      <w:sz w:val="24"/>
      <w:color w:val="475569"/>
    </w:rPr>
    <w:t>{self.escape(subtitle)}</w:t>
  </w:r>
</w:p>'''
            self.paragraphs.append(p_sub)

    def add_heading_1(self, text):
        p = f'''<w:p>
  <w:pPr>
    <w:spacing w:before="240" w:after="100"/>
    <w:pBdr>
      <w:bottom w:val="single" w:sz="12" w:space="4" w:color="1B365D"/>
    </w:pBdr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:b/>
      <w:sz w:val="30"/>
      <w:color w:val="1B365D"/>
    </w:rPr>
    <w:t>{self.escape(text)}</w:t>
  </w:r>
</w:p>'''
        self.paragraphs.append(p)

    def add_heading_2(self, text):
        p = f'''<w:p>
  <w:pPr>
    <w:spacing w:before="180" w:after="80"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:b/>
      <w:sz w:val="25"/>
      <w:color w:val="2C4D75"/>
    </w:rPr>
    <w:t>{self.escape(text)}</w:t>
  </w:r>
</w:p>'''
        self.paragraphs.append(p)

    def add_heading_3(self, text):
        p = f'''<w:p>
  <w:pPr>
    <w:spacing w:before="140" w:after="60"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:b/>
      <w:sz w:val="22"/>
      <w:color w:val="334155"/>
    </w:rPr>
    <w:t>{self.escape(text)}</w:t>
  </w:r>
</w:p>'''
        self.paragraphs.append(p)

    def add_paragraph(self, text, bold_prefix=None, italic=False):
        runs = []
        if bold_prefix:
            runs.append(f'''<w:r>
  <w:rPr>
    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
    <w:b/>
    <w:sz w:val="21"/>
    <w:color w:val="0F172A"/>
  </w:rPr>
  <w:t xml:space="preserve">{self.escape(bold_prefix)} </w:t>
</w:r>''')
        
        i_tag = "<w:i/>" if italic else ""
        runs.append(f'''<w:r>
  <w:rPr>
    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
    {i_tag}
    <w:sz w:val="21"/>
    <w:color w:val="334155"/>
  </w:rPr>
  <w:t xml:space="preserve">{self.escape(text)}</w:t>
</w:r>''')

        p = f'''<w:p>
  <w:pPr>
    <w:spacing w:before="40" w:after="80" w:line="276" w:lineRule="auto"/>
    <w:jc w:val="both"/>
  </w:pPr>
  {''.join(runs)}
</w:p>'''
        self.paragraphs.append(p)

    def add_bullet(self, text, bold_prefix=None):
        runs = []
        runs.append(f'''<w:r>
  <w:rPr>
    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
    <w:b/>
    <w:sz w:val="21"/>
    <w:color w:val="1B365D"/>
  </w:rPr>
  <w:t xml:space="preserve">&#9679;  </w:t>
</w:r>''')
        if bold_prefix:
            runs.append(f'''<w:r>
  <w:rPr>
    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
    <w:b/>
    <w:sz w:val="21"/>
    <w:color w:val="0F172A"/>
  </w:rPr>
  <w:t xml:space="preserve">{self.escape(bold_prefix)} </w:t>
</w:r>''')
        runs.append(f'''<w:r>
  <w:rPr>
    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
    <w:sz w:val="21"/>
    <w:color w:val="334155"/>
  </w:rPr>
  <w:t xml:space="preserve">{self.escape(text)}</w:t>
</w:r>''')
        p = f'''<w:p>
  <w:pPr>
    <w:ind w:left="360" w:hanging="200"/>
    <w:spacing w:before="30" w:after="60" w:line="260" w:lineRule="auto"/>
    <w:jc w:val="both"/>
  </w:pPr>
  {''.join(runs)}
</w:p>'''
        self.paragraphs.append(p)

    def add_code_block(self, code_lines):
        for line in code_lines:
            p = f'''<w:p>
  <w:pPr>
    <w:shd w:val="clear" w:color="auto" w:fill="F1F5F9"/>
    <w:pBdr>
      <w:left w:val="single" w:sz="18" w:space="8" w:color="1B365D"/>
    </w:pBdr>
    <w:ind w:left="240" w:right="120"/>
    <w:spacing w:before="10" w:after="10" w:line="230" w:lineRule="auto"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>
      <w:sz w:val="17"/>
      <w:color w:val="0F172A"/>
    </w:rPr>
    <w:t xml:space="preserve">{self.escape(line)}</w:t>
  </w:r>
</w:p>'''
            self.paragraphs.append(p)

    def add_callout(self, text, title="ARCHITECTURAL NOTE"):
        p = f'''<w:p>
  <w:pPr>
    <w:shd w:val="clear" w:color="auto" w:fill="EFF6FF"/>
    <w:pBdr>
      <w:top w:val="single" w:sz="6" w:space="4" w:color="93C5FD"/>
      <w:bottom w:val="single" w:sz="6" w:space="4" w:color="93C5FD"/>
      <w:left w:val="single" w:sz="24" w:space="10" w:color="2563EB"/>
      <w:right w:val="single" w:sz="6" w:space="4" w:color="93C5FD"/>
    </w:pBdr>
    <w:ind w:left="240" w:right="200"/>
    <w:spacing w:before="80" w:after="80" w:line="260" w:lineRule="auto"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:b/>
      <w:sz w:val="20"/>
      <w:color w:val="1E40AF"/>
    </w:rPr>
    <w:t xml:space="preserve">[{self.escape(title)}] </w:t>
  </w:r>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:i/>
      <w:sz w:val="20"/>
      <w:color w:val="1E3A8A"/>
    </w:rPr>
    <w:t xml:space="preserve">{self.escape(text)}</w:t>
  </w:r>
</w:p>'''
        self.paragraphs.append(p)

    def add_table(self, headers, rows, col_widths=None):
        # Available width is 9026 dxa
        total_w = 9026
        num_cols = len(headers)
        if not col_widths:
            w_per_col = total_w // num_cols
            col_widths = [w_per_col] * num_cols
            col_widths[-1] = total_w - sum(col_widths[:-1])

        tbl_parts = []
        tbl_parts.append(f'''<w:tbl>
  <w:tblPr>
    <w:tblW w:w="{total_w}" w:type="dxa"/>
    <w:tblBorders>
      <w:top w:val="single" w:sz="12" w:space="0" w:color="1B365D"/>
      <w:left w:val="single" w:sz="12" w:space="0" w:color="1B365D"/>
      <w:bottom w:val="single" w:sz="12" w:space="0" w:color="1B365D"/>
      <w:right w:val="single" w:sz="12" w:space="0" w:color="1B365D"/>
      <w:insideH w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
      <w:insideV w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
    </w:tblBorders>
    <w:tblCellMar>
      <w:top w:w="80" w:type="dxa"/>
      <w:left w:w="120" w:type="dxa"/>
      <w:bottom w:w="80" w:type="dxa"/>
      <w:right w:w="120" w:type="dxa"/>
    </w:tblCellMar>
  </w:tblPr>''')

        # Header Row
        tbl_parts.append('''<w:tr>
  <w:trPr>
    <w:tblHeader/>
    <w:cantSplit/>
  </w:trPr>''')
        for i, h in enumerate(headers):
            cw = col_widths[i]
            tbl_parts.append(f'''  <w:tc>
    <w:tcPr>
      <w:tcW w:w="{cw}" w:type="dxa"/>
      <w:shd w:val="clear" w:color="auto" w:fill="1B365D"/>
      <w:vAlign w:val="center"/>
    </w:tcPr>
    <w:p>
      <w:pPr>
        <w:spacing w:before="40" w:after="40"/>
        <w:jc w:val="left"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
          <w:b/>
          <w:sz w:val="19"/>
          <w:color w:val="FFFFFF"/>
        </w:rPr>
        <w:t>{self.escape(h)}</w:t>
      </w:r>
    </w:p>
  </w:tc>''')
        tbl_parts.append('</w:tr>')

        # Data Rows
        for r_idx, row in enumerate(rows):
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            tbl_parts.append('''<w:tr>
  <w:trPr>
    <w:cantSplit/>
  </w:trPr>''')
            for c_idx, cell in enumerate(row):
                cw = col_widths[c_idx] if c_idx < len(col_widths) else col_widths[-1]
                tbl_parts.append(f'''  <w:tc>
    <w:tcPr>
      <w:tcW w:w="{cw}" w:type="dxa"/>
      <w:shd w:val="clear" w:color="auto" w:fill="{bg_color}"/>
      <w:vAlign w:val="center"/>
    </w:tcPr>
    <w:p>
      <w:pPr>
        <w:spacing w:before="30" w:after="30" w:line="240" w:lineRule="auto"/>
        <w:jc w:val="left"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
          <w:sz w:val="18"/>
          <w:color w:val="1E293B"/>
        </w:rPr>
        <w:t>{self.escape(cell)}</w:t>
      </w:r>
    </w:p>
  </w:tc>''')
            tbl_parts.append('</w:tr>')

        tbl_parts.append('</w:tbl>')
        # Add small spacing after table
        tbl_parts.append('''<w:p><w:pPr><w:spacing w:before="40" w:after="60"/></w:pPr></w:p>''')
        self.paragraphs.append('\n'.join(tbl_parts))

    def add_page_break(self):
        self.page_count += 1
        p = '''<w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr><w:r><w:br w:type="page"/></w:r></w:p>'''
        self.paragraphs.append(p)

    def build_docx(self, output_path):
        ct = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
  <Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
</Types>'''

        rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

        doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
</Relationships>'''

        styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>
        <w:sz w:val="21"/>
        <w:color w:val="1E293B"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:before="40" w:after="80" w:line="276" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
</w:styles>'''

        hdr = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:pBdr>
        <w:bottom w:val="single" w:sz="8" w:space="4" w:color="1B365D"/>
      </w:pBdr>
      <w:tabs>
        <w:tab w:val="right" w:pos="9026"/>
      </w:tabs>
      <w:spacing w:after="100"/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:b/>
        <w:sz w:val="17"/>
        <w:color w:val="1B365D"/>
      </w:rPr>
      <w:t>SIMATS ENGINEERING | ITA1439 ETHICAL HACKING</w:t>
    </w:r>
    <w:r>
      <w:tab/>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:b/>
        <w:sz w:val="17"/>
        <w:color w:val="64748B"/>
      </w:rPr>
      <w:t>CO3 – ASSIGNMENT 3</w:t>
    </w:r>
  </w:p>
</w:hdr>'''

        ftr = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:pBdr>
        <w:top w:val="single" w:sz="8" w:space="4" w:color="CBD5E1"/>
      </w:pBdr>
      <w:tabs>
        <w:tab w:val="right" w:pos="9026"/>
      </w:tabs>
      <w:spacing w:before="100"/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:sz w:val="17"/>
        <w:color w:val="64748B"/>
      </w:rPr>
      <w:t>Automated Scan-Data Pipeline &amp; Processing Library</w:t>
    </w:r>
    <w:r>
      <w:tab/>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:b/>
        <w:sz w:val="17"/>
        <w:color w:val="1B365D"/>
      </w:rPr>
      <w:t xml:space="preserve">Page </w:t>
    </w:r>
    <w:fldSimple w:instr="PAGE"/>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:sz w:val="17"/>
        <w:color w:val="64748B"/>
      </w:rPr>
      <w:t xml:space="preserve"> of </w:t>
    </w:r>
    <w:fldSimple w:instr="NUMPAGES"/>
  </w:p>
</w:ftr>'''

        doc_body = '\n'.join(self.paragraphs)
        doc = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{doc_body}
    <w:sectPr>
      <w:headerReference w:type="default" r:id="rId2"/>
      <w:footerReference w:type="default" r:id="rId3"/>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720"/>
    </w:sectPr>
  </w:body>
</w:document>'''

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z:
            z.writestr('[Content_Types].xml', ct)
            z.writestr('_rels/.rels', rels)
            z.writestr('word/_rels/document.xml.rels', doc_rels)
            z.writestr('word/styles.xml', styles)
            z.writestr('word/header1.xml', hdr)
            z.writestr('word/footer1.xml', ftr)
            z.writestr('word/document.xml', doc)

        print(f"Built DOCX with {self.page_count} explicitly demarcated pages at: {output_path}")

print("DocxBuilder initialized in doc_engine.py")
