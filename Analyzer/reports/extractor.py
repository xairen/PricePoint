from bs4 import BeautifulSoup
import re
import csv
import os

# Load and parse HTML
with open("Analyzer/reports/test.html", "r", encoding="utf-8") as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, "lxml")
document_text = soup.get_text(separator=" ", strip=True)

# New attempt to extract the company name
company_name_regex = r"Press Release\s+(.*?)(,|\s+reports)"
company_match = re.search(company_name_regex, document_text, re.IGNORECASE)
company_name = company_match.group(1) if company_match else "Unknown Company"

# Extract sales information
net_sales_regex = r"net sales for the quarter increased (\d+\.\d+) percent, to \$(\d+\.\d+) billion, from \$(\d+\.\d+) billion last year"
matches = re.findall(net_sales_regex, document_text, re.IGNORECASE)

# Write to CSV
csv_file = "earnings_reports.csv"
write_headers = not os.path.isfile(csv_file)
with open(csv_file, "a", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    headers = [
        "Company Name",
        "Sales Growth Percentage",
        "Current Quarter Sales ($B)",
        "Previous Year's Quarter Sales ($B)",
    ]
    if write_headers:
        csvwriter.writerow(headers)
    for match in matches:
        csvwriter.writerow([company_name] + list(match))
