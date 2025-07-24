from docx import Document
import re


def json_to_docx(summary_json, output_path):
    doc = Document()
    doc.add_heading(summary_json.get("title", "Summary"), level=0)

    for section in summary_json.get("sections", []):
        doc.add_heading(section["heading"], level=1)
        for line in section["content"].split("\n"):
            line = line.strip()
            if line.startswith("- "):
                line = line[2:].strip()
                para = doc.add_paragraph(style="List Bullet")
                parts = re.split(r"(\*\*.*?\*\*)", line)
                for part in parts:
                    run = para.add_run()
                    if part.startswith("**") and part.endswith("**"):
                        run.text = part[2:-2]
                        run.bold = True
                    else:
                        run.text = part
            else:
                doc.add_paragraph(line.strip())
    doc.save(output_path)
    print(f"Document saved locally: {output_path}")