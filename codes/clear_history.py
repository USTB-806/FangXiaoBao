# 清除 conversation_history.txt 文件内容
history_file_path = "conversation_history.txt"

# 打开文件并清空内容
with open(history_file_path, "w", encoding="utf-8") as file:
    file.write("")