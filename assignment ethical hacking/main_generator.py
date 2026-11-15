# main_generator.py - Orchestrates document generation for both DOCX and HTML

import os
import sys
from doc_engine import DocxBuilder
from pages_q1_q2 import build_pages_1_to_13
from pages_q3_q4 import build_pages_14_to_23
from pages_q5_q6 import build_pages_24_to_30
from pages_q7 import build_pages_31_to_35

def generate_docx():
    print("Initializing DocxBuilder...")
    builder = DocxBuilder()
    
    print("Adding Pages 1 to 13 (Q1 & Q2)...")
    build_pages_1_to_13(builder)
    
    print("Adding Pages 14 to 23 (Q3 & Q4)...")
    build_pages_14_to_23(builder)
    
    print("Adding Pages 24 to 30 (Q5 & Q6)...")
    build_pages_24_to_30(builder)
    
    print("Adding Pages 31 to 35 (Q7 Day-4 Challenge & Contribution Record)...")
    build_pages_31_to_35(builder)
    
    output_docx = "CO3_Assignment_3_Complete_Solution.docx"
    print(f"Total pages demarcated: {builder.page_count}")
    builder.build_docx(output_docx)
    return output_docx, builder.page_count

def generate_html():
    print("Generating standalone print-ready HTML document...")
    # Read the text content and convert into clean styled HTML
    # We will write a comprehensive HTML companion with matching 35 pages CSS pagination
    from build_html_doc import create_html_report
    output_html = "CO3_Assignment_3_Complete_Solution.html"
    create_html_report(output_html)
    return output_html

if __name__ == "__main__":
    docx_file, pages = generate_docx()
    print(f"[SUCCESS] Generated Word Document: {docx_file} with {pages} pages!")
