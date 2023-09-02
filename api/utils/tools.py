import re

def validate_index_name(index_name: str):
    
    # 正则表达式模式
    pattern = r"^[a-z0-9][a-z0-9\-]*[a-z0-9]$"

    if not re.match(pattern, index_name):
        # 将非法字符替换为 '-'
        index_name = re.sub(r"[^a-z0-9]", "-", index_name)
        # 移除连续多个 '-' 的情况
        index_name = re.sub(r"-+", "-", index_name)
        # 移除开头和结尾的 '-' 字符
        index_name = index_name.strip("-")
        # 将所有字符转为小写
        index_name = index_name.lower()

    return index_name