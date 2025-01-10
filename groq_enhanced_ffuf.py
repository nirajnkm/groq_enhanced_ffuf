import argparse
import os
import subprocess
import requests
from urllib.parse import urlparse
import json
from groq import Groq
from dotenv import load_dotenv 


load_dotenv() 

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def get_headers(url):
    """
    Fetch HTTP headers for a given URL.
    """
    try:
        response = requests.head(url, allow_redirects=True)
        return dict(response.headers)
    except requests.RequestException as e:
        print(f"Error fetching headers: {e}")
        return {"Header": "Error fetching headers."}


def get_ai_extensions(url, headers, max_extensions):
    """
    Use the Groq API to suggest file extensions for fuzzing.
    """
    prompt = f"""
You are tasked with identifying the most likely file extensions for fuzzing based on a given URL and its HTTP headers. Your response must be a valid JSON object, which can be parsed using `json.loads()`. Format the response strictly as: {{"extensions": [".ext1", ".ext2", ...]}}.

Instructions:
1. Relevance: Suggest file extensions that make sense based on the URL path and headers. Avoid irrelevant extensions. For example:
   - If the URL contains `/js/`, prioritize `.js` or related extensions.
   - If the path mentions "presentations," prioritize extensions like `.ppt`, `.pdf`, or `.pptx`.
2. Prioritization: Limit suggestions to {max_extensions} extensions. Select the most interesting or commonly used extensions if constrained.
3. Content Type Guidance: Use HTTP headers (e.g., `Content-Type`, `Server`, etc.) to infer the file type or platform, and suggest extensions accordingly.
4. Avoid Unnecessary Details: Respond concisely without any preamble or additional text. Only provide the JSON response.

Examples:
1. Scenario 1:  
   - URL: https://example.com/presentations/FUZZ  
   - Headers: {{"Content-Type": "application/pdf", "Content-Length": "1234567"}}  
   - JSON Response: {{"extensions": [".pdf", ".ppt", ".pptx"]}}  

2. Scenario 2:  
   - URL: https://example.com/FUZZ  
   - Headers: {{"Server": "Microsoft-IIS/10.0", "X-Powered-By": "ASP.NET"}}  
   - JSON Response: {{"extensions": [".aspx", ".asp", ".exe", ".dll"]}}  

 Task Input:
- URL: {url}
- Headers: {headers}

 Task Output:
JSON Response:
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        print(f"Error with AI response: {e}")
        return {"extensions": []}


def main():
    """
    Main function to run the ffuf tool with suggested extensions from Groq API.
    """
    print("\033[95mGroq-Enhanced FFUF: Fuzzing with Precision\033[0m")   
    parser = argparse.ArgumentParser(description='Groq-Enhanced FFUF: Fuzzing with Precision')
    parser.add_argument('--ffuf-path', default='ffuf', help='Path to ffuf executable')
    parser.add_argument('--max-extensions', type=int, default=4, help='Maximum number of extensions to suggest')
    args, unknown = parser.parse_known_args()

    # Find the -u argument in the unknown args
    try:
        url_index = unknown.index('-u') + 1
        url = unknown[url_index]
    except (ValueError, IndexError):
        print("Error: -u URL argument is required.")
        return

    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')

    if 'FUZZ' not in path_parts[-1]:
        print("Warning: FUZZ keyword is not at the end of the URL path. Extension fuzzing may not work as expected.")

    base_url = url.replace('FUZZ', '')
    headers = get_headers(base_url)

    extensions_data = get_ai_extensions(url, headers, args.max_extensions)
    extensions = ','.join(extensions_data.get('extensions', [])[:args.max_extensions])

    if not extensions:
        print("No extensions were suggested. Please try again.")
        return

    ffuf_command = [args.ffuf_path] + unknown + ['-e', extensions]
    subprocess.run(ffuf_command)


if __name__ == "__main__":
    main()