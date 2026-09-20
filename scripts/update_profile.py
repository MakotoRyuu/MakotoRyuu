"""Generate a self-contained profile card using Python's standard library."""
import argparse
import calendar
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def render(today):
    elapsed = (today - date(today.year, 1, 1)).days + 1
    total = (date(today.year + 1, 1, 1) - date(today.year, 1, 1)).days
    progress = elapsed / total
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="490" viewBox="0 0 880 490" role="img" aria-labelledby="title desc">+<title id="title">MakotoRyuu · 每日日历</title>
<desc id="desc">更新日期 {today.isoformat()}，年度进度 {progress:.1%}。绿色标记今天，紫色标记周末；不包含法定节假日及调休。</desc>
<style>text {{font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif}} .muted {{fill:#9caac4}} .day {{fill:#e5eafa}}</style>
<rect width="880" height="490" rx="24" fill="#101827"/>
<circle cx="822" cy="66" r="100" fill="#172a42"/>
<text x="36" y="45" fill="#80e8c0" font-size="12" letter-spacing="3">DAILY / MAKOTORYUU</text>
<text x="36" y="89" fill="#f1f5ff" font-size="32" font-weight="700">Hello, I'm MakotoRyuu.</text>
<text x="36" y="117" class="muted" font-size="14">一点一滴，持续构建。</text>
<text x="844" y="113" text-anchor="end" class="muted" font-size="13">{today.isoformat()} · UTC+8</text>''']
    for offset in range(2):
        year = today.year + (today.month - 1 + offset) // 12
        month = (today.month - 1 + offset) % 12 + 1
        left = 36 + offset * 418
        parts.append(f'<rect x="{left}" y="144" width="390" height="272" rx="16" fill="#192438"/>')
        parts.append(f'<text x="{left+20}" y="177" fill="#f1f5ff" font-size="19" font-weight="600">{year} / {month:02d}</text>')
        for col, label in enumerate(["一", "二", "三", "四", "五", "六", "日"]):
            x = left + 33 + col * 54
            parts.append(f'<text x="{x}" y="207" text-anchor="middle" class="muted" font-size="12">{label}</text>')
        for row, week in enumerate(calendar.Calendar().monthdayscalendar(year, month)):
            for col, day in enumerate(week):
                if not day:
                    continue
                x, y = left + 33 + col * 54, 237 + row * 30
                current = date(year, month, day) == today
                if current:
                    parts.append(f'<rect x="{x-17}" y="{y-20}" width="34" height="27" rx="8" fill="#80e8c0"/>')
                color = '#101827' if current else '#b7a5f6' if col >= 5 else '#e5eafa'
                parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-size="14" fill="{color}">{day}</text>')
    parts.append(f'''<text x="36" y="447" class="muted" font-size="12">{today.year} 年进度 · {progress:.1%}</text>
<text x="844" y="447" text-anchor="end" class="muted" font-size="12">绿色 / 今天 · 紫色 / 周末</text>
<rect x="36" y="461" width="808" height="5" rx="2.5" fill="#26344c"/>
<rect x="36" y="461" width="{808*progress:.2f}" height="5" rx="2.5" fill="#80e8c0"/>
</svg>''')
    return '\n'.join(parts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', type=date.fromisoformat, help='Override date for previews')
    args = parser.parse_args()
    today = args.date or datetime.now(ZoneInfo('Asia/Shanghai')).date()
    output = ROOT / 'assets' / 'profile-calendar.svg'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(today), encoding='utf-8')
    print(f'Generated {output} for {today}')
