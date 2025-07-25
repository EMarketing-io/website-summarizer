import os
from extract import extract_text_from_url
from summarize import summarize_with_openai
from document import create_docx_in_memory
from drive import upload_docx_to_gdrive
import re
from dotenv import load_dotenv

load_dotenv()

def format_website_name(url):
    domain = re.sub(r"https?://(www\.)?", "", url).split("/")[0]
    domain_parts = domain.split(".")
    formatted_name = " ".join([part.capitalize() for part in domain_parts if part])
    return formatted_name

def summarize_webpage_to_google_docs():
    url = input("Enter the website URL to summarize: ").strip()
    print(f"\nExtracting content from: {url}")
    
    raw_text = extract_text_from_url(url)
    print(f"Extracted {len(raw_text)} characters of content.")
    print("Summarizing with OpenAI...")
    
    summary_json = summarize_with_openai(raw_text)

    formatted_name = format_website_name(url)
    filename = f"{formatted_name} Website Summary.docx"
    document_title = f"{formatted_name} Website Summary"

    print("Creating .docx document in memory...")
    docx_stream = create_docx_in_memory(summary_json, document_title)

    print("Uploading to Google Drive...")
    upload_docx_to_gdrive(docx_stream, filename)

if __name__ == "__main__":
    summarize_webpage_to_google_docs()
