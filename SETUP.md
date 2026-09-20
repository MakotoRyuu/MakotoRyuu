# 使用说明

将本目录中的 README.md、assets、scripts 和 .github 合并到 MakotoRyuu/MakotoRyuu 仓库。保留仓库原有 LICENSE。

提交并推送到默认分支后，在 GitHub Actions 中检查 Update profile calendar；也可以点击 Run workflow 手动刷新。仓库必须公开，名称必须与 GitHub 用户名相同，个人资料页才会展示 README。

工作流每天北京时间 00:17 生成新的 SVG，并提交有变化的图片。实际执行及 GitHub 图片缓存刷新可能延迟。公开仓库连续 60 天没有活动时，定时工作流可能被停用。仓库或组织策略需要允许 GitHub Actions 写入内容；受保护分支可能阻止机器人直接推送。

本地预览：`python3 scripts/update_profile.py`。仅使用 Python 3.9+ 标准库，无需密钥或第三方图片服务。可用 `--date 2026-12-31` 检查跨年布局。

当前版本包含当月、下月、今天标记、周末和年度进度。周末不等于法定休息日；本版本不标记节假日及调休。它借鉴了 hoochanlon 的“脚本生成 SVG + Actions 定时提交 + README 引用图片”机制，代码独立编写。

修改名字、标语、颜色和布局：编辑 scripts/update_profile.py，再运行一次生成脚本。README.md 可补充你自己的介绍。
