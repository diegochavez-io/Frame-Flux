import csv
import fitz  # PyMuPDF for reading PDFs

# Define the path to your PDF file
pdf_path = '/Users/agi/Dropbox/Taxes_2023/2023_Spendings_Edit.pdf'

def extract_transactions_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    page = document[1]  # Assuming transactions are on the second page
    text = page.get_text()
    document.close()

    # Split the text by lines and extract transactions
    lines = text.split('\n')
    transactions = []
    for line in lines:
        parts = line.split()
        if len(parts) > 2:  # Basic check to include only transaction lines
            date = parts[0]
            amount = parts[-1]
            description = ' '.join(parts[1:-1])
            transactions.append((date, description, amount))
    return transactions

def save_to_csv(transactions, filename='transactions.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Description', 'Amount'])  # Header
        for transaction in transactions:
            writer.writerow(transaction)

# Example usage
transactions = extract_transactions_from_pdf(pdf_path)
save_to_csv(transactions)

print("CSV file has been created and is ready for Google Sheets.")
