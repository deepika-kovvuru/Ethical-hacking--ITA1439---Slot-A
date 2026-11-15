# html_converter.py - Converts WordprocessingML snippets to print-ready HTML pages

import re
import html

def convert_paragraphs_to_html(paragraphs):
    pages = []
    current_page = []
    
    for p in paragraphs:
        if '<w:br w:type="page"/>' in p:
            pages.append(current_page)
            current_page = []
            continue
        current_page.append(p)
    if current_page:
        pages.append(current_page)

    html_pages = []
    total_pages = len(pages)
    
    for page_idx, p_list in enumerate(pages, 1):
        page_html = []
        page_html.append(f'<div class="page-container" id="page-{page_idx}">')
        page_html.append('  <div class="header-rule">')
        page_html.append('    <span>SIMATS ENGINEERING | ITA1439 ETHICAL HACKING</span>')
        page_html.append('    <span>CO3 – ASSIGNMENT 3</span>')
        page_html.append('  </div>')
        
        # Render contents
        for item in p_list:
            # Check if title
            if '<w:sz w:val="44"/>' in item:
                # Title
                m = re.findall(r'<w:t(?: xml:space="preserve")?>(.*?)</w:t>', item)
                txt = html.escape(' '.join(m))
                page_html.append(f'  <h1 class="doc-title">{txt}</h1>')
            elif '<w:i/>' in item and '<w:sz w:val="24"/>' in item:
                m = re.findall(r'<w:t(?: xml:space="preserve")?>(.*?)</w:t>', item)
                txt = html.escape(' '.join(m)).replace('\\n', '<br>')
                page_html.append(f'  <div class="doc-subtitle">{txt}</div>')
            elif '<w:sz w:val="30"/>' in item and '<w:b/>' in item:
                m = re.findall(r'<w:t(?: xml:space="preserve")?>(.*?)</w:t>', item)
                txt = html.escape(' '.join(m))
                page_html.append(f'  <h1>{txt}</h1>')
            elif '<w:sz w:val="25"/>' in item and '<w:b/>' in item:
                m = re.findall(r'<w:t(?: xml:space="preserve")?>(.*?)</w:t>', item)
                txt = html.escape(' '.join(m))
                page_html.append(f'  <h2>{txt}</h2>')
            elif '<w:sz w:val="22"/>' in item and '<w:b/>' in item:
                m = re.findall(r'<w:t(?: xml:space="preserve")?>(.*?)</w:t>', item)
                txt = html.escape(' '.join(m))
                page_html.append(f'  <h3>{txt}</h3>')
            elif '<w:tbl>' in item:
                # Convert XML table to HTML table
                page_html.append(convert_xml_table(item))
            elif '<w:shd w:val="clear" w:color="auto" w:fill="F1F5F9"/>' in item:
                # Code block
                m = re.findall(r'<w:t(?: xml:space="preserve")?>(.*?)</w:t>', item)
                line = html.escape(''.join(m))
                page_html.append(f'  <pre><code>{line}</code></pre>')
            elif '<w:shd w:val="clear" w:color="auto" w:fill="EFF6FF"/>' in item:
                # Callout
                m = re.findall(r'<w:t(?: xml:space="preserve")?>(.*?)</w:t>', item)
                txt = html.escape(''.join(m))
                page_html.append(f'  <div class="callout">{txt}</div>')
            elif '&#9679;' in item or '&#9679;  ' in item:
                # Bullet item
                m = re.findall(r'<w:t(?: xml:space="preserve")?>(.*?)</w:t>', item)
                clean_tokens = [tok for tok in m if '&#9679;' not in tok]
                txt = html.escape(''.join(clean_tokens))
                page_html.append(f'  <ul><li>{txt}</li></ul>')
            else:
                # Standard paragraph
                m = re.findall(r'<w:t(?: xml:space="preserve")?>(.*?)</w:t>', item)
                if m:
                    txt = html.escape(''.join(m))
                    if txt.strip():
                        page_html.append(f'  <p>{txt}</p>')

        page_html.append('  <div class="footer-rule">')
        page_html.append('    <span>Automated Scan-Data Pipeline & Processing Library</span>')
        page_html.append(f'    <span>Page {page_idx} of {total_pages}</span>')
        page_html.append('  </div>')
        page_html.append('</div>')
        html_pages.append('\n'.join(page_html))

    return '\n\n'.join(html_pages)

def convert_xml_table(xml_tbl):
    out = ['  <table>']
    # Rows
    tr_matches = re.findall(r'<w:tr>.*?</w:tr>', xml_tbl, re.DOTALL)
    for r_idx, tr in enumerate(tr_matches):
        is_header = '<w:tblHeader/>' in tr or r_idx == 0
        tag = 'th' if is_header else 'td'
        out.append('    <tr>')
        tc_matches = re.findall(r'<w:tc>.*?</w:tc>', tr, re.DOTALL)
        for tc in tc_matches:
            m = re.findall(r'<w:t(?: xml:space="preserve")?>(.*?)</w:t>', tc)
            cell_txt = html.escape(''.join(m))
            out.append(f'      <{tag}>{cell_txt}</{tag}>')
        out.append('    </tr>')
    out.append('  </table>')
    return '\n'.join(out)
