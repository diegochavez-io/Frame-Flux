import os
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def create_table(data):
    data_list = [data.columns.tolist()] + data.values.tolist()
    table = Table(data_list)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    return table

def parse_csv_sections(file_path):
    # Open and read the file line by line
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Find the dividing line based on empty line or format change
    sections = []
    current_section = []
    for line in lines:
        if line.strip() == "":
            if current_section:
                sections.append(current_section)
                current_section = []
        else:
            current_section.append(line)
    if current_section:
        sections.append(current_section)
    
    return sections

def csv_to_pdf(csv_file_path, pdf_file_path):
    sections = parse_csv_sections(csv_file_path)
    pdf = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    elements = []
    
    for section in sections:
        # Convert section list back to a CSV string
        section_csv = ''.join(section)
        from io import StringIO
        data = pd.read_csv(StringIO(section_csv))
        table = create_table(data)
        elements.append(table)
    
    pdf.build(elements)

def process_all_csvs(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(directory, filename)
            pdf_file_path = os.path.join(directory, filename.replace('.csv', '.pdf'))
            csv_to_pdf(csv_file_path, pdf_file_path)
            print(f'Converted {filename} to PDF.')

# Example usage
source_folder = '/Users/agi/Dropbox/Taxes_2023/BOA'
process_all_csvs(source_folder)
