# Groq-Enhanced FFUF: Fuzzing with Precision

This script is an extension of the popular [`ffuf`](https://github.com/ffuf/ffuf) tool that uses the Groq API to suggest file extensions for fuzzing. It provides a more precise and targeted approach to fuzzing by leveraging the power of AI to analyze the URL and HTTP headers and suggest relevant file extensions.

## Prerequisites

- Python 3.x
- `ffuf` tool installed
- Groq API key (set as `GROQ_API_KEY` environment variable or configured in a `.env` file)

## Installation

1. Install the required dependencies:
   ```bash
   pip install argparse requests urllib3 python-dotenv groq
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/nirajnkm/groq-enhanced-ffuf
   ```

3. Navigate to the repository directory:
   ```bash
   cd groq-enhanced-ffuf
   ```

## Setting the Groq API Key

You can set the `GROQ_API_KEY` in two ways:

### 1. Using an Environment Variable
   ```bash
   export GROQ_API_KEY=your_groq_api_key
   ```

### 2. Using a `.env` File

   1. Create a `.env` file in the project directory:
      ```bash
      touch .env
      ```

   2. Add the following line to the `.env` file:
      ```plaintext
      GROQ_API_KEY=your_groq_api_key
      ```

   3. The script will automatically load the `.env` file using the `python-dotenv` package.

## Usage

1. Run the script with the desired options:
   ```bash
   python groq_enhanced_ffuf.py --ffuf-path /path/to/ffuf --max-extensions 4 -u https://example.com/FUZZ
   ```

   Replace `/path/to/ffuf` with the actual path to the `ffuf` executable and `https://example.com/FUZZ` with the target URL.

2. The script will fetch the HTTP headers for the base URL, suggest file extensions using the Groq API, and run `ffuf` with the suggested extensions.

## Parameters

The options that `ffuf` accepts are all supported by `groq_enhanced_ffuf`, along with additional parameters:

- `--ffuf-path`: Specifies the path to the `ffuf` executable. Default is `ffuf`.
   Example:
   ```bash
   groq_enhanced_ffuf --ffuf-path /usr/local/bin/ffuf -u https://example.com/FUZZ
   ```

- `--max-extensions`: Sets the maximum number of extensions suggested. Default is 4.
   Example:
   ```bash
   groq_enhanced_ffuf --max-extensions 6 -u https://example.com/FUZZ
   ```

- `-u`: Specifies the target URL with the `FUZZ` keyword.
   Example:
   ```bash
   groq_enhanced_ffuf -u https://example.com/FUZZ
   ```

- `-w`: Specifies the wordlist for fuzzing.
   Example:
   ```bash
   groq_enhanced_ffuf -u https://example.com/FUZZ -w /path/to/wordlist.txt
   ```

## Notes

- The script uses the `llama3-8b-8192` model for AI-generated responses. You can change the model name in the `get_ai_extensions` function if required.
- Ensure the `FUZZ` keyword is present at the end of the URL path for accurate extension suggestions.
- To avoid accidental exposure of the `.env` file, add it to `.gitignore`:
   ```plaintext
   .env
   ```

## License

This script is licensed under the MIT License. See the `LICENSE` file for more details.

## Credits

This project was inspired by [ffufai](https://github.com/jthack/ffufai), which uses OpenAI and Anthropic APIs for fuzzing. However, I found that Groq API is better suited for my project due to its faster response times, higher accuracy, and simpler integration with [`ffuf`](https://github.com/ffuf/ffuf). 

The free tier of Groq API (1,000 characters/day) has been particularly advantageous for testing and developing my fuzzing tool cost-effectively.

--- 