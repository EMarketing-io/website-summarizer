import openai
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_with_openai(webpage_text):
    prompt = f"""
You are a professional business analyst. Analyze the following website content and extract comprehensive, detailed business information in JSON format.

Each section should contain **4–6 bullet points** with rich, descriptive details — not short or generic phrases. Bold important keywords using `**bold**` markdown format. DO NOT include explanations, just return the valid JSON only.

Use this exact structure:

{{
  "title": "<Website Title or Company Name>",
  "sections": [
    {{
      "heading": "Purpose",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "Target Audience",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "About the Company",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "Company Information",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "Unique Selling Proposition (USP)",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "Reviews/Testimonials",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "Products/Service Categories",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }},
    {{
      "heading": "Offers",
      "content": "- Bullet point 1\\n- Bullet point 2\\n..."
    }}
  ]
}}

Analyze this content:
\"\"\"{webpage_text}\"\"\"
"""

    try:
        response = openai.ChatCompletion.create(
            model="chatgpt-4o-latest",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        raw_text = response["choices"][0]["message"]["content"].strip()
        print("\n🔍 RAW RESPONSE FROM OPENAI:\n", raw_text[:1000], "\n")  # Safe preview

        raw_text = raw_text.strip("`").strip()
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()

        raw_text = (
            raw_text.replace("“", '"')
            .replace("”", '"')
            .replace("’", "'")
            .replace("‘", "'")
            .replace("–", "-")
            .replace("—", "-")
        )

        match = re.search(r"{.*}", raw_text, re.DOTALL)
        json_text = match.group(0) if match else raw_text

        return json.loads(json_text)

    except Exception as e:
        print("⚠️ OpenAI JSON parsing failed:", e)
        print("⚠️ Raw output was:\n", raw_text)
        return {
            "title": "Summary Unavailable",
            "sections": [
                {
                    "heading": "Error",
                    "content": "OpenAI returned invalid or incomplete JSON.",
                }
            ],
        }
