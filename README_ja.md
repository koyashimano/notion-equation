# Notion Equation

Notion ページ内で `$` や `$$` で囲まれたテキストを数式に変換します。

## 要件

- Python 3.7 以上
- [Notion API](https://developers.notion.com/docs/getting-started)
- `.env` ファイルに Notion API キーを記述

## インストール

```bash
pip install -r requirements.txt
```

## 使い方

```bash
python main.py "https://www.notion.so/your-page-id"
```

- `$...$` → インライン数式
- `$$...$$` → 数式ブロック（段落に他のテキストがない場合のみ）
