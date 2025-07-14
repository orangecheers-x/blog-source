import os
import re

def insert_math_true(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 找到最后一个 +++ 的位置
    matches = list(re.finditer(r'^\+\+\+$', content, re.MULTILINE))
    if not matches:
        return

    last_plus_pos = matches[1].start()

    # 拿到 frontmatter 内容
    front_matter = content[:last_plus_pos]

    # 如果已经有 math = true，就不动
    if re.search(r'^math\s*=\s*true$', front_matter, re.MULTILINE):
        return

    # 在最后一个 +++ 前插入 math = true
    new_front_matter = front_matter.rstrip() + '\nmath = true\n'
    new_content = new_front_matter + content[last_plus_pos:]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated math = true: {file_path}")

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                insert_math_true(os.path.join(root, file))

# 设置你的 Markdown 文件目录
process_directory('content/posts')
