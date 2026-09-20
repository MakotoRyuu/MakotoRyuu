# GitHub 主页日历

主页直接采用 hoochanlon/hoochanlon 的 README 展示方式：外部 profile-calendar 图片 + 仓库内的中国节假日日历 SVG。

日历脚本、初始 SVG 和缓存直接复制自本地 hoochanlon 仓库。保留原有样式、字体、节假日和调休标记。README 的日历地址已指向 MakotoRyuu/MakotoRyuu 的 main 分支。

GitHub Actions 每天北京时间 00:01 更新日历，也可以手动运行 Update Holiday Calendar。第一次推送本工作流时会自动运行。需要允许 Actions 写入仓库内容。

本地更新：先安装 `fonttools brotli`，再运行 `TZ=Asia/Shanghai python3 holiday/generate-holiday-svg.py`。脚本会获取节假日数据和字体，网络不可用时使用原脚本的回退逻辑。

来源：https://github.com/hoochanlon/hoochanlon 。仅适配了仓库地址、main 分支、首次运行触发器，并移除了不适用的 Hugo 部署提示；未复制独立 Hugo 网站。
