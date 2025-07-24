from extract import extract_text_from_url
from summarize import summarize_with_openai
from document import json_to_docx
from drive import upload_docx_to_gdrive
import re


def summarize_webpage_to_google_docs():
    url = input("Enter the website URL to summarize: ").strip()
    print(f"\nExtracting content from: {url}")
    raw_text = extract_text_from_url(url)[:8000]  # Optional length limiter

    print("Summarizing with OpenAI...")
    summary_json = summarize_with_openai(raw_text)

    domain = re.sub(r"https?://(www\.)?", "", url).split("/")[0].replace(".", "")
    filename = f"{domain}.docx"

    print("Creating .docx document...")
    json_to_docx(summary_json, filename)

    print("Uploading to Google Drive...")
    upload_docx_to_gdrive(filename, filename)


if __name__ == "__main__":
    summarize_webpage_to_google_docs()
