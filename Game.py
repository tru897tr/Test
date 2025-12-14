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

# Yêu cầu EXP để level up theo độ hiếm
RARITY_EXP_REQUIREMENTS = {
    "Common": 50,        # Common cần 50 exp mỗi level
    "Uncommon": 75,      # Uncommon cần 75 exp mỗi level
    "Rare": 100,         # Rare cần 100 exp mỗi level
    "Epic": 150,
    "Mythical": 200,
    "Patreon": 250,
    "Custom Patreon": 300,
    "Legendary": 350,
    "Gem": 400,
    "Bot Distorted": 450,
    "Fabled": 500,
    "Special": 550,
    "Hidden": 600
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
    except Exception:
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
    except Exception:
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

def show_rarity_table():
    """Hiển thị bảng phân loại độ hiếm"""
    print(f"\n{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BOLD}║                    📊 BẢNG PHÂN LOẠI ĐỘ HIẾM                    ║{Colors.ENDC}")
    print(f"{Colors.BOLD}╠══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
    print(f"{Colors.BOLD}║  Độ hiếm       │  Icon │  EXP/Lv  │  Số loài  │  Màu sắc       ║{Colors.ENDC}")
    print(f"{Colors.BOLD}╠══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
    
    rarity_info = {
        "Common": {"color": Colors.GRAY, "exp_req": 50, "icon": "⚪", "display": "Phổ thông"},
        "Uncommon": {"color": Colors.OKGREEN, "exp_req": 75, "icon": "🟢", "display": "Khá hiếm"},
        "Rare": {"color": Colors.OKBLUE, "exp_req": 100, "icon": "🔵", "display": "Hiếm"},
        "Epic": {"color": Colors.HEADER, "exp_req": 150, "icon": "🟣", "display": "Sử thi"},
        "Mythical": {"color": Colors.WARNING, "exp_req": 200, "icon": "🟠", "display": "Thần t化"},
        "Legendary": {"color": Colors.FAIL, "exp_req": 350, "icon": "🔴", "display": "Huyền thoại"}
    }
    
    for rarity, info in rarity_info.items():
        animals_in_rarity = ANIMALS.get(rarity, [])
        count = len(animals_in_rarity)
        color = info["color"]
        icon = info["icon"]
        exp_req = info["exp_req"]
        display = info["display"]
        
        print(f"{Colors.BOLD}║{Colors.ENDC}  {color}{rarity:<13}{Colors.ENDC} │   {icon}   │  {Colors.BOLD}{exp_req:>6}{Colors.ENDC}  │    {Colors.BOLD}{count:>2}{Colors.ENDC}     │  {color}{'█' * 10}{Colors.ENDC}  {Colors.BOLD}║{Colors.ENDC}")
    
    print(f"{Colors.BOLD}╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")

class Game:
    def __init__(self):
        try:
            self.data = self.load_data()
        except Exception as e:
            self.show_error("Lỗi khởi tạo game", e)
            sys.exit(1)
    
    def get_exp_needed(self, level):
        """Tính EXP cần thiết cho level tiếp theo"""
        return 100 + (level - 1) * 20  # Mỗi level cần thêm 20 EXP
    
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
                    # Đảm bảo có đầy đủ các trường
                    if "zoo" not in data:
                        data["zoo"] = {}
                    if "team" not in data:
                        data["team"] = []
                    if "pet_data" not in data:
                        data["pet_data"] = {}
                    if "stats" not in data:
                        data["stats"] = {}
                    if "animals_caught" not in data["stats"]:
                        data["stats"]["animals_caught"] = 0
                    if "daily_streak" not in data:
                        data["daily_streak"] = 0
                    if "total_daily_collected" not in data:
                        data["total_daily_collected"] = 0
                    if "inventory" not in data:
                        data["inventory"] = []
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
            "last_daily": None,
            "daily_streak": 0,
            "total_daily_collected": 0,
            "inventory": [],
            "zoo": {},
            "pet_data": {},  # Lưu level và exp của từng pet: {"bee": {"level": 1, "exp": 0}, ...}
            "team": [],  # Đội hình tối đa 3 pet
            "stats": {
                "total_coins_earned": 0,
                "days_played": 0,
                "battles_won": 0,
                "animals_caught": 0
            }
        }
    
    def save_data(self, silent=False):
        """Lưu dữ liệu vào file - tự động lưu ngay lập tức"""
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
        except Exception:
            pass
    
    def get_daily_rewards(self, streak):
        """Tính toán phần thưởng dựa trên streak"""
        if 1 <= streak <= 20:
            coins = random.randint(100, 500)
            exp = random.randint(1, 5)
        elif 21 <= streak <= 60:
            coins = random.randint(450, 1200)
            exp = random.randint(5, 10)
        elif 61 <= streak <= 74:
            coins = random.randint(1150, 2500)
            exp = random.randint(10, 19)
        else:  # 75+
            coins = random.randint(2450, 3500)
            exp = random.randint(20, 30)
        
        return coins, exp
    
    def check_daily_reward(self):
        """Kiểm tra và nhận phần thưởng hàng ngày"""
        try:
            now = datetime.now()
            last_daily = self.data.get("last_daily")
            
            if last_daily:
                last_time = datetime.fromisoformat(last_daily)
                time_diff = now - last_time
                
                # Nếu chưa đủ 24 giờ
                if time_diff < timedelta(hours=24):
                    remaining = timedelta(hours=24) - time_diff
                    hours = remaining.seconds // 3600
                    minutes = (remaining.seconds % 3600) // 60
                    
                    clear_screen()
                    msg = f"⏰ Bạn đã nhận daily rồi!\n⏳ Quay lại sau {hours} giờ {minutes} phút"
                    print_box(msg, Colors.WARNING)
                    input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
                    return False
                
                # Nếu quá 48 giờ thì reset streak
                if time_diff > timedelta(hours=48):
                    self.data["daily_streak"] = 0
                    self.auto_save()
            
            loading_animation("Đang xử lý daily reward", 1)
            
            # Tăng streak
            self.data["daily_streak"] += 1
            streak = self.data["daily_streak"]
            
            # Tính phần thưởng
            coins, exp = self.get_daily_rewards(streak)
            
            # Cập nhật dữ liệu
            self.data["coins"] += coins
            self.data["exp"] += exp
            self.data["stats"]["total_coins_earned"] += coins
            self.data["stats"]["days_played"] += 1
            self.data["total_daily_collected"] += 1
            self.data["last_daily"] = now.isoformat()
            
            # Lưu ngay lập tức
            self.auto_save()
            
            # Check level up
            level_up_count = 0
            exp_needed = self.get_exp_needed(self.data['level'])
            while self.data["exp"] >= exp_needed:
                self.data["level"] += 1
                self.data["exp"] -= exp_needed
                level_up_count += 1
                exp_needed = self.get_exp_needed(self.data['level'])
                # Lưu ngay khi level up
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
            print(f"   ✨ EXP: {Colors.BOLD}{self.data['exp']}/{exp_needed}{Colors.ENDC}")
            
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
            # Lưu ngay sau khi trừ coins
            self.auto_save()
            
            loading_animation("Đang săn bắt", 1.5)
            
            # Chọn động vật ngẫu nhiên
            all_animals = []
            for rarity, animals in ANIMALS.items():
                for animal in animals:
                    all_animals.extend([animal] * int(animal["chance"] * 10))
            
            caught_animal = random.choice(all_animals)
            animal_name = caught_animal["name"]
            animal_emoji = caught_animal["emoji"]
            
            # Tìm rarity
            rarity = "Common"
            for r, animals in ANIMALS.items():
                if any(a["name"] == animal_name for a in animals):
                    rarity = r
                    break
            
            # Cập nhật zoo
            if animal_name in self.data["zoo"]:
                self.data["zoo"][animal_name] += 1
            else:
                self.data["zoo"][animal_name] = 1
                # Khởi tạo pet_data cho pet mới
                if animal_name not in self.data["pet_data"]:
                    self.data["pet_data"][animal_name] = {"level": 1, "exp": 0}
            
            self.data["stats"]["animals_caught"] += 1
            
            # Thêm EXP cho người chơi khi săn bắt
            hunt_exp = random.randint(5, 15)
            self.data["exp"] += hunt_exp
            
            # Check level up người chơi
            player_level_up = 0
            exp_needed = self.get_exp_needed(self.data['level'])
            while self.data["exp"] >= exp_needed:
                self.data["level"] += 1
                self.data["exp"] -= exp_needed
                player_level_up += 1
                exp_needed = self.get_exp_needed(self.data['level'])
            
            # Lưu ngay sau khi bắt được
            self.save_data()
            
            clear_screen()
            rarity_colors = {
                "Common": Colors.GRAY,
                "Uncommon": Colors.OKGREEN,
                "Rare": Colors.OKBLUE
            }
            color = rarity_colors.get(rarity, Colors.ENDC)
            
            print(color + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(color + "║" + " " * 22 + "🎣 SĂN BẮT THÀNH CÔNG! 🎣" + " " * 21 + "║" + Colors.ENDC)
            print(color + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            
            print(f"\n{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}║  THÔNG TIN ĐỘNG VẬT                                              ║{Colors.ENDC}")
            print(f"{Colors.BOLD}╠══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  {animal_emoji}  Tên:           {Colors.BOLD}{animal_name.upper():<40}{Colors.ENDC}      {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  ✨ Độ hiếm:      {color}{rarity:<40}{Colors.ENDC}      {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  📊 Số lượng:     {Colors.BOLD}{self.data['zoo'][animal_name]} con{Colors.ENDC} trong sở thú                          {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}╠══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
            print(f"{Colors.BOLD}║  PHẦN THƯỞNG                                                      ║{Colors.ENDC}")
            print(f"{Colors.BOLD}╠══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  ⭐ EXP người chơi:  {Colors.OKCYAN}+{hunt_exp}{Colors.ENDC}                                          {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  💰 Coins còn lại:   {Colors.OKGREEN}{self.data['coins']}{Colors.ENDC}                                          {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
            
            if player_level_up > 0:
                print(f"\n{Colors.WARNING}{'🎊 ' * 35}{Colors.ENDC}")
                print(f"{Colors.WARNING}{Colors.BOLD}   LEVEL UP x{player_level_up}! BẠN ĐẠT LEVEL {self.data['level']}!{Colors.ENDC}")
                print(f"{Colors.WARNING}{'🎊 ' * 35}{Colors.ENDC}")
            
            input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
            
        except Exception as e:
            self.show_error("Lỗi khi săn bắt động vật", e)
    
    def get_zoo_points(self):
        """Tính điểm sở thú theo độ hiếm"""
        total_points = 0
        for animal_name, count in self.data["zoo"].items():
            # Tìm động vật và lấy điểm
            for rarity, animals in ANIMALS.items():
                for animal in animals:
                    if animal["name"] == animal_name:
                        total_points += count * animal["points"]
                        break
        return total_points
    
    def has_any_animal_in_rarity(self, rarity):
        """Kiểm tra xem người chơi có động vật nào trong độ hiếm này không"""
        animals = ANIMALS.get(rarity, [])
        for animal in animals:
            if animal["name"] in self.data["zoo"]:
                return True
        return False
    
    def get_animal_data(self, animal_name):
        """Lấy thông tin động vật từ tên"""
        for rarity, animals in ANIMALS.items():
            for animal in animals:
                if animal["name"] == animal_name:
                    return animal
        return None
    
    def get_animal_rarity(self, animal_name):
        """Lấy độ hiếm của động vật"""
        for rarity, animals in ANIMALS.items():
            for animal in animals:
                if animal["name"] == animal_name:
                    return rarity
        return "Common"
    
    def get_pet_level(self, animal_name):
        """Lấy level của pet"""
        if animal_name not in self.data["pet_data"]:
            self.data["pet_data"][animal_name] = {"level": 1, "exp": 0}
            self.auto_save()
        return self.data["pet_data"][animal_name]["level"]
    
    def get_pet_exp(self, animal_name):
        """Lấy EXP của pet"""
        if animal_name not in self.data["pet_data"]:
            self.data["pet_data"][animal_name] = {"level": 1, "exp": 0}
            self.auto_save()
        return self.data["pet_data"][animal_name]["exp"]
    
    def get_pet_exp_needed(self, animal_name):
        """Tính EXP cần để pet lên level"""
        rarity = self.get_animal_rarity(animal_name)
        return RARITY_EXP_REQUIREMENTS.get(rarity, 50)
    
    def add_pet_exp(self, animal_name, exp_amount):
        """Thêm EXP cho pet và check level up"""
        if animal_name not in self.data["pet_data"]:
            self.data["pet_data"][animal_name] = {"level": 1, "exp": 0}
        
        self.data["pet_data"][animal_name]["exp"] += exp_amount
        
        # Check level up
        level_up_count = 0
        exp_needed = self.get_pet_exp_needed(animal_name)
        
        while self.data["pet_data"][animal_name]["exp"] >= exp_needed:
            self.data["pet_data"][animal_name]["level"] += 1
            self.data["pet_data"][animal_name]["exp"] -= exp_needed
            level_up_count += 1
            exp_needed = self.get_pet_exp_needed(animal_name)
        
        self.auto_save()
        return level_up_count
    
    def calculate_real_stats(self, animal_name, level):
        """Tính toán stats thực tế dựa trên level với công thức chính xác"""
        animal_data = self.get_animal_data(animal_name)
        if not animal_data:
            return {
                "hp": 500,
                "atk": 100,
                "pr": 0,
                "pr_percent": 0,
                "wp": 500,
                "mag": 100,
                "mr": 0,
                "mr_percent": 0
            }
        
        base_stats = animal_data["stats"]
        
        # HP: 2 * "hp stat" * "level" + 500
        hp = 2 * base_stats["hp"] * level + 500
        
        # ATK (STR): "str stat" * "level" + 100
        atk = base_stats["atk"] * level + 100
        
        # PR Percentage: 0.8 x ((25 + 2 * "level" * "PR stat") / (125 + 2 * "level" * "PR stat"))
        pr_stat = base_stats["pr"]
        pr_numerator = 25 + 2 * level * pr_stat
        pr_denominator = 125 + 2 * level * pr_stat
        pr_percent = 0.8 * (pr_numerator / pr_denominator) if pr_denominator != 0 else 0
        
        # WP (Mana): 2 * "wp stat" * "level" + 500
        wp = 2 * base_stats["wp"] * level + 500
        
        # MAG: "mag stat" * "level" + 100
        mag = base_stats["mag"] * level + 100
        
        # MR Percentage: 0.8 x ((25 + 2 * "level" * "MR stat") / (125 + 2 * "level" * "MR stat"))
        mr_stat = base_stats["mr"]
        mr_numerator = 25 + 2 * level * mr_stat
        mr_denominator = 125 + 2 * level * mr_stat
        mr_percent = 0.8 * (mr_numerator / mr_denominator) if mr_denominator != 0 else 0
        
        return {
            "hp": int(hp),
            "atk": int(atk),
            "pr": pr_stat,
            "pr_percent": pr_percent * 100,  # Chuyển sang %
            "wp": int(wp),
            "mag": int(mag),
            "mr": mr_stat,
            "mr_percent": mr_percent * 100  # Chuyển sang %
        }
    
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
                "Rare": Colors.OKBLUE,
                "Epic": Colors.HEADER,
                "Mythical": Colors.HEADER,
                "Patreon": Colors.WARNING,
                "Custom Patreon": Colors.WARNING,
                "Legendary": Colors.WARNING,
                "Gem": Colors.OKCYAN,
                "Bot Distorted": Colors.FAIL,
                "Fabled": Colors.HEADER,
                "Special": Colors.WARNING,
                "Hidden": Colors.GRAY
            }
            
            total_unique = len(self.data["zoo"])
            total_caught = sum(self.data["zoo"].values())
            zoo_points = self.get_zoo_points()
            
            print(f"\n📊 Tổng số loài: {Colors.BOLD}{total_unique}{Colors.ENDC}")
            print(f"🎯 Tổng số con: {Colors.BOLD}{total_caught}{Colors.ENDC}")
            print(f"⭐ Điểm sở thú: {Colors.BOLD}{Colors.WARNING}{zoo_points}{Colors.ENDC}\n")
            
            for rarity, animals in ANIMALS.items():
                # Bỏ qua độ hiếm rỗng hoặc chưa có động vật nào
                if not animals:
                    continue
                
                # Kiểm tra xem người chơi có động vật nào trong độ hiếm này không
                if not self.has_any_animal_in_rarity(rarity):
                    continue
                
                color = rarity_colors.get(rarity, Colors.ENDC)
                
                # Đếm số con và điểm ở độ hiếm này
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
                self.show_zoo()  # Quay lại sở thú sau khi bán
            elif choice == "2":
                self.view_animal_stats()
                self.show_zoo()  # Quay lại sở thú
            elif choice == "0":
                return
            else:
                print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                time.sleep(1)
                self.show_zoo()  # Quay lại sở thú
            
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
                        print(Colors.OKBLUE + "║" + f"  📊 CHỈ SỐ: {selected_animal.upper()} {animal_data['emoji']}" + " " * (56 - len(selected_animal)) + "║" + Colors.ENDC)
                        print(Colors.OKBLUE + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                        
                        # Chỉ hiển thị stats base
                        stats = animal_data['stats']
                        print(f"\n{Colors.BOLD}Chỉ số cơ bản:{Colors.ENDC}")
                        print(f"  ❤️  HP (Health Points):        {stats['hp']}")
                        print(f"  ⚔️  ATK (Physical Attack):     {stats['atk']}")
                        print(f"  🛡️  PR (Physical Resistance):  {stats['pr']}")
                        print(f"  💎 WP (Weapon Points):         {stats['wp']}")
                        print(f"  ✨ MAG (Magical Attack):       {stats['mag']}")
                        print(f"  🌟 MR (Magical Resistance):    {stats['mr']}")
                        
                        print(f"\n{Colors.GRAY}💡 Ghi chú: Đây là chỉ số cơ bản (base stats)")
                        print(f"Stats thực tế sẽ được tính dựa trên level trong chiến đấu.{Colors.ENDC}")
                        
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
            
            # Hiển thị bảng độ hiếm
            show_rarity_table()
            
            if not self.data["zoo"]:
                print(f"\n{Colors.FAIL}❌ Bạn chưa có động vật nào để bán!{Colors.ENDC}")
                input(f"\n{Colors.GRAY}Nhấn Enter để quay lại...{Colors.ENDC}")
                return
            
            print(f"\n{Colors.BOLD}Động vật của bạn:{Colors.ENDC}\n")
            
            # Hiển thị động vật có thể bán theo độ hiếm
            animal_list = []
            for rarity in ["Common", "Uncommon", "Rare", "Epic", "Mythical", "Legendary"]:
                animals_in_rarity = []
                for animal_name, count in self.data["zoo"].items():
                    if self.get_animal_rarity(animal_name) == rarity:
                        animals_in_rarity.append((animal_name, count))
                
                if animals_in_rarity:
                    rarity_colors = {
                        "Common": Colors.GRAY,
                        "Uncommon": Colors.OKGREEN,
                        "Rare": Colors.OKBLUE,
                        "Epic": Colors.HEADER,
                        "Mythical": Colors.WARNING,
                        "Legendary": Colors.FAIL
                    }
                    color = rarity_colors.get(rarity, Colors.ENDC)
                    print(f"{color}【{rarity}】{Colors.ENDC}")
                    
                    for animal_name, count in animals_in_rarity:
                        emoji = "❓"
                        sell_price = 1
                        pet_level = self.get_pet_level(animal_name)
                        
                        for r, animals in ANIMALS.items():
                            for animal in animals:
                                if animal["name"] == animal_name:
                                    emoji = animal["emoji"]
                                    sell_price = animal["sell_price"]
                                    break
                        
                        print(f"  {emoji} {animal_name.capitalize():<15} x{count} (Lv.{pet_level}) | Giá: {sell_price} coin/con")
                        animal_list.append(animal_name)
                    print()
            
            print(f"0. Quay lại")
            
            animal_name = input(f"\n{Colors.OKCYAN}👉 Nhập tên động vật muốn bán: {Colors.ENDC}").strip().lower()
            
            if animal_name == "0":
                return
            
            # Kiểm tra động vật có tồn tại
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
                
                # Tìm giá bán
                sell_price = 1
                for rarity, animals in ANIMALS.items():
                    for animal in animals:
                        if animal["name"] == animal_name:
                            sell_price = animal["sell_price"]
                            break
                
                total_coins = count * sell_price
                
                # Xác nhận
                print(f"\n{Colors.WARNING}Bạn sẽ bán {count} {animal_name} và nhận {total_coins} coins.{Colors.ENDC}")
                confirm = input(f"{Colors.OKCYAN}Xác nhận? (y/n): {Colors.ENDC}").strip().lower()
                
                if confirm == "y":
                    loading_animation("Đang bán", 1)
                    
                    # Cập nhật dữ liệu
                    self.data["zoo"][animal_name] -= count
                    if self.data["zoo"][animal_name] == 0:
                        del self.data["zoo"][animal_name]
                    
                    self.data["coins"] += total_coins
                    self.data["stats"]["total_coins_earned"] += total_coins
                    
                    # Lưu ngay
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
    
    def manage_team(self):
        """Quản lý đội hình"""
        try:
            while True:
                clear_screen()
                print(Colors.HEADER + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                print(Colors.HEADER + "║" + " " * 26 + "⚔️  THIẾT LẬP ĐỘI" + " " * 25 + "║" + Colors.ENDC)
                print(Colors.HEADER + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                
                # Hiển thị bảng độ hiếm
                show_rarity_table()
                
                print(f"\n{Colors.BOLD}Đội hình hiện tại ({len(self.data['team'])}/3):{Colors.ENDC}\n")
                
                if self.data["team"]:
                    for i, animal_name in enumerate(self.data["team"], 1):
                        animal_data = self.get_animal_data(animal_name)
                        if animal_data:
                            pet_level = self.get_pet_level(animal_name)
                            pet_exp = self.get_pet_exp(animal_name)
                            exp_needed = self.get_pet_exp_needed(animal_name)
                            stats = self.calculate_real_stats(animal_name, pet_level)
                            rarity = self.get_animal_rarity(animal_name)
                            
                            rarity_colors = {
                                "Common": Colors.GRAY,
                                "Uncommon": Colors.OKGREEN,
                                "Rare": Colors.OKBLUE
                            }
                            color = rarity_colors.get(rarity, Colors.ENDC)
                            
                            print(f"  {i}. {animal_data['emoji']} {color}{animal_name.capitalize()}{Colors.ENDC} (Lv.{pet_level}) EXP: {pet_exp}/{exp_needed}")
                            print(f"      HP: {stats['hp']} | ATK: {stats['atk']} | MAG: {stats['mag']}")
                else:
                    print(f"  {Colors.GRAY}(Đội trống){Colors.ENDC}")
                
                print(f"\n1. ➕ Thêm pet vào đội")
                print(f"2. ➖ Xóa pet khỏi đội")
                print(f"0. Quay lại")
                
                choice = input(f"\n{Colors.OKCYAN}👉 Chọn: {Colors.ENDC}").strip()
                
                if choice == "1":
                    if len(self.data["team"]) >= 3:
                        print(f"\n{Colors.FAIL}❌ Đội đã đầy (tối đa 3 pet)!{Colors.ENDC}")
                        time.sleep(1.5)
                        continue
                    
                    if not self.data["zoo"]:
                        print(f"\n{Colors.FAIL}❌ Bạn chưa có động vật nào!{Colors.ENDC}")
                        time.sleep(1.5)
                        continue
                    
                    clear_screen()
                    print(Colors.OKGREEN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                    print(Colors.OKGREEN + "║" + " " * 25 + "➕ THÊM PET VÀO ĐỘI" + " " * 24 + "║" + Colors.ENDC)
                    print(Colors.OKGREEN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                    
                    show_rarity_table()
                    
                    print(f"\n{Colors.BOLD}Động vật có sẵn:{Colors.ENDC}\n")
                    
                    available_animals = []
                    index = 1
                    
                    # Hiển thị theo độ hiếm
                    for rarity in ["Common", "Uncommon", "Rare", "Epic", "Mythical", "Legendary"]:
                        animals_in_rarity = []
                        for animal_name in self.data["zoo"].keys():
                            if animal_name not in self.data["team"] and self.get_animal_rarity(animal_name) == rarity:
                                animals_in_rarity.append(animal_name)
                        
                        if animals_in_rarity:
                            rarity_colors = {
                                "Common": Colors.GRAY,
                                "Uncommon": Colors.OKGREEN,
                                "Rare": Colors.OKBLUE,
                                "Epic": Colors.HEADER,
                                "Mythical": Colors.WARNING,
                                "Legendary": Colors.FAIL
                            }
                            color = rarity_colors.get(rarity, Colors.ENDC)
                            print(f"{color}【{rarity}】{Colors.ENDC}")
                            
                            for animal_name in animals_in_rarity:
                                animal_data = self.get_animal_data(animal_name)
                                if animal_data:
                                    pet_level = self.get_pet_level(animal_name)
                                    stats = self.calculate_real_stats(animal_name, pet_level)
                                    print(f"{index}. {animal_data['emoji']} {animal_name.capitalize()} (Lv.{pet_level}) - HP: {stats['hp']} | ATK: {stats['atk']}")
                                    available_animals.append(animal_name)
                                    index += 1
                            print()
                    
                    if not available_animals:
                        print(f"\n{Colors.GRAY}Tất cả động vật đã ở trong đội!{Colors.ENDC}")
                        input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
                        continue
                    
                    print(f"0. Hủy")
                    
                    try:
                        pet_choice = input(f"\n{Colors.OKCYAN}👉 Chọn pet (số): {Colors.ENDC}").strip()
                        
                        if pet_choice == "0":
                            continue
                        
                        pet_idx = int(pet_choice) - 1
                        if 0 <= pet_idx < len(available_animals):
                            selected_pet = available_animals[pet_idx]
                            self.data["team"].append(selected_pet)
                            self.save_data()
                            print(f"\n{Colors.OKGREEN}✅ Đã thêm {selected_pet} vào đội!{Colors.ENDC}")
                            time.sleep(1.5)
                        else:
                            print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                            time.sleep(1.5)
                    except ValueError:
                        print(f"\n{Colors.FAIL}❌ Vui lòng nhập số!{Colors.ENDC}")
                        time.sleep(1.5)
                
                elif choice == "2":
                    if not self.data["team"]:
                        print(f"\n{Colors.FAIL}❌ Đội đang trống!{Colors.ENDC}")
                        time.sleep(1.5)
                        continue
                    
                    clear_screen()
                    print(Colors.FAIL + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                    print(Colors.FAIL + "║" + " " * 25 + "➖ XÓA PET KHỎI ĐỘI" + " " * 24 + "║" + Colors.ENDC)
                    print(Colors.FAIL + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                    
                    print(f"\n{Colors.BOLD}Pet trong đội:{Colors.ENDC}\n")
                    
                    for i, animal_name in enumerate(self.data["team"], 1):
                        animal_data = self.get_animal_data(animal_name)
                        if animal_data:
                            pet_level = self.get_pet_level(animal_name)
                            print(f"{i}. {animal_data['emoji']} {animal_name.capitalize()} (Lv.{pet_level})")
                    
                    print(f"\n0. Hủy")
                    
                    try:
                        remove_choice = input(f"\n{Colors.OKCYAN}👉 Chọn pet cần xóa (số): {Colors.ENDC}").strip()
                        
                        if remove_choice == "0":
                            continue
                        
                        remove_idx = int(remove_choice) - 1
                        if 0 <= remove_idx < len(self.data["team"]):
                            removed_pet = self.data["team"].pop(remove_idx)
                            self.save_data()
                            print(f"\n{Colors.OKGREEN}✅ Đã xóa {removed_pet} khỏi đội!{Colors.ENDC}")
                            time.sleep(1.5)
                        else:
                            print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                            time.sleep(1.5)
                    except ValueError:
                        print(f"\n{Colors.FAIL}❌ Vui lòng nhập số!{Colors.ENDC}")
                        time.sleep(1.5)
                
                elif choice == "0":
                    return
                else:
                    print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                    time.sleep(1)
                    
        except Exception as e:
            self.show_error("Lỗi khi quản lý đội hình", e)
        """Quản lý đội hình"""
        try:
            while True:
                clear_screen()
                print(Colors.HEADER + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                print(Colors.HEADER + "║" + " " * 26 + "⚔️  THIẾT LẬP ĐỘI" + " " * 25 + "║" + Colors.ENDC)
                print(Colors.HEADER + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                
                print(f"\n{Colors.BOLD}Đội hình hiện tại ({len(self.data['team'])}/3):{Colors.ENDC}\n")
                
                if self.data["team"]:
                    for i, animal_name in enumerate(self.data["team"], 1):
                        animal_data = self.get_animal_data(animal_name)
                        if animal_data:
                            stats = self.calculate_real_stats(animal_name, self.data['level'])
                            print(f"  {i}. {animal_data['emoji']} {animal_name.capitalize()} (Lv.{self.data['level']}) - HP: {stats['hp']} | ATK: {stats['atk']}")
                else:
                    print(f"  {Colors.GRAY}(Đội trống){Colors.ENDC}")
                
                print(f"\n1. ➕ Thêm pet vào đội")
                print(f"2. ➖ Xóa pet khỏi đội")
                print(f"0. Quay lại")
                
                choice = input(f"\n{Colors.OKCYAN}👉 Chọn: {Colors.ENDC}").strip()
                
                if choice == "1":
                    if len(self.data["team"]) >= 3:
                        print(f"\n{Colors.FAIL}❌ Đội đã đầy (tối đa 3 pet)!{Colors.ENDC}")
                        time.sleep(1.5)
                        continue
                    
                    if not self.data["zoo"]:
                        print(f"\n{Colors.FAIL}❌ Bạn chưa có động vật nào!{Colors.ENDC}")
                        time.sleep(1.5)
                        continue
                    
                    clear_screen()
                    print(Colors.OKGREEN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                    print(Colors.OKGREEN + "║" + " " * 25 + "➕ THÊM PET VÀO ĐỘI" + " " * 24 + "║" + Colors.ENDC)
                    print(Colors.OKGREEN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                    
                    print(f"\n{Colors.BOLD}Động vật có sẵn:{Colors.ENDC}\n")
                    
                    available_animals = []
                    index = 1
                    for animal_name in self.data["zoo"].keys():
                        if animal_name not in self.data["team"]:
                            animal_data = self.get_animal_data(animal_name)
                            if animal_data:
                                stats = self.calculate_real_stats(animal_name, self.data['level'])
                                print(f"{index}. {animal_data['emoji']} {animal_name.capitalize()} - HP: {stats['hp']} | ATK: {stats['atk']}")
                                available_animals.append(animal_name)
                                index += 1
                    
                    if not available_animals:
                        print(f"\n{Colors.GRAY}Tất cả động vật đã ở trong đội!{Colors.ENDC}")
                        input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
                        continue
                    
                    print(f"\n0. Hủy")
                    
                    try:
                        pet_choice = input(f"\n{Colors.OKCYAN}👉 Chọn pet (số): {Colors.ENDC}").strip()
                        
                        if pet_choice == "0":
                            continue
                        
                        pet_idx = int(pet_choice) - 1
                        if 0 <= pet_idx < len(available_animals):
                            selected_pet = available_animals[pet_idx]
                            self.data["team"].append(selected_pet)
                            self.save_data()
                            print(f"\n{Colors.OKGREEN}✅ Đã thêm {selected_pet} vào đội!{Colors.ENDC}")
                            time.sleep(1.5)
                        else:
                            print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                            time.sleep(1.5)
                    except ValueError:
                        print(f"\n{Colors.FAIL}❌ Vui lòng nhập số!{Colors.ENDC}")
                        time.sleep(1.5)
                
                elif choice == "2":
                    if not self.data["team"]:
                        print(f"\n{Colors.FAIL}❌ Đội đang trống!{Colors.ENDC}")
                        time.sleep(1.5)
                        continue
                    
                    clear_screen()
                    print(Colors.FAIL + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                    print(Colors.FAIL + "║" + " " * 25 + "➖ XÓA PET KHỎI ĐỘI" + " " * 24 + "║" + Colors.ENDC)
                    print(Colors.FAIL + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                    
                    print(f"\n{Colors.BOLD}Pet trong đội:{Colors.ENDC}\n")
                    
                    for i, animal_name in enumerate(self.data["team"], 1):
                        animal_data = self.get_animal_data(animal_name)
                        if animal_data:
                            print(f"{i}. {animal_data['emoji']} {animal_name.capitalize()}")
                    
                    print(f"\n0. Hủy")
                    
                    try:
                        remove_choice = input(f"\n{Colors.OKCYAN}👉 Chọn pet cần xóa (số): {Colors.ENDC}").strip()
                        
                        if remove_choice == "0":
                            continue
                        
                        remove_idx = int(remove_choice) - 1
                        if 0 <= remove_idx < len(self.data["team"]):
                            removed_pet = self.data["team"].pop(remove_idx)
                            self.save_data()
                            print(f"\n{Colors.OKGREEN}✅ Đã xóa {removed_pet} khỏi đội!{Colors.ENDC}")
                            time.sleep(1.5)
                        else:
                            print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                            time.sleep(1.5)
                    except ValueError:
                        print(f"\n{Colors.FAIL}❌ Vui lòng nhập số!{Colors.ENDC}")
                        time.sleep(1.5)
                
                elif choice == "0":
                    return
                else:
                    print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                    time.sleep(1)
                    
        except Exception as e:
            self.show_error("Lỗi khi quản lý đội hình", e)
    
    def show_stats(self):
        """Hiển thị thông tin người chơi"""
        try:
            clear_screen()
            print(Colors.OKCYAN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(Colors.OKCYAN + "║" + Colors.BOLD + " " * 20 + "📊 THÔNG TIN NGƯỜI CHƠI 📊" + " " * 21 + Colors.ENDC + Colors.OKCYAN + "║" + Colors.ENDC)
            print(Colors.OKCYAN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            
            exp_needed = self.get_exp_needed(self.data['level'])
            exp_percent = self.get_exp_percent()
            exp_bar_length = 30
            exp_bar_filled = int((self.data['exp'] / exp_needed) * exp_bar_length)
            exp_bar = "█" * exp_bar_filled + "░" * (exp_bar_length - exp_bar_filled)
            
            print(f"\n{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}║  TÌNH TRẠNG TÀI KHOẢN                                            ║{Colors.ENDC}")
            print(f"{Colors.BOLD}╠══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  💰 Coins:        {Colors.OKGREEN}{Colors.BOLD}{self.data['coins']:>10}{Colors.ENDC}                                    {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  ⭐ Level:        {Colors.BOLD}{self.data['level']:>10}{Colors.ENDC}  ({exp_percent:>5.1f}%)                        {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  ✨ EXP:          [{Colors.OKCYAN}{exp_bar}{Colors.ENDC}] {self.data['exp']}/{exp_needed}           {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  🎒 Túi đồ:       {Colors.BOLD}{len(self.data['inventory']):>10}{Colors.ENDC} vật phẩm                           {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  🔥 Streak:       {Colors.WARNING}{Colors.BOLD}{self.data['daily_streak']:>10}{Colors.ENDC}{Colors.WARNING} ngày{Colors.ENDC}                              {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  ⚔️  Đội hình:     {Colors.BOLD}{len(self.data['team']):>10}/3{Colors.ENDC} pets                            {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
            
            print(f"\n{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}║  THỐNG KÊ GAME                                                    ║{Colors.ENDC}")
            print(f"{Colors.BOLD}╠══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  💵 Tổng coins kiếm:      {Colors.OKGREEN}{self.data['stats']['total_coins_earned']:>10}{Colors.ENDC}                      {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  📅 Số ngày chơi:         {Colors.BOLD}{self.data['stats']['days_played']:>10}{Colors.ENDC}                      {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  🏆 Trận thắng:           {Colors.OKGREEN}{self.data['stats']['battles_won']:>10}{Colors.ENDC}                      {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  🦁 Động vật đã bắt:      {Colors.BOLD}{self.data['stats']['animals_caught']:>10}{Colors.ENDC}                      {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}║{Colors.ENDC}  🎁 Tổng lần nhận daily:  {Colors.BOLD}{self.data['total_daily_collected']:>10}{Colors.ENDC}                      {Colors.BOLD}║{Colors.ENDC}")
            print(f"{Colors.BOLD}╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
            
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
                    # Lưu ngay sau khi mua
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
            # Kiểm tra có pet trong đội không
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
            
            # Tạo đội mình
            player_team = []
            total_player_level = 0
            for animal_name in self.data["team"]:
                animal_data = self.get_animal_data(animal_name)
                if animal_data:
                    pet_level = self.get_pet_level(animal_name)
                    total_player_level += pet_level
                    stats = self.calculate_real_stats(animal_name, pet_level)
                    player_team.append({
                        "name": animal_name,
                        "emoji": animal_data['emoji'],
                        "hp": stats['hp'],
                        "max_hp": stats['hp'],
                        "atk": stats['atk'],
                        "mag": stats['mag'],
                        "pr_percent": stats['pr_percent'],
                        "mr_percent": stats['mr_percent'],
                        "level": pet_level
                    })
            
            # Tính tổng level của đội mình
            max_enemy_level = total_player_level + 3
            
            # Tạo đội địch ngẫu nhiên
            enemy_team = []
            enemy_total_level = 0
            enemy_count = random.randint(1, 3)
            
            # Thu thập tất cả động vật có thể làm địch
            all_animals_list = []
            for rarity, animals in ANIMALS.items():
                if animals:
                    all_animals_list.extend(animals)
            
            for i in range(enemy_count):
                if all_animals_list:
                    enemy_animal = random.choice(all_animals_list)
                    # Random level sao cho tổng không vượt quá
                    remaining_slots = enemy_count - i
                    max_this_level = (max_enemy_level - enemy_total_level) // remaining_slots if remaining_slots > 0 else 1
                    avg_player_level = total_player_level // len(player_team) if player_team else 1
                    enemy_level = random.randint(max(1, avg_player_level - 2), max(1, max_this_level))
                    enemy_total_level += enemy_level
                    
                    stats = self.calculate_real_stats(enemy_animal['name'], enemy_level)
                    enemy_team.append({
                        "name": enemy_animal['name'],
                        "emoji": enemy_animal['emoji'],
                        "hp": stats['hp'],
                        "max_hp": stats['hp'],
                        "atk": stats['atk'],
                        "mag": stats['mag'],
                        "pr_percent": stats['pr_percent'],
                        "mr_percent": stats['mr_percent'],
                        "level": enemy_level
                    })
            
            # Hiển thị đội hình
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
            
            # Bắt đầu chiến đấu (24 lượt tối đa)
            turn = 0
            max_turns = 24
            
            while turn < max_turns:
                turn += 1
                clear_screen()
                print(Colors.WARNING + f"{'═' * 30} LƯỢT {turn}/{max_turns} {'═' * 30}" + Colors.ENDC)
                
                # Hiển thị HP
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
                
                # Đội bạn tấn công
                alive_player = [p for p in player_team if p['hp'] > 0]
                alive_enemy = [p for p in enemy_team if p['hp'] > 0]
                
                if not alive_player or not alive_enemy:
                    break
                
                attacker = random.choice(alive_player)
                target = random.choice(alive_enemy)
                
                # Random sử dụng physical hoặc magical attack
                attack_type = random.choice(['physical', 'magical'])
                if attack_type == 'physical':
                    base_damage = attacker['atk']
                    damage_reduction = target['pr_percent'] / 100
                    attack_icon = "⚔️"
                else:
                    base_damage = attacker['mag']
                    damage_reduction = target['mr_percent'] / 100
                    attack_icon = "✨"
                
                # Tính damage cuối cùng với random variation
                raw_damage = random.randint(int(base_damage * 0.8), int(base_damage * 1.2))
                final_damage = int(raw_damage * (1 - damage_reduction))
                
                target['hp'] -= final_damage
                if target['hp'] < 0:
                    target['hp'] = 0
                
                print(f"\n{attack_icon} {attacker['emoji']} {attacker['name']} tấn công {target['emoji']} {target['name']}: {Colors.FAIL}-{final_damage} HP{Colors.ENDC}")
                time.sleep(0.8)
                
                # Đội địch phản công
                alive_enemy = [p for p in enemy_team if p['hp'] > 0]
                alive_player = [p for p in player_team if p['hp'] > 0]
                
                if alive_enemy and alive_player:
                    attacker = random.choice(alive_enemy)
                    target = random.choice(alive_player)
                    
                    # Random sử dụng physical hoặc magical attack
                    attack_type = random.choice(['physical', 'magical'])
                    if attack_type == 'physical':
                        base_damage = attacker['atk']
                        damage_reduction = target['pr_percent'] / 100
                        attack_icon = "⚔️"
                    else:
                        base_damage = attacker['mag']
                        damage_reduction = target['mr_percent'] / 100
                        attack_icon = "✨"
                    
                    # Tính damage cuối cùng với random variation
                    raw_damage = random.randint(int(base_damage * 0.8), int(base_damage * 1.2))
                    final_damage = int(raw_damage * (1 - damage_reduction))
                    
                    target['hp'] -= final_damage
                    if target['hp'] < 0:
                        target['hp'] = 0
                    
                    print(f"{attack_icon} {attacker['emoji']} {attacker['name']} phản công {target['emoji']} {target['name']}: {Colors.FAIL}-{final_damage} HP{Colors.ENDC}")
                    time.sleep(0.8)
                
                # Kiểm tra kết thúc
                alive_player = [p for p in player_team if p['hp'] > 0]
                alive_enemy = [p for p in enemy_team if p['hp'] > 0]
                
                if not alive_player or not alive_enemy:
                    break
                
                input(f"\n{Colors.GRAY}Nhấn Enter cho lượt tiếp...{Colors.ENDC}")
            
            # Kết quả
            clear_screen()
            alive_player = [p for p in player_team if p['hp'] > 0]
            alive_enemy = [p for p in enemy_team if p['hp'] > 0]
            
            if not alive_enemy and alive_player:
                # Thắng
                print(Colors.OKGREEN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                print(Colors.OKGREEN + "║" + " " * 28 + "🎉 CHIẾN THẮNG!" + " " * 27 + "║" + Colors.ENDC)
                print(Colors.OKGREEN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                
                reward_coins = random.randint(50, 150)
                reward_exp = random.randint(5, 10)  # Người chơi chỉ nhận 5-10 EXP
                
                self.data["coins"] += reward_coins
                self.data["exp"] += reward_exp
                self.data["stats"]["battles_won"] += 1
                self.data["stats"]["total_coins_earned"] += reward_coins
                
                # Check level up người chơi
                level_up_count = 0
                exp_needed = self.get_exp_needed(self.data['level'])
                while self.data["exp"] >= exp_needed:
                    self.data["level"] += 1
                    self.data["exp"] -= exp_needed
                    level_up_count += 1
                    exp_needed = self.get_exp_needed(self.data['level'])
                
                print(f"\n{Colors.BOLD}{'─' * 70}{Colors.ENDC}")
                print(f"{Colors.BOLD}💎 PHẦN THƯỞNG NGƯỜI CHƠI{Colors.ENDC}")
                print(f"{Colors.BOLD}{'─' * 70}{Colors.ENDC}")
                print(f"💰 Coins: {Colors.OKGREEN}+{reward_coins}{Colors.ENDC}")
                print(f"⭐ EXP:   {Colors.OKCYAN}+{reward_exp}{Colors.ENDC}")
                
                if level_up_count > 0:
                    print(f"\n{Colors.WARNING}{'🎊 ' * 35}{Colors.ENDC}")
                    print(f"{Colors.WARNING}{Colors.BOLD}   PLAYER LEVEL UP x{level_up_count}! BẠN ĐẠT LEVEL {self.data['level']}!{Colors.ENDC}")
                    print(f"{Colors.WARNING}{'🎊 ' * 35}{Colors.ENDC}")
                
                # Thêm EXP cho các pets tham gia chiến đấu
                print(f"\n{Colors.BOLD}{'─' * 70}{Colors.ENDC}")
                print(f"{Colors.BOLD}✨ KINH NGHIỆM CHO THÚ CƯNG{Colors.ENDC}")
                print(f"{Colors.BOLD}{'─' * 70}{Colors.ENDC}")
                
                pet_level_ups = {}
                
                for pet in player_team:
                    if pet['hp'] > 0:  # Chỉ pets còn sống nhận EXP
                        pet_name = pet['name']
                        # EXP ngẫu nhiên 20-100 cho mỗi pet (không giới hạn)
                        pet_exp_gain = random.randint(20, 100)
                        
                        # Thêm EXP cho pet
                        level_ups = self.add_pet_exp(pet_name, pet_exp_gain)
                        
                        if level_ups > 0:
                            pet_level_ups[pet_name] = {
                                "level_ups": level_ups,
                                "new_level": self.get_pet_level(pet_name)
                            }
                        
                        animal_data = self.get_animal_data(pet_name)
                        emoji = animal_data['emoji'] if animal_data else "❓"
                        
                        print(f"  {emoji} {Colors.BOLD}{pet_name.capitalize():<12}{Colors.ENDC}", end="")
                        print(f" | +{Colors.OKCYAN}{pet_exp_gain:>3}{Colors.ENDC} EXP", end="")
                        
                        if level_ups > 0:
                            print(f" {Colors.WARNING}→ ⬆️ LEVEL UP x{level_ups}!{Colors.ENDC} {Colors.BOLD}(Lv.{pet_level_ups[pet_name]['new_level']}){Colors.ENDC}")
                        else:
                            current_exp = self.get_pet_exp(pet_name)
                            needed_exp = self.get_pet_exp_needed(pet_name)
                            progress = (current_exp / needed_exp) * 100
                            print(f" | {Colors.GRAY}EXP: {current_exp}/{needed_exp} ({progress:.1f}%){Colors.ENDC}")
                
                print(f"{Colors.BOLD}{'─' * 70}{Colors.ENDC}")
                
                self.save_data()
                
            elif not alive_player and alive_enemy:
                # Thua
                print(Colors.FAIL + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                print(Colors.FAIL + "║" + " " * 28 + "💀 BẠN ĐÃ THUA!" + " " * 28 + "║" + Colors.ENDC)
                print(Colors.FAIL + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                print(f"\n{Colors.GRAY}Hãy nâng cấp đội hình và thử lại!{Colors.ENDC}")
                
            else:
                # Hòa
                print(Colors.WARNING + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                print(Colors.WARNING + "║" + " " * 30 + "🤝 HÒA!" + " " * 31 + "║" + Colors.ENDC)
                print(Colors.WARNING + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                print(f"\n{Colors.GRAY}Trận đấu hết {max_turns} lượt!{Colors.ENDC}")
            
            input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
            
        except Exception as e:
            self.show_error("Lỗi trong chiến đấu", e)
    
    def reset_data(self):
        """Reset tất cả dữ liệu về ban đầu"""
        try:
            clear_screen()
            print(Colors.FAIL + "╔" + "═" * 68 + "╗" + Colors.ENDC)
            print(Colors.FAIL + "║" + " " * 24 + "⚠️  RESET DỮ LIỆU  ⚠️" + " " * 23 + "║" + Colors.ENDC)
            print(Colors.FAIL + "╚" + "═" * 68 + "╝" + Colors.ENDC)
            
            print(f"\n{Colors.WARNING}{Colors.BOLD}CẢNH BÁO:{Colors.ENDC}")
            print(f"{Colors.WARNING}Thao tác này sẽ XÓA TOÀN BỘ dữ liệu game của bạn!{Colors.ENDC}")
            print(f"\n{Colors.GRAY}Bao gồm:{Colors.ENDC}")
            print(f"  • Level và EXP người chơi")
            print(f"  • Tất cả coins")
            print(f"  • Toàn bộ động vật trong sở thú")
            print(f"  • Level và EXP của tất cả pets")
            print(f"  • Đội hình")
            print(f"  • Daily streak")
            print(f"  • Vật phẩm trong túi")
            print(f"  • Tất cả thống kê")
            
            print(f"\n{Colors.FAIL}Hành động này KHÔNG THỂ HOÀN TÁC!{Colors.ENDC}")
            
            confirm1 = input(f"\n{Colors.WARNING}Bạn có chắc chắn muốn reset? (yes/no): {Colors.ENDC}").strip().lower()
            
            if confirm1 == "yes":
                confirm2 = input(f"{Colors.FAIL}Nhập 'RESET' (viết hoa) để xác nhận: {Colors.ENDC}").strip()
                
                if confirm2 == "RESET":
                    loading_animation("Đang reset dữ liệu", 2)
                    
                    # Xóa file dữ liệu
                    if os.path.exists(DATA_FILE):
                        os.remove(DATA_FILE)
                    
                    # Tạo dữ liệu mới
                    self.data = self.create_new_data()
                    self.save_data()
                    
                    clear_screen()
                    print(Colors.OKGREEN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                    print(Colors.OKGREEN + "║" + " " * 23 + "✅ RESET THÀNH CÔNG!" + " " * 24 + "║" + Colors.ENDC)
                    print(Colors.OKGREEN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                    
                    print(f"\n{Colors.BOLD}Dữ liệu đã được reset về ban đầu!{Colors.ENDC}")
                    print(f"\n💰 Coins: {self.data['coins']}")
                    print(f"⭐ Level: {self.data['level']}")
                    print(f"🦁 Sở thú: Trống")
                    print(f"⚔️  Đội hình: Trống")
                    
                    print(f"\n{Colors.OKGREEN}Bạn có thể nhận daily reward ngay bây giờ!{Colors.ENDC}")
                    
                    input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
                else:
                    print(f"\n{Colors.GRAY}❌ Xác nhận không đúng. Đã hủy reset.{Colors.ENDC}")
                    time.sleep(1.5)
            else:
                print(f"\n{Colors.GRAY}Đã hủy reset.{Colors.ENDC}")
                time.sleep(1.5)
                
        except Exception as e:
            self.show_error("Lỗi khi reset dữ liệu", e)
    
    def run(self):
        """Chạy game"""
        try:
            clear_screen()
            print_with_effect("=" * 70, 0.01, Colors.OKCYAN)
            print_with_effect("🎮 CHÀO MỪNG ĐẾN VỚI GAME PHIÊU LƯU!", 0.03, Colors.BOLD)
            print_with_effect("=" * 70, 0.01, Colors.OKCYAN)
            time.sleep(1)
            
            while True:
                try:
                    clear_screen()
                    
                    # Header đẹp
                    print(Colors.OKCYAN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                    print(Colors.OKCYAN + "║" + Colors.BOLD + " " * 22 + "🎮 GAME PHIÊU LƯU THÚ CƯNG 🎮" + " " * 17 + Colors.ENDC + Colors.OKCYAN + "║" + Colors.ENDC)
                    print(Colors.OKCYAN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                    
                    # Thông tin người chơi
                    exp_percent = self.get_exp_percent()
                    exp_needed = self.get_exp_needed(self.data['level'])
                    exp_bar_length = 20
                    exp_bar_filled = int((self.data['exp'] / exp_needed) * exp_bar_length)
                    exp_bar = "█" * exp_bar_filled + "░" * (exp_bar_length - exp_bar_filled)
                    
                    print(f"\n{Colors.BOLD}┌─ THÔNG TIN NGƯỜI CHƠI {'─' * 45}┐{Colors.ENDC}")
                    print(f"{Colors.BOLD}│{Colors.ENDC} 💰 Coins: {Colors.OKGREEN}{Colors.BOLD}{self.data['coins']:>8}{Colors.ENDC}  │  ⭐ Level: {Colors.BOLD}{self.data['level']:>3}{Colors.ENDC}  │  🔥 Streak: {Colors.WARNING}{self.data['daily_streak']:>3} ngày{Colors.ENDC}")
                    print(f"{Colors.BOLD}│{Colors.ENDC} ✨ EXP: [{Colors.OKCYAN}{exp_bar}{Colors.ENDC}] {self.data['exp']}/{exp_needed} ({exp_percent:.1f}%)")
                    print(f"{Colors.BOLD}└{'─' * 68}┘{Colors.ENDC}")
                    
                    # Menu với box đẹp
                    print(f"\n{Colors.BOLD}╔══════════════════════ MENU CHÍNH ═══════════════════════╗{Colors.ENDC}")
                    print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.OKBLUE}1.{Colors.ENDC} 📊 Xem thông tin    {Colors.BOLD}│{Colors.ENDC}  {Colors.OKBLUE}5.{Colors.ENDC} 🎣 Săn bắt            {Colors.BOLD}║{Colors.ENDC}")
                    print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.OKBLUE}2.{Colors.ENDC} 🏪 Cửa hàng        {Colors.BOLD}│{Colors.ENDC}  {Colors.OKBLUE}6.{Colors.ENDC} 🦁 Sở thú            {Colors.BOLD}║{Colors.ENDC}")
                    print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.OKBLUE}3.{Colors.ENDC} ⚔️  Chiến đấu        {Colors.BOLD}│{Colors.ENDC}  {Colors.OKBLUE}7.{Colors.ENDC} ⚔️  Thiết lập đội      {Colors.BOLD}║{Colors.ENDC}")
                    print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.OKBLUE}4.{Colors.ENDC} 🎁 Nhận daily       {Colors.BOLD}│{Colors.ENDC}  {Colors.FAIL}0.{Colors.ENDC} 🚪 Thoát game         {Colors.BOLD}║{Colors.ENDC}")
                    print(f"{Colors.BOLD}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
                    print(f"\n{Colors.GRAY}💡 Mẹo: Nhập 'xoadulieu' để reset game về ban đầu{Colors.ENDC}")
                    
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
                    elif choice == "xoadulieu":
                        self.reset_data()
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
        # Kiểm tra hệ thống trước khi chạy
        check_requirements()
        clear_screen()
        
        # Chạy game
        game = Game()
        game.run()
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Lỗi khởi động game:{Colors.ENDC}")
        print(f"{type(e).__name__}: {str(e)}")
        traceback.print_exc()
        sys.exit(1)
