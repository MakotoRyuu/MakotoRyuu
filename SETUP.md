# GitHub 主页日历

主页直接采用 hoochanlon/hoochanlon 的 README 展示方式：外部 profile-calendar 图片 + 仓库内的中国节假日日历 SVG。

日历脚本、初始 SVG 和缓存直接复制自本地 hoochanlon 仓库。保留原有样式、字体、节假日和调休标记。README 的日历地址已指向 MakotoRyuu/MakotoRyuu 的 main 分支。

GitHub Actions 每天北京时间 00:01 更新日历，也可以手动运行 Update Holiday Calendar。第一次推送本工作流时会自动运行。需要允许 Actions 写入仓库内容。

本地更新：先安装 `fonttools brotli`，再运行 `TZ=Asia/Shanghai python3 holiday/generate-holiday-svg.py`。脚本会获取节假日数据和字体，网络不可用时使用原脚本的回退逻辑。

来源：https://github.com/hoochanlon/hoochanlon 。仅适配了仓库地址、main 分支、首次运行触发器，并移除了不适用的 Hugo 部署提示；未复制独立 Hugo 网站。

## 每日一言（独立图片）

编辑 `quotes/quotes.txt`，每行一句，格式为 `名言正文 | 作者或出处`，也可以只写正文。空行和以 `#` 开头的行会被忽略。示例可全部替换，但至少保留一句。

Python 按北京时间日期从列表中顺序循环选择一句（以 2026-09-20 为第一句的起点），同一天重复运行不切换；修改列表顺序或数量后当天选句可能改变。每日一言输出为 `quotes/daily-quote.svg`，与 `holiday/holiday-calendar.svg` 是两张独立静态图片，放在节假日日历上方。无动画。字体与日历使用相同来源，名言与作者同行显示，图片固定为 64 高；长句会缩小字号，特别长的句子会横向压缩。

工作流每天北京时间 00:01 同时生成两张图片，再一起提交。修改名言文件并推送到 main 后也会触发更新；GitHub 图片缓存刷新可能稍有延迟。

本地生成：`python3 quotes/generate-quote-svg.py`（依赖与日历相同）。指定日期预览：`python3 quotes/generate-quote-svg.py --date 2026-09-21`。
