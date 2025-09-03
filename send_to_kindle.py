#!/usr/bin/env python3
"""
发送最新生成的EPUB文件到Kindle邮箱
"""

import os
import glob
import smtplib
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime
import argparse

def load_email_config():
    """加载邮件配置（优先使用环境变量）"""
    
    # 首先尝试从环境变量加载
    env_config = {
        'smtp_server': os.environ.get('SMTP_SERVER'),
        'smtp_port': os.environ.get('SMTP_PORT'),
        'sender_email': os.environ.get('SENDER_EMAIL'),
        'sender_password': os.environ.get('SENDER_PASSWORD'),
        'kindle_email': os.environ.get('KINDLE_EMAIL'),
        'subject': os.environ.get('EMAIL_SUBJECT', 'RSS Feed'),
        'body': os.environ.get('EMAIL_BODY', f'RSS订阅推送 - {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    }
    
    # 检查是否所有必要的环境变量都存在
    required_fields = ['smtp_server', 'smtp_port', 'sender_email', 'sender_password', 'kindle_email']
    if all(env_config.get(field) for field in required_fields):
        print("✅ 使用环境变量配置")
        # 转换端口为整数
        env_config['smtp_port'] = int(env_config['smtp_port'])
        return env_config
    
    # 如果环境变量不完整，尝试从配置文件加载
    config_file = 'email_config.yaml'
    if not os.path.exists(config_file):
        print(f"❌ 配置文件 {config_file} 不存在，且环境变量未设置")
        print("请创建配置文件或设置环境变量")
        return None
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 验证必要的配置项
    for field in required_fields:
        if field not in config:
            print(f"❌ 配置文件缺少必要字段: {field}")
            return None
    
    print("✅ 使用配置文件")
    return config

def get_latest_epub():
    """获取最新生成的EPUB文件"""
    # 查找所有的EPUB文件（支持多种命名格式）
    epub_files = glob.glob('*.epub')
    if not epub_files:
        print("❌ 没有找到EPUB文件")
        return None
    
    # 按修改时间排序，获取最新的文件
    latest_file = max(epub_files, key=os.path.getmtime)
    file_size = os.path.getsize(latest_file) / (1024 * 1024)  # 转换为MB
    
    print(f"📚 找到最新EPUB文件: {latest_file}")
    print(f"   文件大小: {file_size:.2f} MB")
    
    # Kindle邮件附件限制为25MB
    if file_size > 25:
        print(f"⚠️  警告: 文件大小超过25MB，可能无法发送到Kindle")
    
    return latest_file

def send_to_kindle(epub_file, config):
    """发送EPUB文件到Kindle邮箱"""
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = config['sender_email']
        msg['To'] = config['kindle_email']
        msg['Subject'] = config.get('subject', 'RSS Feed')
        
        # 添加邮件正文
        body = config.get('body', f'RSS订阅推送 - {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 添加EPUB附件
        with open(epub_file, 'rb') as f:
            attachment = MIMEBase('application', 'epub+zip')
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(epub_file)}'
            )
            msg.attach(attachment)
        
        # 连接SMTP服务器并发送
        print(f"📧 正在发送邮件到 {config['kindle_email']}...")
        
        # 根据端口选择加密方式
        if config['smtp_port'] == 587:
            # STARTTLS
            server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
            server.starttls()
        elif config['smtp_port'] == 465:
            # SSL
            server = smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'])
        else:
            # 无加密
            server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        
        server.login(config['sender_email'], config['sender_password'])
        server.send_message(msg)
        server.quit()
        
        print(f"✅ 邮件发送成功！")
        print(f"   请检查Kindle设备或邮箱确认接收")
        
        return True
        
    except Exception as e:
        print(f"❌ 发送邮件失败: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='发送EPUB文件到Kindle邮箱')
    parser.add_argument('-f', '--file', help='指定要发送的EPUB文件')
    parser.add_argument('-c', '--config', default='email_config.yaml', help='指定配置文件')
    args = parser.parse_args()
    
    # 加载配置
    config = load_email_config()
    if not config:
        print("\n请创建 email_config.yaml 文件，参考 email_config_example.yaml")
        return
    
    # 获取EPUB文件
    if args.file:
        if not os.path.exists(args.file):
            print(f"❌ 指定的文件不存在: {args.file}")
            return
        epub_file = args.file
        print(f"📚 使用指定文件: {epub_file}")
    else:
        epub_file = get_latest_epub()
        if not epub_file:
            return
    
    # 发送邮件
    send_to_kindle(epub_file, config)

if __name__ == "__main__":
    main()