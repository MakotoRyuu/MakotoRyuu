#!/usr/bin/env python3
"""Read editable quotes and render one static quote per Shanghai calendar day."""
import argparse
import base64
from datetime import date, datetime
from html import escape
import importlib.util
from pathlib import Path
import unicodedata
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
EPOCH = date(2026, 9, 20)


def read_quotes(path):
    quotes = []
    for number, raw in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        text, separator, author = line.partition('|')
        if not text.strip():
            raise ValueError(f'{path.name}:{number}: 名言正文不能为空')
        quotes.append((text.strip(), author.strip() if separator else ''))
    if not quotes:
        raise ValueError(f'{path.name}: 请至少填写一句名言')
    return quotes


def wrap(text, limit=60):
    lines, current, width = [], '', 0
    for char in text:
        size = 0 if unicodedata.combining(char) else 2 if unicodedata.east_asian_width(char) in 'WF' else 1
        if current and width + size > limit:
            lines.append(current.rstrip())
            current, width = '', 0
        current += char
        width += size
    if current:
        lines.append(current.rstrip())
    return lines


def render(today, quote, font_data=None):
    text, author = quote
    lines = wrap(text)
    authors = wrap('—— ' + author, 86) if author else []
    height = 104 + 34 * len(lines) + 24 * len(authors)
    css = ''
    if font_data:
        encoded = base64.b64encode(font_data).decode('ascii')
        css = '@font-face{font-family:QuoteHandwriting;src:url(data:font/woff2;base64,' + encoded + ') format("woff2");}'
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 816 {height}" role="img" aria-labelledby="title desc">
<title id="title">每日一言 · {today.isoformat()}</title>
<desc id="desc">{escape(text)}{escape(' —— ' + author) if author else ''}</desc>
<style>{css}text{{font-family:QuoteHandwriting,"PingFang SC","Microsoft YaHei",sans-serif;}}</style>
<rect width="100%" height="100%" fill="#ffffff"/>
<text x="40" y="38" font-size="20" font-weight="600" fill="#24292f">每日一言</text>
<text x="776" y="38" font-size="12" text-anchor="end" fill="#57606a">{today.isoformat()}</text>
<rect x="40" y="61" width="3" height="{34*len(lines)}" rx="1.5" fill="#1f883d"/>''']
    for index, line in enumerate(lines):
        parts.append(f'<text x="62" y="{86+index*34}" font-size="22" fill="#24292f">{escape(line)}</text>')
    for index, line in enumerate(authors):
        parts.append(f'<text x="776" y="{98+len(lines)*34+index*24}" text-anchor="end" font-size="15" fill="#57606a">{escape(line)}</text>')
    parts.append('</svg>')
    return '\n'.join(parts) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', type=date.fromisoformat, help='预览指定日期 YYYY-MM-DD')
    args = parser.parse_args()
    today = args.date or datetime.now(ZoneInfo('Asia/Shanghai')).date()
    quotes = read_quotes(HERE / 'quotes.txt')
    quote = quotes[(today - EPOCH).days % len(quotes)]
    # Reuse the calendar's exact handwriting font and font-subsetting implementation.
    spec = importlib.util.spec_from_file_location('holiday_style', HERE.parent / 'holiday/generate-holiday-svg.py')
    calendar = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(calendar)
    font = calendar.subset_font_for_text('每日一言' + today.isoformat() + ''.join(quote) + '——')
    if not font:
        print('警告：字体获取失败，使用系统中文字体；下次更新会重新尝试。')
    output = HERE / 'daily-quote.svg'
    output.write_text(render(today, quote, font), encoding='utf-8')
    print(f'已生成 {output.name}：{today.isoformat()}')


if __name__ == '__main__':
    main()
