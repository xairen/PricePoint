from bs4 import BeautifulSoup
import re
from transformers import pipeline

# Load the HTML content
with open("Analyzer/reports/test.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "lxml")
text = soup.get_text(separator=" ", strip=True)

# print(text)

document_text = text

net_sales_regex = r"net sales for the quarter increased (\d+\.\d+) percent, to \$(\d+\.\d+) billion, from \$(\d+\.\d+) billion last year"
matches = re.findall(net_sales_regex, document_text, re.IGNORECASE)
print("Extracted Net Sales Figures:", matches)

summarizer = pipeline("summarization", model="t5-small", framework="pt")
summary = summarizer(document_text, max_length=130, min_length=30, do_sample=False)

print(summary[0]["summary_text"])
