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


def render(today, quote, font_data=None):
    text, author = quote
    attribution = ' —— ' + author if author else ''
    combined = text + attribution
    # Reserve a separate right-aligned author area with a gap from the quote.
    def units(value):
        return sum(0 if unicodedata.combining(c) else 2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in value)

    author_width = min(280, units(attribution) * 11) if author else 0
    quote_width = 714 - author_width - (28 if author else 0)
    font_size = min(22, max(14, quote_width / max(units(text), 1) * 2))
    fit = f' textLength="{quote_width}" lengthAdjust="spacingAndGlyphs"' if units(text) * font_size / 2 > quote_width else ''
    author_fit = f' textLength="{author_width}" lengthAdjust="spacingAndGlyphs"' if units(attribution) * 11 > author_width else ''
    author_svg = f'<text x="776" y="40" text-anchor="end" font-size="22" fill="#57606a"{author_fit}>{escape(attribution.strip())}</text>' if author else ''
    css = ''
    if font_data:
        encoded = base64.b64encode(font_data).decode('ascii')
        css = '@font-face{font-family:QuoteHandwriting;src:url(data:font/woff2;base64,' + encoded + ') format("woff2");}'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 816 64" role="img" aria-labelledby="title">
<title id="title">{escape(combined)}</title>
<style>{css}text{{font-family:QuoteHandwriting,"PingFang SC","Microsoft YaHei",sans-serif;}}</style>
<rect width="100%" height="100%" fill="#ffffff"/>
<rect x="40" y="18" width="3" height="28" rx="1.5" fill="#1f883d"/>
<text x="62" y="40" font-size="{font_size:.2f}" fill="#24292f"{fit}>{escape(text)}</text>
{author_svg}
</svg>
'''


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
    font = calendar.subset_font_for_text(''.join(quote) + ' —— ')
    if not font:
        print('警告：字体获取失败，使用系统中文字体；下次更新会重新尝试。')
    output = HERE / 'daily-quote.svg'
    output.write_text(render(today, quote, font), encoding='utf-8')
    print(f'已生成 {output.name}：{today.isoformat()}')


if __name__ == '__main__':
    main()
