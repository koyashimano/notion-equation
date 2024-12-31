import os
import sys
from dotenv import load_dotenv


load_dotenv()

args = sys.argv[1:]
NOTION_PAGE_URL = args[0]

option_names = []
options = {}
for i in range(2, len(args)):
    if args[i].startswith("--"):
        opt = args[i][2:]
        if opt in option_names:
            options[opt] = args[i + 1]

NOTION_AUTH_TOKEN = os.getenv("NOTION_AUTH_TOKEN")
