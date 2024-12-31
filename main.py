#!/usr/bin/env python

import re
from notion_client import Client
from notion_client.helpers import iterate_paginated_api

import settings
from utils import extract_page_id


TEXT_BLOCK_TYPES = [
    "paragraph",
    "numbered_list_item",
    "bulleted_list_item",
    "callout",
    "heading_1",
    "heading_2",
    "heading_3",
    "quote",
    "to_do",
    "toggle",
]

EQUATION_PATTERN = re.compile(r"\$[^$]+\$")
SPLIT_PATTERN = re.compile(r"(\$[^$]+\$)")


def convert_equations_in_rich_text(rich_text_list):
    new_rich_text_list = []
    changed = False
    for rich_text in rich_text_list:
        if rich_text["type"] != "text" or not EQUATION_PATTERN.search(
            rich_text["text"]["content"]
        ):
            new_rich_text_list.append(rich_text)
            continue

        changed = True
        for text in re.split(SPLIT_PATTERN, rich_text["text"]["content"]):
            if not text:
                continue
            if len(text) > 2 and text.startswith("$") and text.endswith("$"):
                text = text[1:-1]
                new_rich_text_list.append(
                    {
                        "type": "equation",
                        "equation": {"expression": text},
                        "plain_text": text,
                        "annotations": rich_text["annotations"],
                        "href": rich_text["href"],
                    }
                )
            else:
                new_rich_text_list.append(
                    {
                        "type": "text",
                        "text": {
                            "content": text,
                            "link": rich_text["text"]["link"],
                        },
                        "plain_text": text,
                        "annotations": rich_text["annotations"],
                        "href": rich_text["href"],
                    }
                )

    return new_rich_text_list, changed


def process_block(block, notion, parent_id):
    block_type = block["type"]
    rich_text_list = block[block_type]["rich_text"]
    if (
        block_type == "paragraph"
        and len(rich_text_list) == 1
        and rich_text_list[0]["type"] == "text"
    ):
        content = rich_text_list[0]["text"]["content"]
        if (
            len(content) > 4
            and content.startswith("$$")
            and content.endswith("$$")
            and content.count("$$") == 2
        ):
            block["type"] = "equation"
            block.pop(block_type)
            block["equation"] = {"expression": content[2:-2]}
            notion.blocks.children.append(
                block_id=parent_id, after=block["id"], children=[block]
            )
            notion.blocks.delete(block_id=block["id"])
            print(f"Updated block {block['id']}")
            return

    new_rich_text_list, changed = convert_equations_in_rich_text(rich_text_list)
    if changed:
        block[block_type]["rich_text"] = new_rich_text_list
        notion.blocks.update(block_id=block["id"], **block)
        print(f"Updated block {block['id']}")


def execute(parent_id, notion):
    for block in iterate_paginated_api(notion.blocks.children.list, block_id=parent_id):
        if block["type"] in TEXT_BLOCK_TYPES:
            process_block(block, notion, parent_id)
        if block["has_children"]:
            execute(block["id"], notion)


def main():
    try:
        notion = Client(auth=settings.NOTION_AUTH_TOKEN)
        page_id = extract_page_id(settings.NOTION_PAGE_URL)
        execute(page_id, notion)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
