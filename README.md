# Notion Equation

Convert `$` or `$$` enclosed text in a Notion page into math expressions.

## Requirements

- Python 3.7+
- [Notion API](https://developers.notion.com/docs/getting-started)
- `.env` file with your Notion API key

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py "https://www.notion.so/your-page-id"
```

- `$...$` → inline equation
- `$$...$$` → equation block (only if paragraph has no other text)
