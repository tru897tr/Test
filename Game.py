import json
import os
from datetime import datetime, timedelta
import random
import time
import traceback
import sys

# File lưu dữ liệu
DATA_FILE = "game_data.json"

# Màu sắc cho terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = '\033[90m'

# Danh sách động vật theo độ hiếm với stats
ANIMALS = {
    "Common": [
        {"name": "bee", "emoji": "🐝", "chance": 11.6, "points": 1, "sell_price": 1, "exp": 1,
         "stats": {"hp": 1, "atk": 1, "pr": 2, "wp": 3, "mag": 3, "mr": 1}},
        {"name": "bug", "emoji": "🐛", "chance": 11.6, "points": 1, "sell_price": 1, "exp": 1,
         "stats": {"hp": 3, "atk": 2, "pr": 2, "wp": 4, "mag": 2, "mr": 2}},
        {"name": "snail", "emoji": "🐌", "chance": 11.6, "points": 1, "sell_price": 1, "exp": 1,
         "stats": {"hp": 8, "atk": 1, "pr": 2, "wp": 3, "mag": 5, "mr": 1}},
        {"name": "butterfly", "emoji": "🦋", "chance": 11.6, "points": 1, "sell_price": 1, "exp": 1,
         "stats": {"hp": 1, "atk": 1, "pr": 1, "wp": 5, "mag": 5, "mr": 2}},
        {"name": "beetle", "emoji": "🪲", "chance": 11.6, "points": 1, "sell_price": 1, "exp": 1,
         "stats": {"hp": 4, "atk": 2, "pr": 2, "wp": 3, "mag": 2, "mr": 2}}
    ],
    "Uncommon": [
        {"name": "chick", "emoji": "🐤", "chance": 6.0, "points": 5, "sell_price": 3, "exp": 10,
         "stats": {"hp": 3, "atk": 2, "pr": 3, "wp": 3, "mag": 3, "mr": 2}},
        {"name": "mouse", "emoji": "🐭", "chance": 6.0, "points": 5, "sell_price": 3, "exp": 10,
         "stats": {"hp": 3, "atk": 3, "pr": 2, "wp": 3, "mag": 3, "mr": 2}},
        {"name": "chicken", "emoji": "🐔", "chance": 6.0, "points": 5, "sell_price": 3, "exp": 10,
         "stats": {"hp": 3, "atk": 4, "pr": 3, "wp": 2, "mag": 2, "mr": 2}},
        {"name": "rabbit", "emoji": "🐰", "chance": 6.0, "points": 5, "sell_price": 3, "exp": 10,
         "stats": {"hp": 3, "atk": 4, "pr": 2, "wp": 3, "mag": 2, "mr": 2}},
        {"name": "chipmunk", "emoji": "🐿️", "chance": 6.0, "points": 5, "sell_price": 3, "exp": 10,
         "stats": {"hp": 3, "atk": 5, "pr": 2, "wp": 3, "mag": 2, "mr": 1}}
    ],
    "Rare": [
        {"name": "sheep", "emoji": "🐑", "chance": 2.0, "points": 20, "sell_price": 10, "exp": 20,
         "stats": {"hp": 5, "atk": 2, "pr": 2, "wp": 3, "mag": 1, "mr": 4}},
        {"name": "pig", "emoji": "🐷", "chance": 2.0, "points": 20, "sell_price": 10, "exp": 20,
         "stats": {"hp": 4, "atk": 2, "pr": 3, "wp": 2, "mag": 2, "mr": 4}},
        {"name": "cow", "emoji": "🐮", "chance": 2.0, "points": 20, "sell_price": 10, "exp": 20,
         "stats": {"hp": 5, "atk": 4, "pr": 3, "wp": 1, "mag": 1, "mr": 3}},
        {"name": "dog", "emoji": "🐶", "chance": 2.0, "points": 20, "sell_price": 10, "exp": 20,
         "stats": {"hp": 4, "atk": 6, "pr": 3, "wp": 1, "mag": 1, "mr": 2}},
        {"name": "cat", "emoji": "🐱", "chance": 2.0, "points": 20, "sell_price": 10, "exp": 20,
         "stats": {"hp": 3, "atk": 1, "pr": 1, "wp": 6, "mag": 3, "mr": 3}}
    ],
    "Epic": [],
    "Mythical": [],
    "Patreon": [],
    "Custom Patreon": [],
    "Legendary": [],
    "Gem": [],
    "Bot Distorted": [],
    "Fabled": [],
    "Special": [],
    "Hidden": []
}

def check_requirements():
    """Kiểm tra yêu cầu hệ thống trước khi chạy game"""
    print(Colors.OKCYAN + "=" * 70 + Colors.ENDC)
    print(Colors.BOLD + "🔍 ĐANG KIỂM TRA HỆ THỐNG..." + Colors.ENDC)
    print(Colors.OKCYAN + "=" * 70 + Colors.ENDC)
    
    issues = []
    
    # Kiểm tra Python version
    print("\n📌 Kiểm tra Python version...", end=" ")
    if sys.version_info < (3, 6):
        issues.append("Python version quá cũ (cần >= 3.6)")
        print(Colors.FAIL + "❌" + Colors.ENDC)
    else:
        print(Colors.OKGREEN + f"✓ Python {sys.version_info.major}.{sys.version_info.minor}" + Colors.ENDC)
    
    # Kiểm tra thư viện cần thiết
    required_modules = ['json', 'os', 'datetime', 'random', 'time', 'traceback', 'sys']
    print("📌 Kiểm tra thư viện cần thiết...", end=" ")
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        issues.append(f"Thiếu thư viện: {', '.join(missing_modules)}")
        print(Colors.FAIL + "❌" + Colors.ENDC)
    else:
        print(Colors.OKGREEN + "✓ Đầy đủ" + Colors.ENDC)
    
    # Kiểm tra quyền ghi file
    print("📌 Kiểm tra quyền ghi file...", end=" ")
    try:
        test_file = "test_write_permission.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print(Colors.OKGREEN + "✓ OK" + Colors.ENDC)
    except:
        issues.append("Không có quyền ghi file trong thư mục hiện tại")
        print(Colors.FAIL + "❌" + Colors.ENDC)
    
    # Kiểm tra màn hình terminal
    print("📌 Kiểm tra kích thước terminal...", end=" ")
    try:
        cols = os.get_terminal_size().columns
        if cols < 70:
            issues.append(f"Terminal quá nhỏ (hiện tại: {cols}, cần ít nhất 70)")
            print(Colors.WARNING + f"⚠ {cols} cols" + Colors.ENDC)
        else:
            print(Colors.OKGREEN + f"✓ {cols} cols" + Colors.ENDC)
    except:
        print(Colors.WARNING + "⚠ Không xác định được" + Colors.ENDC)
    
    print(Colors.OKCYAN + "=" * 70 + Colors.ENDC)
    
    if issues:
        print(Colors.FAIL + "\n⚠️  PHÁT HIỆN VẤN ĐỀ:" + Colors.ENDC)
        for issue in issues:
            print(f"   • {issue}")
        print("\n" + Colors.WARNING + "Game có thể không hoạt động đúng!" + Colors.ENDC)
        choice = input("\nBạn có muốn tiếp tục? (y/n): ").strip().lower()
        if choice != 'y':
            print(Colors.FAIL + "Đã hủy chạy game." + Colors.ENDC)
            sys.exit(0)
    else:
        print(Colors.OKGREEN + "\n✅ HỆ THỐNG SẴN SÀNG!" + Colors.ENDC)
        time.sleep(1)

