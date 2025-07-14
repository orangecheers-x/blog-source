import os
import re

def remove_tags_block_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 用非贪婪模式匹配 tags: 开始，到下一个 +++ 为止的内容
    pattern = r'(?ms)^tags:\s*\n.*?\n(?=^\+\+\+)'  # 跨行匹配，匹配 tags 到下一个 +++ 之前的所有内容
    new_content = re.sub(pattern, '', content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Cleaned: {file_path}")

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                remove_tags_block_from_file(os.path.join(root, file))

# 修改为你 Markdown 文件所在的目录
process_directory('content/posts')
