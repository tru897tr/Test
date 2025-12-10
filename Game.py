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

# Danh sách động vật theo độ hiếm
ANIMALS = {
    "Common": [
        {"name": "bee", "emoji": "🐝", "chance": 20},
        {"name": "bug", "emoji": "🐛", "chance": 20},
        {"name": "snail", "emoji": "🐌", "chance": 20},
        {"name": "butterfly", "emoji": "🦋", "chance": 20},
        {"name": "beetle", "emoji": "🪲", "chance": 20}
    ]
}

def clear_screen():
    """Xóa màn hình để gọn gàng"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_with_effect(text, delay=0.02, color=""):
    """In text với hiệu ứng đánh máy"""
    for char in text:
        print(color + char + Colors.ENDC, end='', flush=True)
        time.sleep(delay)
    print()

def print_box(text, color=Colors.OKCYAN, width=60):
    """In text trong box đẹp"""
    print(color + "╔" + "═" * (width - 2) + "╗" + Colors.ENDC)
    lines = text.split('\n')
    for line in lines:
        padding = width - len(line) - 4
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
        
    def show_error(self, message, error):
        """Hiển thị lỗi chi tiết với debug info"""
        clear_screen()
        print(Colors.FAIL + "╔" + "═" * 58 + "╗" + Colors.ENDC)
        print(Colors.FAIL + "║" + " " * 20 + "⚠️  LỖI HỆ THỐNG  ⚠️" + " " * 19 + "║" + Colors.ENDC)
        print(Colors.FAIL + "╚" + "═" * 58 + "╝" + Colors.ENDC)
        print(f"\n{Colors.BOLD}Mô tả lỗi:{Colors.ENDC} {message}")
        print(f"{Colors.BOLD}Loại lỗi:{Colors.ENDC} {type(error).__name__}")
        print(f"{Colors.BOLD}Chi tiết:{Colors.ENDC} {str(error)}")
        print(f"\n{Colors.GRAY}{'='*60}")
        print("DEBUG TRACEBACK:")
        print('='*60)
        traceback.print_exc()
        print('='*60 + Colors.ENDC)
        input(f"\n{Colors.WARNING}Nhấn Enter để tiếp tục...{Colors.ENDC}")
        
    def load_data(self):
        """Tải dữ liệu từ file hoặc tạo mới nếu chưa có"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Đảm bảo có trường zoo
                    if "zoo" not in data:
                        data["zoo"] = {}
                    # Đảm bảo có trường animals_caught trong stats
                    if "stats" not in data:
                        data["stats"] = {}
                    if "animals_caught" not in data["stats"]:
                        data["stats"]["animals_caught"] = 0
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
            "coins": 100,  # Cho sẵn 100 coins để bắt đầu
            "level": 1,
            "exp": 0,
            "last_daily": None,
            "inventory": [],
            "zoo": {},  # Lưu động vật đã săn: {"bee": 3, "dragon": 1}
            "stats": {
                "total_coins_earned": 0,
                "days_played": 0,
                "battles_won": 0,
                "animals_caught": 0
            }
        }
    
    def save_data(self):
        """Lưu dữ liệu vào file"""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            print(f"{Colors.OKGREEN}💾 Dữ liệu đã được lưu!{Colors.ENDC}")
        except Exception as e:
            self.show_error("Lỗi khi lưu dữ liệu", e)
    
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
                    print_box(f"⏰ Bạn đã nhận daily rồi!\n⏳ Quay lại sau {hours} giờ {minutes} phút", Colors.WARNING)
                    input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
                    return False
            
            loading_animation("Đang xử lý daily reward", 1)
            
            # Nhận thưởng
            self.data["coins"] += 1000
            self.data["stats"]["total_coins_earned"] += 1000
            self.data["stats"]["days_played"] += 1
            self.data["last_daily"] = now.isoformat()
            self.save_data()
            
            clear_screen()
            print(Colors.OKGREEN + "╔" + "═" * 58 + "╗" + Colors.ENDC)
            print(Colors.OKGREEN + "║" + " " * 16 + "🎁 PHẦN THƯỞNG HÀNG NGÀY 🎁" + " " * 15 + "║" + Colors.ENDC)
            print(Colors.OKGREEN + "╚" + "═" * 58 + "╝" + Colors.ENDC)
            print_with_effect(f"\n✨ Bạn đã nhận: {Colors.BOLD}+1000 coins!{Colors.ENDC}", 0.03, Colors.OKGREEN)
            print(f"💰 Tổng coins hiện tại: {Colors.BOLD}{self.data['coins']}{Colors.ENDC}")
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
            loading_animation("Đang săn bắt", 1.5)
            
            # Chọn động vật ngẫu nhiên dựa trên tỷ lệ
            all_animals = []
            for rarity, animals in ANIMALS.items():
                for animal in animals:
                    all_animals.extend([animal] * int(animal["chance"] * 10))
            
            caught_animal = random.choice(all_animals)
            animal_name = caught_animal["name"]
            animal_emoji = caught_animal["emoji"]
            
            # Tìm rarity
            rarity = ""
            for r, animals in ANIMALS.items():
                if any(a["name"] == animal_name for a in animals):
                    rarity = r
                    break
            
            # Cập nhật zoo
            if animal_name in self.data["zoo"]:
                self.data["zoo"][animal_name] += 1
            else:
                self.data["zoo"][animal_name] = 1
            
            self.data["stats"]["animals_caught"] += 1
            self.save_data()
            
            clear_screen()
            rarity_colors = {
                "Common": Colors.GRAY,
                "Uncommon": Colors.OKGREEN,
                "Rare": Colors.OKBLUE,
                "Epic": Colors.HEADER,
                "Legendary": Colors.WARNING
            }
            color = rarity_colors.get(rarity, Colors.ENDC)
            
            print(color + "╔" + "═" * 58 + "╗" + Colors.ENDC)
            print(color + "║" + " " * 20 + "🎣 SĂN BẮT THÀNH CÔNG!" + " " * 18 + "║" + Colors.ENDC)
            print(color + "╚" + "═" * 58 + "╝" + Colors.ENDC)
            print(f"\n{animal_emoji} Bạn đã bắt được: {Colors.BOLD}{animal_name.upper()}{Colors.ENDC}")
            print(f"✨ Độ hiếm: {color}{rarity}{Colors.ENDC}")
            print(f"📊 Số lượng hiện có: {Colors.BOLD}{self.data['zoo'][animal_name]}{Colors.ENDC}")
            print(f"💰 Coins còn lại: {self.data['coins']}")
            input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
            
        except Exception as e:
            self.show_error("Lỗi khi săn bắt động vật", e)
    
    def show_zoo(self):
        """Hiển thị sở thú"""
        try:
            clear_screen()
            print(Colors.OKCYAN + "╔" + "═" * 58 + "╗" + Colors.ENDC)
            print(Colors.OKCYAN + "║" + " " * 24 + "🦁 SỞ THÚ 🦁" + " " * 23 + "║" + Colors.ENDC)
            print(Colors.OKCYAN + "╚" + "═" * 58 + "╝" + Colors.ENDC)
            
            rarity_colors = {
                "Common": Colors.GRAY,
                "Uncommon": Colors.OKGREEN,
                "Rare": Colors.OKBLUE,
                "Epic": Colors.HEADER,
                "Legendary": Colors.WARNING
            }
            
            total_unique = len(self.data["zoo"])
            total_caught = sum(self.data["zoo"].values())
            
            print(f"\n📊 Tổng số loài: {Colors.BOLD}{total_unique}{Colors.ENDC}")
            print(f"🎯 Tổng số con: {Colors.BOLD}{total_caught}{Colors.ENDC}\n")
            
            for rarity, animals in ANIMALS.items():
                color = rarity_colors.get(rarity, Colors.ENDC)
                print(f"{color}{'─' * 60}{Colors.ENDC}")
                print(f"{color}{Colors.BOLD}✨ {rarity.upper()}{Colors.ENDC}")
                print(f"{color}{'─' * 60}{Colors.ENDC}")
                
                for animal in animals:
                    name = animal["name"]
                    emoji = animal["emoji"]
                    
                    if name in self.data["zoo"]:
                        count = self.data["zoo"][name]
                        print(f"  {emoji} {name.capitalize():<15} x{count}")
                    else:
                        print(f"  ❓ {'?':<15} x0 {Colors.GRAY}(Chưa bắt được){Colors.ENDC}")
                print()
            
            input(f"{Colors.GRAY}Nhấn Enter để quay lại...{Colors.ENDC}")
            
        except Exception as e:
            self.show_error("Lỗi khi hiển thị sở thú", e)
    
    def show_stats(self):
        """Hiển thị thông tin người chơi"""
        try:
            clear_screen()
            print(Colors.OKCYAN + "╔" + "═" * 58 + "╗" + Colors.ENDC)
            print(Colors.OKCYAN + "║" + " " * 18 + "📊 THÔNG TIN NGƯỜI CHƠI" + " " * 17 + "║" + Colors.ENDC)
            print(Colors.OKCYAN + "╚" + "═" * 58 + "╝" + Colors.ENDC)
            
            exp_percent = (self.data['exp'] / 100) * 20
            exp_bar = "█" * int(exp_percent) + "░" * (20 - int(exp_percent))
            
            print(f"\n💰 Coins: {Colors.BOLD}{Colors.OKGREEN}{self.data['coins']}{Colors.ENDC}")
            print(f"⭐ Level: {Colors.BOLD}{self.data['level']}{Colors.ENDC}")
            print(f"✨ EXP: [{exp_bar}] {self.data['exp']}/100")
            print(f"🎒 Túi đồ: {len(self.data['inventory'])} vật phẩm")
            
            print(f"\n{Colors.BOLD}📈 THỐNG KÊ:{Colors.ENDC}")
            print(f"  • Tổng coins kiếm được: {self.data['stats']['total_coins_earned']}")
            print(f"  • Số ngày chơi: {self.data['stats']['days_played']}")
            print(f"  • Trận thắng: {self.data['stats']['battles_won']}")
            print(f"  • Động vật đã bắt: {self.data['stats']['animals_caught']}")
            
            input(f"\n{Colors.GRAY}Nhấn Enter để quay lại...{Colors.ENDC}")
            
        except Exception as e:
            self.show_error("Lỗi khi hiển thị thông tin", e)
    
    def shop(self):
        """Cửa hàng mua vật phẩm"""
        try:
            items = {
                "1": {"name": "Kiếm sắt", "price": 500, "desc": "Vũ khí cơ bản", "emoji": "⚔️"},
                "2": {"name": "Áo giáp", "price": 800, "desc": "Tăng phòng thủ", "emoji": "🛡️"},
                "3": {"name": "Thuốc hồi máu", "price": 200, "desc": "Hồi 50 HP", "emoji": "💊"},
                "4": {"name": "Bùa may mắn", "price": 1500, "desc": "Tăng tỷ lệ critical", "emoji": "🍀"}
            }
            
            clear_screen()
            print(Colors.OKGREEN + "╔" + "═" * 58 + "╗" + Colors.ENDC)
            print(Colors.OKGREEN + "║" + " " * 24 + "🏪 CỬA HÀNG" + " " * 23 + "║" + Colors.ENDC)
            print(Colors.OKGREEN + "╚" + "═" * 58 + "╝" + Colors.ENDC)
            print(f"\n💰 Coins của bạn: {Colors.BOLD}{self.data['coins']}{Colors.ENDC}\n")
            
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
            
        except Exception as e:
            self.show_error("Lỗi trong cửa hàng", e)
    
    def battle(self):
        """Chiến đấu với quái vật"""
        try:
            monsters = [
                {"name": "Slime", "hp": 30, "reward": 100, "emoji": "🟢"},
                {"name": "Goblin", "hp": 50, "reward": 200, "emoji": "👺"},
                {"name": "Orc", "hp": 80, "reward": 350, "emoji": "👹"},
                {"name": "Dragon", "hp": 150, "reward": 1000, "emoji": "🐲"}
            ]
            
            monster = random.choice(monsters)
            player_hp = 100
            max_monster_hp = monster["hp"]
            
            clear_screen()
            print(Colors.FAIL + "╔" + "═" * 58 + "╗" + Colors.ENDC)
            print(Colors.FAIL + "║" + f"  ⚔️  BẮT GẶP {monster['name'].upper()}! {monster['emoji']}" + " " * (50 - len(monster['name'])) + "║" + Colors.ENDC)
            print(Colors.FAIL + "╚" + "═" * 58 + "╝" + Colors.ENDC)
            
            while monster["hp"] > 0 and player_hp > 0:
                # Thanh HP
                monster_hp_percent = (monster["hp"] / max_monster_hp) * 30
                monster_hp_bar = "█" * int(monster_hp_percent) + "░" * (30 - int(monster_hp_percent))
                player_hp_percent = (player_hp / 100) * 30
                player_hp_bar = "█" * int(player_hp_percent) + "░" * (30 - int(player_hp_percent))
                
                print(f"\n👹 {monster['name']} HP: [{Colors.FAIL}{monster_hp_bar}{Colors.ENDC}] {monster['hp']}/{max_monster_hp}")
                print(f"👤 Your HP: [{Colors.OKGREEN}{player_hp_bar}{Colors.ENDC}] {player_hp}/100")
                
                print(f"\n1. ⚔️  Tấn công")
                print(f"2. 🏃 Bỏ chạy")
                choice = input(f"\n{Colors.OKCYAN}👉 Chọn hành động: {Colors.ENDC}").strip()
                
                if choice == "1":
                    damage = random.randint(15, 30)
                    monster["hp"] -= damage
                    print(f"\n{Colors.OKGREEN}⚔️  Bạn gây {damage} sát thương!{Colors.ENDC}")
                    time.sleep(0.5)
                    
                    if monster["hp"] > 0:
                        enemy_damage = random.randint(10, 20)
                        player_hp -= enemy_damage
                        print(f"{Colors.FAIL}💥 {monster['name']} phản công gây {enemy_damage} sát thương!{Colors.ENDC}")
                        time.sleep(0.5)
                elif choice == "2":
                    print(f"\n{Colors.WARNING}🏃 Bạn đã bỏ chạy!{Colors.ENDC}")
                    time.sleep(1)
                    return
                else:
                    print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                    time.sleep(0.5)
                    continue
            
            if player_hp > 0:
                clear_screen()
                print(Colors.OKGREEN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                print(Colors.OKGREEN + "║" + " " * 28 + "🎉 CHIẾN THẮNG!" + " " * 27 + "║" + Colors.ENDC)
                print(Colors.OKGREEN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                print(f"\n💰 +{monster['reward']} coins")
                print(f"✨ +50 EXP")
                
                self.data["coins"] += monster["reward"]
                self.data["exp"] += 50
                self.data["stats"]["total_coins_earned"] += monster["reward"]
                self.data["stats"]["battles_won"] += 1
                
                if self.data["exp"] >= 100:
                    self.data["level"] += 1
                    self.data["exp"] -= 100
                    print(f"\n{Colors.WARNING}🎊 LEVEL UP! Bạn đạt Level {self.data['level']}!{Colors.ENDC}")
                
                self.save_data()
                input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
            else:
                clear_screen()
                print(Colors.FAIL + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                print(Colors.FAIL + "║" + " " * 28 + "💀 BẠN ĐÃ THUA!" + " " * 28 + "║" + Colors.ENDC)
                print(Colors.FAIL + "╚" + "═" * 68 + "╝" + Colors.ENDC)
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
                clear_screen()
                print(Colors.OKCYAN + "╔" + "═" * 68 + "╗" + Colors.ENDC)
                print(Colors.OKCYAN + "║" + " " * 29 + "MENU CHÍNH" + " " * 29 + "║" + Colors.ENDC)
                print(Colors.OKCYAN + "╚" + "═" * 68 + "╝" + Colors.ENDC)
                
                print(f"\n💰 Coins: {Colors.BOLD}{self.data['coins']}{Colors.ENDC} | ⭐ Level: {Colors.BOLD}{self.data['level']}{Colors.ENDC} | 🔥 Streak: {Colors.WARNING}{self.data['daily_streak']}{Colors.ENDC}")
                print("\n1. 📊 Xem thông tin")
                print("2. 🏪 Cửa hàng")
                print("3. ⚔️  Chiến đấu")
                print("4. 🎁 Nhận daily")
                print("5. 🎣 Săn bắt")
                print("6. 🦁 Sở thú")
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
                elif choice == "0":
                    clear_screen()
                    print_with_effect("👋 Tạm biệt! Hẹn gặp lại!", 0.03, Colors.OKGREEN)
                    self.save_data()
                    time.sleep(1)
                    break
                else:
                    print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            clear_screen()
            print(f"\n{Colors.WARNING}⚠️  Game bị gián đoạn!{Colors.ENDC}")
            self.save_data()
            sys.exit(0)
        except Exception as e:
            self.show_error("Lỗi nghiêm trọng trong game", e)
            sys.exit(1)

if __name__ == "__main__":
    # Kiểm tra hệ thống trước khi chạy
    check_requirements()
    clear_screen()
    
    # Chạy game
    game = Game()
    game.run()monster['name']} phản công gây {enemy_damage} sát thương!{Colors.ENDC}")
                        time.sleep(0.5)
                elif choice == "2":
                    print(f"\n{Colors.WARNING}🏃 Bạn đã bỏ chạy!{Colors.ENDC}")
                    time.sleep(1)
                    return
                else:
                    print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                    time.sleep(0.5)
                    continue
            
            if player_hp > 0:
                clear_screen()
                print(Colors.OKGREEN + "╔" + "═" * 58 + "╗" + Colors.ENDC)
                print(Colors.OKGREEN + "║" + " " * 22 + "🎉 CHIẾN THẮNG!" + " " * 21 + "║" + Colors.ENDC)
                print(Colors.OKGREEN + "╚" + "═" * 58 + "╝" + Colors.ENDC)
                print(f"\n💰 +{monster['reward']} coins")
                print(f"✨ +50 EXP")
                
                self.data["coins"] += monster["reward"]
                self.data["exp"] += 50
                self.data["stats"]["total_coins_earned"] += monster["reward"]
                self.data["stats"]["battles_won"] += 1
                
                if self.data["exp"] >= 100:
                    self.data["level"] += 1
                    self.data["exp"] = 0
                    print(f"\n{Colors.WARNING}🎊 LEVEL UP! Bạn đạt Level {self.data['level']}!{Colors.ENDC}")
                
                self.save_data()
                input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
            else:
                clear_screen()
                print(Colors.FAIL + "╔" + "═" * 58 + "╗" + Colors.ENDC)
                print(Colors.FAIL + "║" + " " * 22 + "💀 BẠN ĐÃ THUA!" + " " * 22 + "║" + Colors.ENDC)
                print(Colors.FAIL + "╚" + "═" * 58 + "╝" + Colors.ENDC)
                input(f"\n{Colors.GRAY}Nhấn Enter để tiếp tục...{Colors.ENDC}")
                
        except Exception as e:
            self.show_error("Lỗi trong chiến đấu", e)
    
    def run(self):
        """Chạy game"""
        try:
            clear_screen()
            print_with_effect("=" * 60, 0.01, Colors.OKCYAN)
            print_with_effect("🎮 CHÀO MỪNG ĐÃ ĐẾN VỚI GAME PHIÊU LƯU!", 0.03, Colors.BOLD)
            print_with_effect("=" * 60, 0.01, Colors.OKCYAN)
            time.sleep(1)
            
            while True:
                clear_screen()
                print(Colors.OKCYAN + "╔" + "═" * 58 + "╗" + Colors.ENDC)
                print(Colors.OKCYAN + "║" + " " * 23 + "MENU CHÍNH" + " " * 25 + "║" + Colors.ENDC)
                print(Colors.OKCYAN + "╚" + "═" * 58 + "╝" + Colors.ENDC)
                
                print(f"\n💰 Coins: {Colors.BOLD}{self.data['coins']}{Colors.ENDC} | ⭐ Level: {Colors.BOLD}{self.data['level']}{Colors.ENDC}")
                print("\n1. 📊 Xem thông tin")
                print("2. 🏪 Cửa hàng")
                print("3. ⚔️  Chiến đấu")
                print("4. 🎁 Nhận daily")
                print("5. 🎣 Săn bắt")
                print("6. 🦁 Sở thú")
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
                elif choice == "0":
                    clear_screen()
                    print_with_effect("👋 Tạm biệt! Hẹn gặp lại!", 0.03, Colors.OKGREEN)
                    self.save_data()
                    time.sleep(1)
                    break
                else:
                    print(f"\n{Colors.FAIL}❌ Lựa chọn không hợp lệ!{Colors.ENDC}")
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            clear_screen()
            print(f"\n{Colors.WARNING}⚠️  Game bị gián đoạn!{Colors.ENDC}")
            self.save_data()
            sys.exit(0)
        except Exception as e:
            self.show_error("Lỗi nghiêm trọng trong game", e)
            sys.exit(1)

if __name__ == "__main__":
    game = Game()
    game.run()
