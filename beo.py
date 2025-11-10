import time
import sys
import os

# Làm đẹp giao diện terminal (xóa màn hình)
os.system('cls' if os.name == 'nt' else 'clear')

def type_effect(text, delay=0.05):
    """Hiệu ứng chữ xuất hiện từng ký tự"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Câu hỏi vui
question = "Hiếu có bị gay không?"
type_effect(question)
time.sleep(1)

print("\nĐang xử lý câu trả lời...\n")
time.sleep(1)

# Đếm ngược
for i in range(5, 0, -1):
    sys.stdout.write(f"Đếm ngược: {i}...\r")
    sys.stdout.flush()
    time.sleep(1)

# Hiệu ứng trả lời
time.sleep(0.5)
type_effect("\nCâu trả lời là...")
time.sleep(1)
type_effect("CÓ 😎🌈")

print("\n(Chill tí thôi nha Hiếu :)) )")
