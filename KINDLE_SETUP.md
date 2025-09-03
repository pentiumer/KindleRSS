# Kindle 邮件推送设置指南

## 功能说明
自动将生成的RSS EPUB文件发送到你的Kindle设备。

## 快速开始

### 1. 配置邮件设置
复制示例配置文件并编辑：
```bash
cp email_config_example.yaml email_config.yaml
```

编辑 `email_config.yaml` 填写：
- SMTP服务器信息
- 发件人邮箱和密码
- Kindle接收邮箱

### 2. 配置Kindle邮箱
1. 登录亚马逊账户
2. 进入"管理我的内容和设备"
3. 选择"首选项" → "个人文档设置"
4. 记下你的Kindle邮箱地址（如 `yourname_123@kindle.com`）
5. **重要**：将发件人邮箱添加到"已认可的发件人电子邮箱列表"

### 3. 使用方法

#### 手动发送最新的EPUB
```bash
python send_to_kindle.py
```

#### 生成并自动发送
```bash
python rss_and_send.py
```

#### 仅生成不发送
```bash
python rss_and_send.py --no-send
```

#### 指定文件发送
```bash
python send_to_kindle.py -f specific_file.epub
```

## 邮箱配置说明

### Gmail
```yaml
smtp_server: smtp.gmail.com
smtp_port: 587
```
注意：需要开启两步验证并生成应用专用密码

### QQ邮箱
```yaml
smtp_server: smtp.qq.com
smtp_port: 587
```
注意：使用授权码，不是QQ密码

### 163邮箱
```yaml
smtp_server: smtp.163.com
smtp_port: 465
```
注意：使用授权码

### Outlook
```yaml
smtp_server: smtp-mail.outlook.com
smtp_port: 587
```

## 定时推送

使用 crontab 设置定时任务：

```bash
# 编辑定时任务
crontab -e

# 添加任务（每天早上7点推送）
0 7 * * * cd /Users/haleyc/vscode/RSS && python3 rss_and_send.py >> cron_log.txt 2>&1
```

更多定时任务示例见 `cron_setup.sh`

## 注意事项

1. **文件大小限制**：Kindle邮件附件限制为25MB
2. **格式支持**：确保发送EPUB格式（Kindle支持）
3. **邮箱白名单**：必须将发件邮箱添加到Kindle的认可发件人列表
4. **网络要求**：需要稳定的网络连接发送邮件

## 故障排查

### 邮件发送失败
- 检查网络连接
- 验证SMTP设置是否正确
- 确认邮箱密码/授权码是否正确
- 检查是否需要应用专用密码

### Kindle未收到
- 确认Kindle邮箱地址正确
- 检查是否添加了发件人白名单
- 查看垃圾邮件文件夹
- 确认文件大小未超过25MB

### 定时任务不执行
- 使用 `crontab -l` 确认任务已添加
- 检查Python路径是否正确
- 查看 `cron_log.txt` 日志文件