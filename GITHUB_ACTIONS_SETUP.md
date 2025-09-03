# GitHub Actions 自动推送设置指南

## 概述
使用 GitHub Actions 自动生成 RSS EPUB 并发送到 Kindle，所有敏感信息都通过 GitHub Secrets 管理。

## 设置步骤

### 1. Fork 或上传代码到 GitHub

确保你的仓库包含以下文件：
- `main.py` - RSS 转 EPUB 主程序
- `send_to_kindle.py` - 邮件发送程序
- `rss_and_send.py` - 组合脚本
- `config.yaml` - RSS 源配置
- `.github/workflows/rss_to_kindle.yml` - GitHub Actions 工作流
- `requirements.txt` - Python 依赖

### 2. 配置 GitHub Secrets 和 Variables

#### 配置方式一：使用 Repository Variables（推荐）

在你的 GitHub 仓库中设置 Variables：

1. 进入仓库页面
2. 点击 `Settings` → `Secrets and variables` → `Actions`
3. 选择 `Variables` 标签
4. 点击 `New repository variable`
5. 添加 `CONFIG_YAML` 变量，内容为完整的 config.yaml 配置

**CONFIG_YAML 示例内容：**
```yaml
Settings:
  max_history: 7
  load_images: true

Feeds:
  - url: "https://sspai.com/feed"
    name: "少数派"
    title: "少数派精选"
    enabled: true
    resolve_link:
      enabled: true
      method: "readability"
```

#### 配置方式二：使用 Secrets（用于私密RSS源）

如果你的RSS源包含私密信息，使用 Secrets：

1. 选择 `Secrets` 标签
2. 点击 `New repository secret`
3. 添加 `CONFIG_YAML` Secret，内容同上

#### 邮件配置 Secrets

添加以下 Secrets 用于邮件发送：

| Secret 名称 | 说明 | 示例值 |
|------------|------|--------|
| `SMTP_SERVER` | SMTP 服务器地址 | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP 端口 | `587` |
| `SENDER_EMAIL` | 发件人邮箱 | `your_email@gmail.com` |
| `SENDER_PASSWORD` | 邮箱密码/授权码 | `your_app_password` |
| `KINDLE_EMAIL` | Kindle 接收邮箱 | `your_kindle@kindle.com` |

### 3. 各邮箱服务商配置

#### Gmail
- **SMTP_SERVER**: `smtp.gmail.com`
- **SMTP_PORT**: `587`
- **SENDER_PASSWORD**: 需要生成应用专用密码
  1. 开启两步验证
  2. 访问 https://myaccount.google.com/apppasswords
  3. 生成应用专用密码

#### QQ 邮箱
- **SMTP_SERVER**: `smtp.qq.com`
- **SMTP_PORT**: `587`
- **SENDER_PASSWORD**: 使用授权码（不是QQ密码）
  1. 登录 QQ 邮箱
  2. 设置 → 账户 → POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务
  3. 生成授权码

#### 163 邮箱
- **SMTP_SERVER**: `smtp.163.com`
- **SMTP_PORT**: `465`
- **SENDER_PASSWORD**: 使用授权码
  1. 登录 163 邮箱
  2. 设置 → POP3/SMTP/IMAP
  3. 开启服务并获取授权码

#### Outlook
- **SMTP_SERVER**: `smtp-mail.outlook.com`
- **SMTP_PORT**: `587`
- **SENDER_PASSWORD**: 使用邮箱密码或应用密码

### 4. 配置 Kindle 白名单

**重要**：必须将发件邮箱添加到 Kindle 白名单

1. 登录亚马逊账户
2. 进入 **管理我的内容和设备**
3. 点击 **首选项** 标签
4. 找到 **个人文档设置**
5. 在 **已认可的发件人电子邮箱列表** 中添加你的 `SENDER_EMAIL`

### 5. 调整定时任务（可选）

编辑 `.github/workflows/rss_to_kindle.yml` 中的 cron 表达式：

```yaml
on:
  schedule:
    - cron: '0 23 * * *'  # UTC 时间，相当于北京时间早上 7 点
```

常用时间设置：
- `0 23 * * *` - 每天北京时间早上 7 点
- `0 11 * * *` - 每天北京时间晚上 7 点
- `0 1 * * 1,3,5` - 每周一三五北京时间早上 9 点
- `0 14 * * 0` - 每周日北京时间晚上 10 点

### 6. 手动触发测试

1. 进入仓库的 `Actions` 标签
2. 选择 `RSS to Kindle` 工作流
3. 点击 `Run workflow` → `Run workflow`
4. 查看运行日志确认是否成功

## 功能特性

- ✅ 自动定时运行（每天早上 7 点）
- ✅ 支持手动触发
- ✅ 所有敏感信息通过 Secrets 管理
- ✅ 自动缓存依赖加快运行速度
- ✅ 保留 EPUB 备份（7 天）
- ✅ 自动清理旧文件

## 查看运行结果

### 查看运行日志
1. 进入 `Actions` 标签
2. 点击具体的运行记录
3. 查看各步骤的详细日志

### 下载 EPUB 备份
1. 进入具体的运行记录
2. 在页面底部找到 `Artifacts`
3. 下载 `rss-epub-xxx` 文件

## 故障排查

### Action 运行失败
- 检查 Secrets 是否正确配置
- 查看具体的错误日志
- 确认 RSS 源可以正常访问

### 邮件发送失败
- 确认 SMTP 设置正确
- 检查邮箱是否需要应用专用密码
- 验证 Kindle 邮箱地址是否正确

### Kindle 未收到邮件
- 确认已添加发件邮箱到白名单
- 检查文件大小是否超过 25MB
- 查看垃圾邮件文件夹

## 本地测试

使用环境变量在本地测试：

```bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SENDER_EMAIL="your_email@gmail.com"
export SENDER_PASSWORD="your_password"
export KINDLE_EMAIL="your_kindle@kindle.com"

python rss_and_send.py
```

## 安全建议

1. **不要**在代码中硬编码任何密码
2. **不要**将 `email_config.yaml` 提交到仓库
3. 定期更新邮箱密码/授权码
4. 仅给仓库必要的权限
5. 如果是私有仓库，确保只有信任的人有访问权限