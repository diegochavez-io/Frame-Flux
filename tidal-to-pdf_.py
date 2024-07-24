import os
from fpdf import FPDF
from tqdm import tqdm

# Define the path to your .tidal files and the output PDF
folder_path = '/Users/agi/Dropbox/_MAKE/Tidalcycles'
output_pdf_path = '/Users/agi/Dropbox/_MAKE/Tidalcycles/PDF/TIDAL-CODE/tidal_2407.pdf'
font_path = '/Users/agi/Library/Fonts/Inter-Regular.ttf'  # Updated font path

class PDF(FPDF):
    def header(self):
        self.set_font('Inter-Regular', 'B', 6)
        self.cell(0, 6, 'TidalCycles Code', align='C')
        self.ln(6)

    def footer(self):
        self.set_y(-10)
        self.set_font('Inter-Regular', 'I', 6)
        self.cell(0, 6, f'Page {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('Inter-Regular', 'B', 6)
        self.cell(0, 6, title, new_x='LMARGIN', new_y='TOP')
        self.ln(3)

    def chapter_body(self, body):
        self.set_font('Inter-Regular', '', 5)
        margin = 10
        column_width = (self.w - 3 * margin) / 2  # Two columns with margins
        column_height = self.h - 2 * margin  # Height of the column

        # Remove extra line breaks
        body = body.replace('\n\n', '\n')

        # Split the body into lines
        lines = body.split('\n')
        num_lines = len(lines)
        half_lines = num_lines // 2

        # Write the left column
        self.set_xy(margin, self.get_y())
        for i in range(half_lines):
            if self.get_y() > column_height:
                self.add_page()
                self.set_xy(margin, self.get_y())
            self.multi_cell(column_width, 2, lines[i], border=0)

        # Write the right column
        self.set_xy(margin + column_width + margin, self.get_y())
        for i in range(half_lines, num_lines):
            if self.get_y() > column_height:
                self.add_page()
                self.set_xy(margin + column_width + margin, self.get_y())
            self.multi_cell(column_width, 2, lines[i], border=0)

def convert_tidal_to_pdf(folder_path, output_pdf_path, font_path):
    pdf = PDF()

    # Check if font file exists
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")

    # Add custom fonts
    pdf.add_font('Inter-Regular', '', font_path)
    pdf.add_font('Inter-Regular', 'B', font_path)
    pdf.add_font('Inter-Regular', 'I', font_path)
    
    # Add a fallback font
    pdf.add_font('PlusJakartaSans', '', '/Users/agi/Library/Fonts/PlusJakartaSans-Regular.ttf')

    # Get a list of all .tidal files in the folder
    tidal_files = [f for f in os.listdir(folder_path) if f.endswith('.tidal')]

    # Iterate over all .tidal files in the folder with a progress bar
    for filename in tqdm(tidal_files, desc="Processing files"):
        file_path = os.path.join(folder_path, filename)

        # Read the content of the .tidal file
        with open(file_path, 'r') as file:
            content = file.read()

        # Add content to the PDF
        pdf.add_page()
        pdf.chapter_title(filename)
        pdf.chapter_body(content)

    # Save the PDF
    pdf.output(output_pdf_path)

if __name__ == "__main__":
    convert_tidal_to_pdf(folder_path, output_pdf_path, font_path)
