from http.server import BaseHTTPRequestHandler
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        user_data = data.get("userData", {})

        prompt = f"""You are a professional resume writer. Based on the following information, rewrite each section in polished, professional language suitable for a resume. Return ONLY a JSON object with these exact keys: name, email, phone, location, summary, education, experience, skills, projects. Keep the same structure but improve the language. Do not add any explanation or markdown.

User data:
{json.dumps(user_data, indent=2)}"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content
            # Strip any markdown if present
            result = result.replace('```json', '').replace('```', '').strip()

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"result": json.loads(result)}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())