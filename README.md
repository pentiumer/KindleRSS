# KindleRSS
[![Static Badge](https://img.shields.io/badge/Readme-EN-blue)](README_EN.md)


将RSS订阅转换为EPUB电子书，并自动发送到Kindle设备。支持全文提取、图片嵌入、GitHub Actions自动化推送。

## ✨ 功能特性

- 📚 **RSS转EPUB** - 将多个RSS源合并为一本精美的EPUB电子书
- 🔍 **全文提取** - 支持从原网页提取完整文章内容（CSS选择器/Readability）
- 🖼️ **图片处理** - 自动下载并嵌入文章图片，支持防跨页显示
- 📧 **Kindle推送** - 自动发送到Kindle邮箱
- 🤖 **GitHub Actions** - 全自动定时生成和推送
- 📖 **智能导航** - 多级目录结构，方便阅读导航

## 🚀 快速开始

### 本地使用

1. **克隆仓库**
```bash
git clone https://github.com/ZRui-C/KindleRSS.git
cd KindleRSS
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置RSS源**
```bash
cp config.example.yaml config.yaml
# 编辑 config.yaml，添加你的RSS源
```

4. **生成EPUB**
```bash
python main.py
```

5. **发送到Kindle**（可选）
```bash
# 配置邮件设置
cp email_config.example.yaml email_config.yaml
# 编辑 email_config.yaml

# 发送最新的EPUB
python send_to_kindle.py

# 或生成并发送
python rss_and_send.py
```

### GitHub Actions 自动化

1. **Fork本仓库**

2. **配置GitHub Variables/Secrets**
   
   在仓库设置中配置：
   
   **RSS配置** (Variables或Secrets)：
   - `CONFIG_YAML` - 完整的config.yaml内容
   
   **邮件配置** (Secrets)：
   - `SMTP_SERVER` - SMTP服务器地址
   - `SMTP_PORT` - SMTP端口
   - `SENDER_EMAIL` - 发件人邮箱
   - `SENDER_PASSWORD` - 邮箱密码/授权码
   - `KINDLE_EMAIL` - Kindle接收邮箱

3. **配置Kindle白名单**
   
   将发件邮箱添加到Kindle的认可发件人列表

4. **自动运行**
   
   - 每天北京时间早上7点自动推送
   - 或手动触发：Actions → RSS to Kindle → Run workflow

详细设置见 [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)

## 📝 配置说明

### RSS源配置 (config.yaml)

```yaml
Settings:
  max_history: 7  # 保留最近N天的文章
  load_images: true  # 是否下载图片

Feeds:
  - url: "https://example.com/rss"
    name: "示例源"
    title: "示例标题"
    enabled: true
    resolve_link:  # 可选：提取全文
      enabled: true
      method: "readability"  # 或 "selector"
      selectors:  # method为selector时使用
        content: "article, .content"
        remove: ".ads, .comments"
      fallback: "readability"
```

### 邮件配置 (email_config.yaml)

参考 `email_config.example.yaml` 配置你的SMTP服务器信息。

支持的邮箱服务：
- Gmail（需要应用专用密码）
- QQ邮箱（需要授权码）
- 163邮箱（需要授权码）
- Outlook
- 其他SMTP服务器

## 📂 项目结构

```
.
├── main.py                 # 主程序：RSS转EPUB
├── send_to_kindle.py       # Kindle邮件发送
├── rss_and_send.py        # 组合脚本
├── config.yaml            # RSS源配置
├── email_config.yaml      # 邮件配置（需创建）
├── requirements.txt       # Python依赖
├── .github/
│   └── workflows/
│       ├── rss_to_kindle.yml      # 基础工作流
│       ├── rss_to_kindle_advanced.yml  # 高级工作流
│       └── test.yml               # 测试工作流
└── README.md              # 本文档
```

## 🛠️ 高级功能

### 全文提取模式

1. **Readability模式** - 自动识别文章主体
2. **CSS选择器模式** - 精确指定内容区域
3. **混合模式** - 选择器失败时自动切换到Readability

### 定时任务

使用crontab设置本地定时任务：
```bash
# 每天早上7点运行
0 7 * * * cd /path/to/rss-to-epub && python3 rss_and_send.py
```

### GitHub Actions工作流

- **基础版** - 每日自动推送
- **高级版** - 支持Release发布、自定义时间
- **测试版** - 代码提交时自动测试

## 🔧 故障排查

### 常见问题

1. **Kindle未收到邮件**
   - 检查是否添加发件邮箱到白名单
   - 确认文件大小未超过25MB
   - 查看垃圾邮件文件夹

2. **邮件发送失败**
   - 验证SMTP设置
   - 确认使用应用专用密码/授权码
   - 检查网络连接

3. **RSS解析失败**
   - 确认RSS源URL正确
   - 检查网络是否可访问
   - 查看是否需要代理

## 📖 文档

- [Kindle推送设置](KINDLE_SETUP.md)
- [GitHub Actions设置](GITHUB_ACTIONS_SETUP.md)
- [配置示例](config.example.yaml)

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 🙏 致谢

- [ebooklib](https://github.com/aerkalov/ebooklib) - EPUB生成库
- [feedparser](https://github.com/kurtmckee/feedparser) - RSS解析库
- [readability-lxml](https://github.com/buriy/python-readability) - 网页内容提取

---

如有问题或建议，请提交[Issue](https://github.com/ZRui-C/KindleRSS/issues)。