def clear_screen():
    """Xóa màn hình để gọn gàng"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_with_effect(text, delay=0.02, color=""):
    """In text với hiệu ứng đánh máy"""
    for char in text:
        print(color + char + Colors.ENDC, end='', flush=True)
        time.sleep(delay)
    print()

def print_box(text, color=Colors.OKCYAN, width=70):
    """In text trong box đẹp với căn chỉnh đúng"""
    lines = text.split('\n')
    
    print(color + "╔" + "═" * (width - 2) + "╗" + Colors.ENDC)
    for line in lines:
        # Loại bỏ các ký tự màu để tính độ dài thực
        clean_line = line
        for color_code in [Colors.HEADER, Colors.OKBLUE, Colors.OKCYAN, Colors.OKGREEN, 
                          Colors.WARNING, Colors.FAIL, Colors.ENDC, Colors.BOLD, Colors.UNDERLINE, Colors.GRAY]:
            clean_line = clean_line.replace(color_code, '')
        
        padding = width - len(clean_line) - 4
        if padding < 0:
            padding = 0
        print(color + "║ " + Colors.ENDC + line + " " * padding + color + " ║" + Colors.ENDC)
    print(color + "╚" + "═" * (width - 2) + "╝" + Colors.ENDC)

def loading_animation(text="Loading", duration=1):
    """Hiệu ứng loading"""
    animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{Colors.OKCYAN}{animation[i % len(animation)]} {text}...{Colors.ENDC}", end='', flush=True)
        time.sleep(0.1)
        i += 1
    print("\r" + " " * 50 + "\r", end='')

class Game:
    def __init__(self):
        try:
            self.data = self.load_data()
        except Exception as e:
            self.show_error("Lỗi khởi tạo game", e)
            sys.exit(1)
    
    def get_exp_needed(self, level):
        """Tính EXP cần thiết cho level tiếp theo"""
        return 100 + (level - 1) * 20
    
    def get_exp_percent(self):
        """Tính phần trăm EXP hiện tại"""
        needed = self.get_exp_needed(self.data['level'])
        return (self.data['exp'] / needed) * 100
        
    def show_error(self, message, error):
        """Hiển thị lỗi chi tiết với debug info nhưng không tự động thoát"""
        clear_screen()
        print(Colors.FAIL + "╔" + "═" * 68 + "╗" + Colors.ENDC)
        print(Colors.FAIL + "║" + " " * 24 + "⚠️  LỖI HỆ THỐNG  ⚠️" + " " * 23 + "║" + Colors.ENDC)
        print(Colors.FAIL + "╚" + "═" * 68 + "╝" + Colors.ENDC)
        print(f"\n{Colors.BOLD}Mô tả lỗi:{Colors.ENDC} {message}")
        print(f"{Colors.BOLD}Loại lỗi:{Colors.ENDC} {type(error).__name__}")
        print(f"{Colors.BOLD}Chi tiết:{Colors.ENDC} {str(error)}")
        print(f"\n{Colors.GRAY}{'='*70}")
        print("DEBUG TRACEBACK:")
        print('='*70)
        traceback.print_exc()
        print('='*70 + Colors.ENDC)
        print(f"\n{Colors.OKGREEN}Game sẽ tiếp tục chạy...{Colors.ENDC}")
        input(f"\n{Colors.WARNING}Nhấn Enter để tiếp tục...{Colors.ENDC}")
        
    def load_data(self):
        """Tải dữ liệu từ file hoặc tạo mới nếu chưa có"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "zoo" not in data:
                        data["zoo"] = {}
                    if "team" not in data:
                        data["team"] = []
                    if "stats" not in data:
                        data["stats"] = {}
                    if "animals_caught" not in data["stats"]:
                        data["stats"]["animals_caught"] = 0
                    if "daily_streak" not in data:
                        data["daily_streak"] = 0
                    if "total_daily_collected" not in data:
                        data["total_daily_collected"] = 0
                    return data
            except Exception as e:
                self.show_error("Không thể đọc file dữ liệu", e)
                return self.create_new_data()
        else:
            print_with_effect("🎮 Chào mừng đến với game! Tạo dữ liệu mới...", 0.03, Colors.OKGREEN)
            time.sleep(1)
            return self.create_new_data()
    
    def create_new_data(self):
        """Tạo dữ liệu mới cho người chơi"""
        return {
            "coins": 100,
            "level": 1,
            "exp": 0,
            "last_daily":                     for idx, animal_name in enumerate(self.data["team"], 1):
                        animal_data = self.get_animal_data(animal_name)
                        if animal_data:
                            real_stats = self.calculate_real_stats(animal_name, self.data['level'])
                            print(f"  {idx}. {animal_data['emoji']} {animal_name.capitalize()}")
                            print(f"     ❤️  HP: {real_stats['hp']} | ⚔️  ATK: {real_stats['atk']} | 🛡️  PR: {real_stats['pr']}%")
                            print(f"     💎 WP: {real_stats['wp']} | ✨ MAG: {real_stats['mag']} | 🌟 MR: {real_stats['mr']}%")
                
                print(f"\n1. Thêm pet vào đội")
                print(f"2. Tháo pet khỏi đội")
                print(f"0. Quay lại")
                
                choice = input(f"\n{Colors.OKCYAN}👉 Chọn: {Colors.ENDC}").strip()
                
                if choice == "1":
                    if len(self.data["team"]) >= 3:
                        print(f"\n{Colors.FAIL}❌ Đội đã đầy (tối đa 3 pet)!{Colors.ENDC}")
                        time.sleep(1.5)
                        continue
                    self.add_to_team()
                elif choice == "2":
                    if not self.data["team"]:
                        print(f"\n{Colors.FAIL}❌ Đội chưa có pet nào!{Colors.ENDC}")
                        time.sleep(1.5)
                        continue
                    self.remove_from_team()
                elif choice == "0":
                    return
                else:
                    print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                    time.sleep(1)
                    
        except Exception as e:
            self.show_error("Lỗi khi quản lý đội hình", e)
    
    def add_to_team(self):
        """Thêm pet vào đội"""
        try:
            clear_screen()
            print(Colors.OKGREEN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(Colors.OKGREEN + "║" + " " * 25 + "➕ THÊM PET VÀO ĐỘI" + " " * 24 + "║" + Colors.ENDC)
            print(Colors.OKGREEN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            
            if not self.data["zoo"]:
                print(f"\n{Colors.FAIL}❌ Bạn chưa có pet nào!{Colors.ENDC}")
                input(f"\n{Colors.GRAY}Nhấn Enter để quay lại...{Colors.ENDC}")
                return
            
            print(f"\n{Colors.BOLD}Chọn pet để thêm vào đội:{Colors.ENDC}\n")
            
            available_animals = []
            index = 1
            for animal_name in self.data["zoo"].keys():
                if animal_name not in self.data["team"]:
                    animal_data = self.get_animal_data(animal_name)
                    if animal_data:
                        print(f"{index}. {animal_data['emoji']} {animal_name.capitalize()}")
                        available_animals.append(animal_name)
                        index += 1
            
            if not available_animals:
                print(f"  {Colors.GRAY}(Tất cả pet đã ở trong đội){Colors.ENDC}")
                input(f"\n{Colors.GRAY}Nhấn Enter để quay lại...{Colors.ENDC}")
                return
            
            print(f"\n0. Quay lại")
            
            choice = input(f"\n{Colors.OKCYAN}👉 Chọn số: {Colors.ENDC}").strip()
            
            if choice == "0":
                return
            
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(available_animals):
                    selected_animal = available_animals[choice_idx]
                    self.data["team"].append(selected_animal)
                    self.save_data()
                    print(f"\n{Colors.OKGREEN}✅ Đã thêm {selected_animal} vào đội!{Colors.ENDC}")
                    time.sleep(1.5)
                else:
                    print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                    time.sleep(1)
            except ValueError:
                print(f"\n{Colors.FAIL}❌ Vui lòng nhập số hợp lệ!{Colors.ENDC}")
                time.sleep(1)
                
        except Exception as e:
            self.show_error("Lỗi khi thêm pet vào đội", e)
    
    def remove_from_team(self):
        """Tháo pet khỏi đội"""
        try:
            clear_screen()
            print(Colors.FAIL + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(Colors.FAIL + "║" + " " * 25 + "➖ THÁO PET KHỎI ĐỘI" + " " * 24 + "║" + Colors.ENDC)
            print(Colors.FAIL + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            
            print(f"\n{Colors.BOLD}Chọn pet để tháo khỏi đội:{Colors.ENDC}\n")
            
            for idx, animal_name in enumerate(self.data["team"], 1):
                animal_data = self.get_animal_data(animal_name)
                if animal_data:
                    print(f"{idx}. {animal_data['emoji']} {animal_name.capitalize()}")
            
            print(f"\n0. Quay lại")
            
            choice = input(f"\n{Colors.OKCYAN}👉 Chọn số: {Colors.ENDC}").strip()
            
            if choice == "0":
                return
            
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(self.data["team"]):
                    removed_animal = self.data["team"].pop(choice_idx)
                    self.save_data()
                    print(f"\n{Colors.OKGREEN}✅ Đã tháo {removed_animal} khỏi đội!{Colors.ENDC}")
                    time.sleep(1.5)
                else:
                    print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                    time.sleep(1)
            except ValueError:
                print(f"\n{Colors.FAIL}❌ Vui lòng nhập số hợp lệ!{Colors.ENDC}")
                time.sleep(1)
                
        except Exception as e:
            self.show_error("Lỗi khi tháo pet khỏi đội", e)
    
    def has_any_animal_in_rarity(self, rarity):
        """Kiểm tra xem người chơi có động vật nào trong độ hiếm này không"""
        animals = ANIMALS.get(rarity, [])
        for animal in animals:
            if animal["name"] in self.data["zoo"]:
                return True
        return False
    
    def get_zoo_points(self):
        """Tính điểm sở thú theo độ hiếm"""
        total_points = 0
        for animal_name, count in self.data["zoo"].items():
            for rarity, animals in ANIMALS.items():
                for animal in animals:
                    if animal["name"] == animal_name:
                        total_points += count * animal["points"]
                        break
        return total_points
    
    def show_zoo(self):
        """Hiển thị sở thú"""
        try:
            clear_screen()
            print(Colors.OKCYAN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(Colors.OKCYAN + "║" + " " * 30 + "🦁 SỞ THÚ 🦁" + " " * 27 + "║" + Colors.ENDC)
            print(Colors.OKCYAN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            
            rarity_colors = {
                "Common": Colors.GRAY,
                "Uncommon": Colors.OKGREEN,
                "Rare": Colors.OKBLUE
            }
            
            total_unique = len(self.data["zoo"])
            total_caught = sum(self.data["zoo"].values())
            zoo_points = self.get_zoo_points()
            
            print(f"\n📊 Tổng số loài: {Colors.BOLD}{total_unique}{Colors.ENDC}")
            print(f"🎯 Tổng số con: {Colors.BOLD}{total_caught}{Colors.ENDC}")
            print(f"⭐ Điểm sở thú: {Colors.BOLD}{Colors.WARNING}{zoo_points}{Colors.ENDC}\n")
            
            for rarity, animals in ANIMALS.items():
                if not animals:
                    continue
                
                if not self.has_any_animal_in_rarity(rarity):
                    continue
                
                color = rarity_colors.get(rarity, Colors.ENDC)
                
                rarity_count = 0
                rarity_points = 0
                for animal in animals:
                    if animal["name"] in self.data["zoo"]:
                        count = self.data["zoo"][animal["name"]]
                        rarity_count += count
                        rarity_points += count * animal["points"]
                
                print(f"{color}{'─' * 70}{Colors.ENDC}")
                print(f"{color}{Colors.BOLD}✨ {rarity.upper()} (Điểm: {rarity_points} / Tổng số lượng: {rarity_count}){Colors.ENDC}")
                print(f"{color}{'─' * 70}{Colors.ENDC}")
                
                for animal in animals:
                    name = animal["name"]
                    emoji = animal["emoji"]
                    
                    if name in self.data["zoo"]:
                        count = self.data["zoo"][name]
                        print(f"  {emoji} {name.capitalize():<20} x{count}")
                    else:
                        print(f"  ❓ {'?':<20} x0 {Colors.GRAY}(Chưa bắt được){Colors.ENDC}")
                print()
            
            print(f"1. 💰 Bán động vật")
            print(f"2. 📊 Xem chỉ số động vật")
            print(f"0. Quay lại")
            
            choice = input(f"\n{Colors.OKCYAN}👉 Chọn: {Colors.ENDC}").strip()
            
            if choice == "1":
                self.sell_animal()
                self.show_zoo()
            elif choice == "2":
                self.view_animal_stats()
                self.show_zoo()
            elif choice == "0":
                return
            else:
                print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                time.sleep(1)
                self.show_zoo()
            
        except Exception as e:
            self.show_error("Lỗi khi hiển thị sở thú", e)
    
    def view_animal_stats(self):
        """Xem chỉ số động vật"""
        try:
            clear_screen()
            print(Colors.OKBLUE + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(Colors.OKBLUE + "║" + " " * 24 + "📊 CHỈ SỐ ĐỘNG VẬT" + " " * 25 + "║" + Colors.ENDC)
            print(Colors.OKBLUE + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            
            if not self.data["zoo"]:
                print(f"\n{Colors.FAIL}❌ Bạn chưa có động vật nào!{Colors.ENDC}")
                input(f"\n{Colors.GRAY}Nhấn Enter để quay lại...{Colors.ENDC}")
                return
            
            print(f"\n{Colors.BOLD}Chọn động vật để xem chỉ số:{Colors.ENDC}\n")
            
            animal_list = []
            index = 1
            for animal_name in self.data["zoo"].keys():
                animal_data = self.get_animal_data(animal_name)
                if animal_data:
                    print(f"{index}. {animal_data['emoji']} {animal_name.capitalize()}")
                    animal_list.append(animal_name)
                    index += 1
            
            print(f"\n0. Quay lại")
            
            choice = input(f"\n{Colors.OKCYAN}👉 Chọn số: {Colors.ENDC}").strip()
            
            if choice == "0":
                return
            
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(animal_list):
                    selected_animal = animal_list[choice_idx]
                    animal_data = self.get_animal_data(selected_animal)
                    
                    if animal_data:
                        clear_screen()
                        print(Colors.OKBLUE + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                        title = f"  📊 CHỈ SỐ: {selected_animal.upper()} {animal_data['emoji']}"
                        padding = 70 - len(title) - 2
                        print(Colors.OKBLUE + "║" + title + " " * padding + "║" + Colors.ENDC)
                        print(Colors.OKBLUE + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                        
                        stats = animal_data['stats']
                        print(f"\n{Colors.BOLD}Chỉ số cơ bản:{Colors.ENDC}")
                        print(f"  ❤️  HP (Health Points):        {stats['hp']}")
                        print(f"  ⚔️  ATK (Physical Attack):     {stats['atk']}")
                        print(f"  🛡️  PR (Physical Resistance):  {stats['pr']}")
                        print(f"  💎 WP (Weapon Points):         {stats['wp']}")
                        print(f"  ✨ MAG (Magical Attack):       {stats['mag']}")
                        print(f"  🌟 MR (Magical Resistance):    {stats['mr']}")
                        
                        input(f"\n{Colors.GRAY}Nhấn Enter để quay lại...{Colors.ENDC}")
                else:
                    print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                    time.sleep(1)
                    self.view_animal_stats()
            except ValueError:
                print(f"\n{Colors.FAIL}❌ Vui lòng nhập số hợp lệ!{Colors.ENDC}")
                time.sleep(1)
                self.view_animal_stats()
                
        except Exception as e:
            self.show_error("Lỗi khi xem chỉ số động vật", e)
    
    def sell_animal(self):
        """Bán động vật"""
        try:
            clear_screen()
            print(Colors.WARNING + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(Colors.WARNING + "║" + " " * 27 + "💰 BÁN ĐỘNG VẬT" + " " * 26 + "║" + Colors.ENDC)
            print(Colors.WARNING + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            
            if not self.data["zoo"]:
                print(f"\n{Colors.FAIL}❌ Bạn chưa có động vật nào để bán!{Colors.ENDC}")
                input(f"\n{Colors.GRAY}Nhấn Enter để quay lại...{Colors.ENDC}")
                return
            
            print(f"\n{Colors.BOLD}Động vật của bạn:{Colors.ENDC}\n")
            
            animal_list = []
            for animal_name, count in self.data["zoo"].items():
                emoji = "❓"
                sell_price = 1
                for rarity, animals in ANIMALS.items():
                    for animal in animals:
                        if animal["name"] == animal_name:
                            emoji = animal["emoji"]
                            sell_price = animal["sell_price"]
                            break
                
                print(f"  {emoji} {animal_name.capitalize():<15} x{count} (Giá: {sell_price} coin/con)")
                animal_list.append(animal_name)
            
            print(f"\n0. Quay lại")
            
            animal_name = input(f"\n{Colors.OKCYAN}👉 Nhập tên động vật muốn bán: {Colors.ENDC}").strip().lower()
            
            if animal_name == "0":
                return
            
            if animal_name not in self.data["zoo"]:
                print(f"\n{Colors.FAIL}❌ Bạn không có động vật này!{Colors.ENDC}")
                time.sleep(1.5)
                return
            
            max_count = self.data["zoo"][animal_name]
            
            try:
                count_str = input(f"{Colors.OKCYAN}👉 Nhập số lượng muốn bán (max: {max_count}): {Colors.ENDC}").strip()
                
                if count_str == "0":
                    return
                
                count = int(count_str)
                
                if count <= 0:
                    print(f"\n{Colors.FAIL}❌ Số lượng phải lớn hơn 0!{Colors.ENDC}")
                    time.sleep(1.5)
                    return
                
                if count > max_count:
                    print(f"\n{Colors.FAIL}❌ Bạn chỉ có {max_count} con!{Colors.ENDC}")
                    time.sleep(1.5)
                    return
                
                sell_price = 1
                for rarity, animals in ANIMALS.items():
                    for animal in animals:
                        if animal["name"] == animal_name:
                            sell_price = animal["sell_price"]
                            break
                
                total_coins = count * sell_price
                
                print(f"\n{Colors.WARNING}Bạn sẽ bán {count} {animal_name} và nhận {total_coins} coins.{Colors.ENDC}")
                confirm = input(f"{Colors.OKCYAN}Xác nhận? (y/n): {Colors.ENDC}").strip().lower()
                
                if confirm == "y":
                    loading_animation("Đang bán", 1)
                    
                    self.data["zoo"][animal_name] -= count
                    if self.data["zoo"][animal_name] == 0:
                        del self.data["zoo"][animal_name]
                    
                    self.data["coins"] += total_coins
                    
                    self.save_data()
                    
                    print(f"\n{Colors.OKGREEN}✅ Đã bán thành công!{Colors.ENDC}")
                    print(f"💰 +{total_coins} coins (Tổng: {self.data['coins']})")
                    time.sleep(2)
                else:
                    print(f"\n{Colors.GRAY}Đã hủy bán.{Colors.ENDC}")
                    time.sleep(1)
                    
            except ValueError:
                print(f"\n{Colors.FAIL}❌ Vui lòng nhập số hợp lệ!{Colors.ENDC}")
                time.sleep(1.5)
                return
                
        except Exception as e:
            self.show_error("Lỗi khi bán động vật", e)
    
    def show_stats(self):
        """Hiển thị thông tin người chơi"""
        try:
            clear_screen()
            print(Colors.OKCYAN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(Colors.OKCYAN + "║" + " " * 22 + "📊 THÔNG TIN NGƯỜI CHƠI" + " " * 23 + "║" + Colors.ENDC)
            print(Colors.OKCYAN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            
            exp_needed = self.get_exp_needed(self.data['level'])
            exp_percent = self.get_exp_percent()
            exp_bar_length = 30
            exp_bar_filled = int((self.data['exp'] / exp_needed) * exp_bar_length)
            exp_bar = "█" * exp_bar_filled + "░" * (exp_bar_length - exp_bar_filled)
            
            print(f"\n💰 Coins: {Colors.BOLD}{Colors.OKGREEN}{self.data['coins']}{Colors.ENDC}")
            print(f"⭐ Level: {Colors.BOLD}{self.data['level']}{Colors.ENDC} ({exp_percent:.1f}%)")
            print(f"✨ EXP: [{exp_bar}] {self.data['exp']:.2f}/{exp_needed}")
            print(f"🎒 Túi đồ: {len(self.data['inventory'])} vật phẩm")
            print(f"🔥 Daily Streak: {Colors.WARNING}{self.data['daily_streak']} ngày{Colors.ENDC}")
            
            print(f"\n{Colors.BOLD}📈 THỐNG KÊ:{Colors.ENDC}")
            print(f"  • Tổng coins kiếm được: {self.data['stats']['total_coins_earned']}")
            print(f"  • Số ngày chơi: {self.data['stats']['days_played']}")
            print(f"  • Trận thắng: {self.data['stats']['battles_won']}")
            print(f"  • Động vật đã bắt: {self.data['stats']['animals_caught']}")
            print(f"  • Tổng lần nhận daily: {self.data['total_daily_collected']}")
            
            input(f"\n{Colors.GRAY}Nhấn Enter để quay lại...{Colors.ENDC}")
            
        except Exception as e:
            self.show_error("Lỗi khi hiển thị thông tin", e)
    
    def shop(self):
        """Cửa hàng mua vật phẩm"""
        try:
            clear_screen()
            print(Colors.OKGREEN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(Colors.OKGREEN + "║" + " " * 29 + "🏪 CỬA HÀNG" + " " * 28 + "║" + Colors.ENDC)
            print(Colors.OKGREEN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            print(f"\n💰 Coins của bạn: {Colors.BOLD}{self.data['coins']}{Colors.ENDC}\n")
            
            items = {
                "1": {"name": "Kiếm sắt", "price": 500, "desc": "Vũ khí cơ bản", "emoji": "⚔️"},
                "2": {"name": "Áo giáp", "price": 800, "desc": "Tăng phòng thủ", "emoji": "🛡️"},
                "3": {"name": "Thuốc hồi máu", "price": 200, "desc": "Hồi 50 HP", "emoji": "💊"},
                "4": {"name": "Bùa may mắn", "price": 1500, "desc": "Tăng tỷ lệ critical", "emoji": "🍀"}
            }
            
            for key, item in items.items():
                print(f"{item['emoji']} {key}. {Colors.BOLD}{item['name']}{Colors.ENDC} - {Colors.WARNING}{item['price']} coins{Colors.ENDC}")
                print(f"   {Colors.GRAY}{item['desc']}{Colors.ENDC}")
            print(f"\n0. Quay lại")
            
            choice = input(f"\n{Colors.OKCYAN}👉 Chọn vật phẩm muốn mua: {Colors.ENDC}").strip()
            
            if choice in items:
                item = items[choice]
                if self.data["coins"] >= item["price"]:
                    loading_animation("Đang mua hàng", 1)
                    self.data["coins"] -= item["price"]
                    self.data["inventory"].append(item["name"])
                    self.save_data()
                    print(f"\n{Colors.OKGREEN}✅ Đã mua {item['name']}!{Colors.ENDC}")
                    time.sleep(1)
                else:
                    print(f"\n{Colors.FAIL}❌ Không đủ coins!{Colors.ENDC}")
                    time.sleep(1)
            elif choice == "0":
                return
            else:
                print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                time.sleep(1)
            
        except Exception as e:
            self.show_error("Lỗi trong cửa hàng", e)
    
    def battle(self):
        """Chiến đấu PvE với đội hình"""
        try:
            if not self.data["team"]:
                clear_screen()
                print_box("❌ Bạn phải thiết lập đội trước!\nVào mục 7. Thiết lập đội để thêm pet.", Colors.FAIL)
                input(f"\n{Colors.GRAY}Nhấn Enter để quay lại...{Colors.ENDC}")
                return
            
            clear_screen()
            print(Colors.FAIL + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(Colors.FAIL + "║" + " " * 26 + "⚔️  BẮT ĐẦU CHIẾN ĐẤU" + " " * 23 + "║" + Colors.ENDC)
            print(Colors.FAIL + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            
            loading_animation("Đang tìm đối thủ", 2)
            
            player_team = []
            for animal_name in self.data["team"]:
                animal_data = self.get_animal_data(animal_name)
                if animal_data:
                    stats = self.calculate_real_stats(animal_name, self.data['level'])
                    player_team.append({
                        "name": animal_name,
                        "emoji": animal_data['emoji'],
                        "hp": stats['hp'],
                        "max_hp": stats['hp'],
                        "atk": stats['atk'],
                        "mag": stats['mag'],
                        "level": self.data['level']
                    })
            
            total_player_level = len(player_team) * self.data['level']
            max_enemy_level = total_player_level + 3
            
            enemy_team = []
            enemy_total_level = 0
            enemy_count = random.randint(1, 3)
            
            for i in range(enemy_count):
                all_animals_list = []
                for rarity, animals in ANIMALS.items():
                    if animals:
                        all_animals_list.extend(animals)
                
                if all_animals_list:
                    enemy_animal = random.choice(all_animals_list)
                    remaining_slots = enemy_count - i
                    max_this_level = (max_enemy_level - enemy_total_level) // remaining_slots if remaining_slots > 0 else 1
                    enemy_level = random.randint(max(1, self.data['level'] - 2), max(1, max_this_level))
                    enemy_total_level += enemy_level
                    
                    stats = self.calculate_real_stats(enemy_animal['name'], enemy_level)
                    enemy_team.append({
                        "name": enemy_animal['name'],
                        "emoji": enemy_animal['emoji'],
                        "hp": stats['hp'],
                        "max_hp": stats['hp'],
                        "atk": stats['atk'],
                        "mag": stats['mag'],
                        "level": enemy_level
                    })
            
            clear_screen()
            print(Colors.OKGREEN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(Colors.OKGREEN + "║" + " " * 28 + "⚔️  ĐỘI CỦA BẠN" + " " * 25 + "║" + Colors.ENDC)
            print(Colors.OKGREEN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            for pet in player_team:
                print(f"  {pet['emoji']} {pet['name'].capitalize()} (Lv.{pet['level']}) - HP: {pet['hp']}/{pet['max_hp']}")
            
            print(f"\n{Colors.FAIL}{'─' * 70}{Colors.ENDC}")
            print(Colors.FAIL + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(Colors.FAIL + "║" + " " * 27 + "⚔️  ĐỘI ĐỐI THỦ" + " " * 26 + "║" + Colors.ENDC)
            print(Colors.FAIL + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            for pet in enemy_team:
                print(f"  {pet['emoji']} {pet['name'].capitalize()} (Lv.{pet['level']}) - HP: {pet['hp']}/{pet['max_hp']}")
            
            input(f"\n{Colors.WARNING}Nhấn Enter để bắt đầu...{Colors.ENDC}")
            
            turn = 0
            max_turns = 24
            
            while turn < max_turns:
                turn += 1
                clear_screen()
                print(Colors.WARNING + f"{'═' * 30} LƯỢT {turn}/{max_turns} {'═' * 30}" + Colors.ENDC)
                
                print(f"\n{Colors.OKGREEN}Đội bạn:{Colors.ENDC}")
                for pet in player_team:
                    if pet['hp'] > 0:
                        hp_percent = (pet['hp'] / pet['max_hp']) * 20
                        hp_bar = "█" * int(hp_percent) + "░" * (20 - int(hp_percent))
                        print(f"  {pet['emoji']} {pet['name']} [{Colors.OKGREEN}{hp_bar}{Colors.ENDC}] {pet['hp']}/{pet['max_hp']}")
                
                print(f"\n{Colors.FAIL}Đội địch:{Colors.ENDC}")
                for pet in enemy_team:
                    if pet['hp'] > 0:
                        hp_percent = (pet['hp'] / pet['max_hp']) * 20
                        hp_bar = "█" * int(hp_percent) + "░" * (20 - int(hp_percent))
                        print(f"  {pet['emoji']} {pet['name']} [{Colors.FAIL}{hp_bar}{Colors.ENDC}] {pet['hp']}/{pet['max_hp']}")
                
                alive_player = [p for p in player_team if p['hp'] > 0]
                alive_enemy = [p for p in enemy_team if p['hp'] > 0]
                
                if not alive_player or not alive_enemy:
                    break
                
                attacker = random.choice(alive_player)
                target = random.choice(alive_enemy)
                damage = random.randint(int(attacker['atk'] * 0.8), int(attacker['atk'] * 1.2))
                target['hp'] -= damage
                if target['hp'] < 0:
                    target['hp'] = 0
                
                print(f"\n⚔️  {attacker['emoji']} {attacker['name']} tấn công {target['emoji']} {target['name']}: {Colors.FAIL}-{damage} HP{Colors.ENDC}")
                time.sleep(0.8)
                
                alive_enemy = [p for p in enemy_team if p['hp'] > 0]
                if alive_enemy:
                    attacker = random.choice(alive_enemy)
                    target = random.choice([p for p in player_team if p['hp'] > 0])
                    damage = random.randint(int(attacker['atk'] * 0.8), int(attacker['atk'] * 1.2))
                    target['hp'] -= damage
                    if target['hp'] < 0:
                        target['hp'] = 0
                    
                    print(f"💥 {attacker['emoji']} {attacker['name']} phản công {target['emoji']} {target['name']}: {Colors.FAIL}-{damage} HP{Colors.ENDC}")
                    time.sleep(0.8)
                
                alive_player = [p for p in player_team if p['hp'] > 0]
                alive_enemy = [p for p in enemy_team if p['hp'] > 0]
                
                if not alive_player or not alive_enemy:
                    break
                
                input(f"\n{Colors.GRAY}Nhấn Enter cho lượt tiếp...{Colors.ENDC}")
            
            clear_screen()
            alive_player = [p for p in player_team if p['hp'] > 0]
            alive_enemy = [p for p in enemy_team if p['hp'] > 0]
            
            if not alive_enemy and alive_player:
                print(Colors.OKGREEN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                print(Colors.OKGREEN + "║" + " " * 28 + "🎉 CHIẾN THẮNG!" + " " * 27 + "║" + Colors.ENDC)
                print(Colors.OKGREEN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                
                reward_coins = random.randint(50, 150)
                reward_exp = random.randint(30, 80)
                
                self.data["coins"] += reward_coins
                self.data["exp"] += reward_exp
                self.data["stats"]["battles_won"] += 1
                self.data["stats"]["total_coins_earned"] += reward_coins
                
                level_up_count = 0
                exp_needed = self.get_exp_needed(self.data['level'])
                while self.data["exp"] >= exp_needed:
                    self.data["level"] += 1
                    self.data["exp"] -= exp_needed
                    level_up_count += 1
                    exp_needed = self.get_exp_needed(self.data['level'])
                
                print(f"\n💰 +{reward_coins} coins")
                print(f"⭐ +{reward_exp} EXP")
                
                if level_up_count > 0:
                    print(f"\n{Colors.WARNING}🎊 LEVEL UP x{level_up_count}! Bạn đạt Level {self.data['level']}!{Colors.ENDC}")
                
                self.save_data()
                
            elif not alive_player and alive_enemy:
                print(Colors.FAIL + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                print(Colors.FAIL + "║" + " " * 28 + "💀 BẠN ĐÃ THUA!" + " " * 28 + "║" + Colors.ENDC)
                print(Colors.FAIL + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                print(f"\n{Colors.GRAY}Hãy nâng cấp đội hình và thử lại!{Colors.ENDC}")
                
            else:
                print(Colors.WARNING + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                print(Colors.WARNING + "║" + " " * 30 + "🤝 HÒA!" + " " * 31 + "║" + Colors.ENDC)
                print(Colors.WARNING + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                print(f"\n{Colors.GRAY}Trận đấu hết {max_turns} lượt!{Colors.ENDC}")
            
            input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
            
        except Exception as e:
            self.show_error("Lỗi trong chiến đấu", e)
    
    def run(self):
        """Chạy game"""
        try:
            clear_screen()
            print_with_effect("=" * 70, 0.01, Colors.OKCYAN)
            print_with_effect("🎮 CHÀO MỪNG ĐÃ ĐẾN VỚI GAME PHIÊU LƯU!", 0.03, Colors.BOLD)
            print_with_effect("=" * 70, 0.01, Colors.OKCYAN)
            time.sleep(1)
            
            while True:
                try:
                    clear_screen()
                    exp_percent = self.get_exp_percent()
                    print(Colors.OKCYAN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                    print(Colors.OKCYAN + "║" + " " * 29 + "MENU CHÍNH" + " " * 29 + "║" + Colors.ENDC)
                    print(Colors.OKCYAN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                    
                    print(f"\n💰 Coins: {Colors.BOLD}{self.data['coins']}{Colors.ENDC} | ⭐ Level: {Colors.BOLD}{self.data['level']}{Colors.ENDC} ({exp_percent:.1f}%) | 🔥 Streak: {Colors.WARNING}{self.data['daily_streak']}{Colors.ENDC}")
                    print("\n1. 📊 Xem thông tin")
                    print("2. 🏪 Cửa hàng")
                    print("3. ⚔️  Chiến đấu")
                    print("4. 🎁 Nhận daily")
                    print("5. 🎣 Săn bắt")
                    print("6. 🦁 Sở thú")
                    print("7. ⚔️  Thiết lập đội")
                    print("0. 🚪 Thoát game")
                    
                    choice = input(f"\n{Colors.OKCYAN}👉 Nhập lựa chọn: {Colors.ENDC}").strip().lower()
                    
                    if choice == "1":
                        self.show_stats()
                    elif choice == "2":
                        self.shop()
                    elif choice == "3":
                        self.battle()
                    elif choice in ["4", "odaily", "owo daily", "daily"]:
                        self.check_daily_reward()
                    elif choice in ["5", "oh", "owo hunt", "hunt"]:
                        self.hunt_animal()
                    elif choice in ["6", "ozoo", "owo zoo", "zoo"]:
                        self.show_zoo()
                    elif choice == "7":
                        self.manage_team()
                    elif choice == "0":
                        clear_screen()
                        print_with_effect("👋 Tạm biệt! Hẹn gặp lại!", 0.03, Colors.OKGREEN)
                        self.save_data()
                        time.sleep(1)
                        break
                    else:
                        print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                        time.sleep(1)
                except Exception as e:
                    self.show_error("Lỗi trong menu", e)
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            clear_screen()
            print(f"\n{Colors.WARNING}⚠️  Game bị gián đoạn!{Colors.ENDC}")
            self.save_data()
            sys.exit(0)
        except Exception as e:
            self.show_error("Lỗi nghiêm trọng trong game", e)
            time.sleep(2)

if __name__ == "__main__":
    try:
        check_requirements()
        clear_screen()
        
        game = Game()
        game.run()
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Lỗi khởi động game:{Colors.ENDC}")
        print(f"{type(e).__name__}: {str(e)}")
        traceback.print_exc()
        sys.exit(1),
            "daily_streak": 0,
            "total_daily_collected": 0,
            "inventory": [],
            "zoo": {},
            "team": [],
            "stats": {
                "total_coins_earned": 0,
                "days_played": 0,
                "battles_won": 0,
                "animals_caught": 0
            }
        }
    
    def save_data(self, silent=False):
        """Lưu dữ liệu vào file"""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            if not silent:
                print(f"{Colors.OKGREEN}💾 Dữ liệu đã được lưu!{Colors.ENDC}")
        except Exception as e:
            self.show_error("Lỗi khi lưu dữ liệu", e)
    
    def auto_save(self):
        """Tự động lưu im lặng"""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except:
            pass
    
    def get_daily_rewards(self, streak):
        """Tính toán phần thưởng dựa trên streak"""
        if 1 <= streak <= 20:
            coins = random.randint(100, 500)
            exp = random.uniform(1, 5)
        elif 21 <= streak <= 60:
            coins = random.randint(450, 1200)
            exp = random.uniform(4.5, 10)
        elif 61 <= streak <= 74:
            coins = random.randint(1150, 2500)
            exp = random.uniform(9.85, 19)
        else:
            coins = random.randint(2450, 3500)
            exp = random.uniform(20, 29.5)
        
        return coins, round(exp, 2)
    
    def check_daily_reward(self):
        """Kiểm tra và nhận phần thưởng hàng ngày"""
        try:
            now = datetime.now()
            last_daily = self.data.get("last_daily")
            
            if last_daily:
                last_time = datetime.fromisoformat(last_daily)
                time_diff = now - last_time
                
                if time_diff < timedelta(hours=24):
                    remaining = timedelta(hours=24) - time_diff
                    hours = remaining.seconds // 3600
                    minutes = (remaining.seconds % 3600) // 60
                    
                    clear_screen()
                    msg = f"⏰ Bạn đã nhận daily rồi!\n⏳ Quay lại sau {hours} giờ {minutes} phút"
                    print_box(msg, Colors.WARNING)
                    input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
                    return False
                
                if time_diff > timedelta(hours=48):
                    self.data["daily_streak"] = 0
                    self.auto_save()
            
            loading_animation("Đang xử lý daily reward", 1)
            
            self.data["daily_streak"] += 1
            streak = self.data["daily_streak"]
            
            coins, exp = self.get_daily_rewards(streak)
            
            self.data["coins"] += coins
            self.data["exp"] += exp
            self.data["stats"]["total_coins_earned"] += coins
            self.data["stats"]["days_played"] += 1
            self.data["total_daily_collected"] += 1
            self.data["last_daily"] = now.isoformat()
            
            self.auto_save()
            
            level_up_count = 0
            exp_needed = self.get_exp_needed(self.data['level'])
            while self.data["exp"] >= exp_needed:
                self.data["level"] += 1
                self.data["exp"] -= exp_needed
                level_up_count += 1
                exp_needed = self.get_exp_needed(self.data['level'])
                self.auto_save()
            
            self.save_data()
            
            clear_screen()
            print(Colors.OKGREEN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(Colors.OKGREEN + "║" + " " * 20 + "🎁 PHẦN THƯỞNG HÀNG NGÀY 🎁" + " " * 21 + "║" + Colors.ENDC)
            print(Colors.OKGREEN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            
            print(f"\n{Colors.BOLD}✨ Phần thưởng nhận được:{Colors.ENDC}")
            print(f"   💰 Coins: {Colors.OKGREEN}+{coins}{Colors.ENDC}")
            print(f"   ⭐ EXP: {Colors.OKCYAN}+{exp}{Colors.ENDC}")
            print(f"\n{Colors.BOLD}📊 Thông tin streak:{Colors.ENDC}")
            print(f"   🔥 Streak hiện tại: {Colors.WARNING}{streak} ngày{Colors.ENDC}")
            print(f"   📅 Tổng số lần nhận: {self.data['total_daily_collected']}")
            print(f"   🎯 Lần nhận tiếp theo: Ngày thứ {streak + 1}")
            
            exp_percent = self.get_exp_percent()
            exp_needed = self.get_exp_needed(self.data['level'])
            print(f"\n{Colors.BOLD}💼 Trạng thái tài khoản:{Colors.ENDC}")
            print(f"   💰 Tổng coins: {Colors.BOLD}{self.data['coins']}{Colors.ENDC}")
            print(f"   ⭐ Level: {Colors.BOLD}{self.data['level']}{Colors.ENDC} ({exp_percent:.1f}%)")
            print(f"   ✨ EXP: {Colors.BOLD}{self.data['exp']:.2f}/{exp_needed}{Colors.ENDC}")
            
            if level_up_count > 0:
                print(f"\n{Colors.WARNING}🎊 LEVEL UP x{level_up_count}! Bạn đạt Level {self.data['level']}!{Colors.ENDC}")
            
            input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
            return True
            
        except Exception as e:
            self.show_error("Lỗi khi nhận daily reward", e)
            return False
    
    def hunt_animal(self):
        """Săn bắt động vật"""
        try:
            if self.data["coins"] < 5:
                clear_screen()
                print_box("❌ Không đủ 5 coins để săn bắt!", Colors.FAIL)
                input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
                return
            
            self.data["coins"] -= 5
            self.auto_save()
            
            loading_animation("Đang săn bắt", 1.5)
            
            all_animals = []
            for rarity, animals in ANIMALS.items():
                for animal in animals:
                    all_animals.extend([animal] * int(animal["chance"] * 100))
            
            if not all_animals:
                print(f"\n{Colors.FAIL}Không có động vật nào để săn!{Colors.ENDC}")
                time.sleep(1)
                return
            
            caught_animal = random.choice(all_animals)
            animal_name = caught_animal["name"]
            animal_emoji = caught_animal["emoji"]
            animal_exp = caught_animal["exp"]
            
            rarity = "Common"
            for r, animals in ANIMALS.items():
                if any(a["name"] == animal_name for a in animals):
                    rarity = r
                    break
            
            if animal_name in self.data["zoo"]:
                self.data["zoo"][animal_name] += 1
            else:
                self.data["zoo"][animal_name] = 1
            
            # CỘNG EXP VÀO NGƯỜI CHƠI
            self.data["exp"] += animal_exp
            self.data["stats"]["animals_caught"] += 1
            
            self.auto_save()
            
            level_up_count = 0
            exp_needed = self.get_exp_needed(self.data['level'])
            while self.data["exp"] >= exp_needed:
                self.data["level"] += 1
                self.data["exp"] -= exp_needed
                level_up_count += 1
                exp_needed = self.get_exp_needed(self.data['level'])
                self.auto_save()
            
            self.save_data()
            
            clear_screen()
            rarity_colors = {
                "Common": Colors.GRAY,
                "Uncommon": Colors.OKGREEN,
                "Rare": Colors.OKBLUE,
                "Epic": Colors.HEADER,
                "Mythical": Colors.HEADER,
                "Legendary": Colors.WARNING
            }
            color = rarity_colors.get(rarity, Colors.ENDC)
            
            print(color + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(color + "║" + " " * 24 + "🎣 SĂN BẮT THÀNH CÔNG!" + " " * 23 + "║" + Colors.ENDC)
            print(color + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            
            print(f"\n{animal_emoji} Bạn đã bắt được: {Colors.BOLD}{animal_name.upper()}{Colors.ENDC}")
            print(f"✨ Độ hiếm: {color}{rarity}{Colors.ENDC}")
            print(f"⭐ EXP nhận được: {Colors.BOLD}{Colors.OKCYAN}+{animal_exp} EXP{Colors.ENDC}")
            print(f"📈 EXP hiện tại: {Colors.BOLD}{self.data['exp']:.2f}/{self.get_exp_needed(self.data['level'])}{Colors.ENDC}")
            print(f"📊 Số lượng hiện có: {Colors.BOLD}{self.data['zoo'][animal_name]}{Colors.ENDC}")
            print(f"💰 Coins còn lại: {self.data['coins']}")
            
            if level_up_count > 0:
                print(f"\n{Colors.WARNING}🎊 LEVEL UP x{level_up_count}! Bạn đạt Level {self.data['level']}!{Colors.ENDC}")
            
            input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
            
        except Exception as e:
            self.show_error("Lỗi khi săn bắt động vật", e)
    
    def get_animal_data(self, animal_name):
        """Lấy thông tin động vật từ tên"""
        for rarity, animals in ANIMALS.items():
            for animal in animals:
                if animal["name"] == animal_name:
                    return animal
        return None
    
    def calculate_real_stats(self, animal_name, level):
        """Tính chỉ số thực tế của động vật dựa trên level"""
        animal_data = self.get_animal_data(animal_name)
        if not animal_data:
            return None
        
        stats = animal_data['stats']
        
        real_hp = 2 * stats['hp'] * level + 500
        real_atk = stats['atk'] * level + 100
        real_pr = 0.8 * ((25 + 2 * level * stats['pr']) / (125 + 2 * level * stats['pr'])) * 100
        real_wp = 2 * stats['wp'] * level + 500
        real_mag = stats['mag'] * level + 100
        real_mr = 0.8 * ((25 + 2 * level * stats['mr']) / (125 + 2 * level * stats['mr'])) * 100
        
        return {
            "hp": int(real_hp),
            "atk": int(real_atk),
            "pr": round(real_pr, 2),
            "wp": int(real_wp),
            "mag": int(real_mag),
            "mr": round(real_mr, 2)
        }
    
    def manage_team(self):
        """Quản lý đội hình"""
        try:
            while True:
                clear_screen()
                print(Colors.WARNING + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                print(Colors.WARNING + "║" + " " * 26 + "⚔️  THIẾT LẬP ĐỘI" + " " * 25 + "║" + Colors.ENDC)
                print(Colors.WARNING + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                
                print(f"\n{Colors.BOLD}Đội hình hiện tại (Tối đa 3 pet):{Colors.ENDC}\n")
                
                if not self.data["team"]:
                    print(f"  {Colors.GRAY}(Chưa có pet nào trong đội){Colors.ENDC}")
                else:
                    for idx, animal_name in enumerate(self.data["team"], 1):
                        animal_data = self.get_animal_data(animal_name)
                        if animal_data:
                            real_stats = self.calculate_real_stats(animal_name, self.data['level'])
                            print(f"
