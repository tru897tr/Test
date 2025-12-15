#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 GAME PHIÊU LƯU THÚ CƯNG
Phiên bản: 5.0.0
Tác giả: Nguyễn Thanh Trứ
Bản quyền © 2024 Nguyễn Thanh Trứ. All rights reserved.
"""

import os
import sys
import json
import random
import time
import traceback
from datetime import datetime, timedelta

# ==================== CONSTANTS ====================
DATA_FILE = "game_data.json"
LANG_FILE = "language.json"
VERSION = "5.0.0"
AUTHOR = "Nguyễn Thanh Trứ"

# ==================== COLORS ====================
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

# ==================== ANIMALS DATA ====================
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
    "Legendary": []
}

RARITY_EXP_REQUIREMENTS = {
    "Common": 50,
    "Uncommon": 75,
    "Rare": 100,
    "Epic": 150,
    "Mythical": 200,
    "Legendary": 350
}

# ==================== LANGUAGES ====================
LANGUAGES = {
    "vi": {
        "name": "Tiếng Việt",
        "flag": "🇻🇳",
        "translations": {
            "game_title": "🎮 GAME PHIÊU LƯU THÚ CƯNG 🎮",
            "main_menu": "MENU CHÍNH",
            "player_info": "THÔNG TIN NGƯỜI CHƠI",
            "coins": "Coins",
            "level": "Level",
            "streak": "Streak",
            "exp": "EXP",
            "menu_stats": "📊 Xem thông tin",
            "menu_shop": "🏪 Cửa hàng",
            "menu_battle": "⚔️  Chiến đấu",
            "menu_daily": "🎁 Nhận daily",
            "menu_hunt": "🎣 Săn bắt",
            "menu_zoo": "🦁 Sở thú",
            "menu_team": "⚔️  Thiết lập đội",
            "menu_settings": "⚙️  Cài đặt",
            "menu_info": "ℹ️  Thông tin game",
            "menu_exit": "🚪 Thoát game",
            "press_enter": "Nhấn Enter để tiếp tục...",
            "choose": "Nhập lựa chọn",
            "back": "Quay lại",
            "cancel": "Hủy",
            "confirm": "Xác nhận",
            "yes": "Có",
            "no": "Không",
            "loading": "Đang tải",
            "victory": "CHIẾN THẮNG!",
            "defeat": "BẠN ĐÃ THUA!",
            "draw": "HÒA!",
            "player_reward": "PHẦN THƯỞNG NGƯỜI CHƠI",
            "pet_exp": "KINH NGHIỆM CHO THÚ CƯNG",
            "level_up": "LEVEL UP",
            "rarity_table": "BẢNG PHÂN LOẠI ĐỘ HIẾM",
            "rarity": "Độ hiếm",
            "icon": "Icon",
            "exp_per_level": "EXP/Lv",
            "species_count": "Số loài",
            "color": "Màu sắc",
            "team_setup": "THIẾT LẬP ĐỘI",
            "current_team": "Đội hình hiện tại",
            "add_pet": "➕ Thêm pet vào đội",
            "remove_pet": "➖ Xóa pet khỏi đội",
            "view_details": "👁️  Xem chi tiết",
            "shop_coming_soon": "Cửa hàng sẽ được nâng cấp trong tương lai gần!",
            "settings": "CÀI ĐẶT",
            "language": "Ngôn ngữ",
            "game_info": "THÔNG TIN GAME",
            "version": "Phiên bản",
            "copyright": "Bản quyền",
            "changelog": "Lịch sử thay đổi",
            "apply_language": "Bạn có chắc muốn áp dụng ngôn ngữ này không?",
            "language_applied": "Đã áp dụng ngôn ngữ thành công!",
            "downloading": "Đang tải gói ngôn ngữ"
        }
    },
    "en": {
        "name": "English",
        "flag": "🇬🇧",
        "translations": {
            "game_title": "🎮 PET ADVENTURE GAME 🎮",
            "main_menu": "MAIN MENU",
            "player_info": "PLAYER INFO",
            "coins": "Coins",
            "level": "Level",
            "streak": "Streak",
            "exp": "EXP",
            "menu_stats": "📊 View Stats",
            "menu_shop": "🏪 Shop",
            "menu_battle": "⚔️  Battle",
            "menu_daily": "🎁 Daily Reward",
            "menu_hunt": "🎣 Hunt",
            "menu_zoo": "🦁 Zoo",
            "menu_team": "⚔️  Team Setup",
            "menu_settings": "⚙️  Settings",
            "menu_info": "ℹ️  Game Info",
            "menu_exit": "🚪 Exit Game",
            "press_enter": "Press Enter to continue...",
            "choose": "Enter choice",
            "back": "Back",
            "cancel": "Cancel",
            "confirm": "Confirm",
            "yes": "Yes",
            "no": "No",
            "loading": "Loading",
            "victory": "VICTORY!",
            "defeat": "DEFEAT!",
            "draw": "DRAW!",
            "player_reward": "PLAYER REWARD",
            "pet_exp": "PET EXPERIENCE",
            "level_up": "LEVEL UP",
            "rarity_table": "RARITY TABLE",
            "rarity": "Rarity",
            "icon": "Icon",
            "exp_per_level": "EXP/Lv",
            "species_count": "Species",
            "color": "Color",
            "team_setup": "TEAM SETUP",
            "current_team": "Current Team",
            "add_pet": "➕ Add Pet",
            "remove_pet": "➖ Remove Pet",
            "view_details": "👁️  View Details",
            "shop_coming_soon": "Shop will be upgraded soon!",
            "settings": "SETTINGS",
            "language": "Language",
            "game_info": "GAME INFO",
            "version": "Version",
            "copyright": "Copyright",
            "changelog": "Changelog",
            "apply_language": "Are you sure you want to apply this language?",
            "language_applied": "Language applied successfully!",
            "downloading": "Downloading language pack"
        }
    },
    "zh": {
        "name": "中文",
        "flag": "🇨🇳",
        "translations": {
            "game_title": "🎮 宠物冒险游戏 🎮",
            "main_menu": "主菜单",
            "player_info": "玩家信息",
            "coins": "金币",
            "level": "等级",
            "streak": "连续",
            "exp": "经验",
            "menu_stats": "📊 查看信息",
            "menu_shop": "🏪 商店",
            "menu_battle": "⚔️  战斗",
            "menu_daily": "🎁 每日奖励",
            "menu_hunt": "🎣 狩猎",
            "menu_zoo": "🦁 动物园",
            "menu_team": "⚔️  队伍设置",
            "menu_settings": "⚙️  设置",
            "menu_info": "ℹ️  游戏信息",
            "menu_exit": "🚪 退出游戏",
            "press_enter": "按Enter继续...",
            "choose": "输入选择",
            "back": "返回",
            "cancel": "取消",
            "confirm": "确认",
            "yes": "是",
            "no": "否",
            "loading": "加载中",
            "victory": "胜利！",
            "defeat": "失败！",
            "draw": "平局！",
            "player_reward": "玩家奖励",
            "pet_exp": "宠物经验",
            "level_up": "升级",
            "rarity_table": "稀有度表",
            "rarity": "稀有度",
            "icon": "图标",
            "exp_per_level": "经验/级",
            "species_count": "种类",
            "color": "颜色",
            "team_setup": "队伍设置",
            "current_team": "当前队伍",
            "add_pet": "➕ 添加宠物",
            "remove_pet": "➖ 移除宠物",
            "view_details": "👁️  查看详情",
            "shop_coming_soon": "商店即将升级！",
            "settings": "设置",
            "language": "语言",
            "game_info": "游戏信息",
            "version": "版本",
            "copyright": "版权",
            "changelog": "更新日志",
            "apply_language": "您确定要应用此语言吗？",
            "language_applied": "语言应用成功！",
            "downloading": "正在下载语言包"
        }
    }
}

CHANGELOG = """
═══════════════════════════════════════════════════════════════════════
                         📜 LỊCH SỬ CẬP NHẬT
═══════════════════════════════════════════════════════════════════════

🔥 Phiên bản 5.0.0 (Hiện tại) - 15/12/2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✨ Tính năng mới:
    • Hệ thống đa ngôn ngữ (Tiếng Việt, English, 中文)
    • Menu Cài đặt với tùy chọn ngôn ngữ
    • Menu Thông tin game với changelog
    • Cải thiện UI thiết lập đội với bảng chi tiết
    • Bảng stats đầy đủ cho mỗi pet
  
  🔧 Cải tiến:
    • Giao diện menu chính gọn gàng hơn
    • Bố cục bảng chuẩn, không bị lệch
    • Cửa hàng tạm thời tắt (sẽ nâng cấp)
    • Xóa hint 'xoadulieu' khỏi menu
  
  🐛 Sửa lỗi:
    • Fix alignment các bảng
    • Fix đường kẻ không thẳng
    • Fix lỗi syntax trên Termux

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 Phiên bản 4.0.0 - 14/12/2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Cân bằng EXP: Người chơi 5-10, Pets 20-100
  • Cải thiện giao diện battle result
  • Thêm progress bar cho EXP
  • Fix lỗi syntax critical

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Phiên bản 3.0.0 - 13/12/2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Hệ thống EXP cho pets
  • Level riêng cho mỗi pet
  • EXP requirement theo độ hiếm
  • Lệnh xoadulieu để reset game

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚔️  Phiên bản 2.0.0 - 12/12/2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Hệ thống chiến đấu với physical/magical attacks
  • Công thức stats chính xác
  • Resistance system (PR%, MR%)
  • Bảng độ hiếm

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎮 Phiên bản 1.0.0 - 11/12/2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Ra mắt game
  • Hệ thống săn bắt
  • Daily rewards
  • Sở thú
  • Team setup

═══════════════════════════════════════════════════════════════════════
"""

# ==================== UTILITY FUNCTIONS ====================

def clear_screen():
    """Xóa màn hình"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_with_effect(text, delay=0.02, color=Colors.ENDC):
    """In text với hiệu ứng typing"""
    for char in text:
        print(color + char + Colors.ENDC, end='', flush=True)
        time.sleep(delay)
    print()

def print_box(text, color=Colors.ENDC):
    """In text trong box"""
    lines = text.split('\n')
    max_len = max(len(line) for line in lines)
    
    print(color + "╔" + "═" * (max_len + 2) + "╗" + Colors.ENDC)
    for line in lines:
        padding = max_len - len(line)
        print(color + "║ " + Colors.ENDC + line + " " * padding + color + " ║" + Colors.ENDC)
    print(color + "╚" + "═" * (max_len + 2) + "╝" + Colors.ENDC)

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

def show_rarity_table(lang):
    """Hiển thị bảng phân loại độ hiếm"""
    t = lang["translations"]
    
    print(f"\n{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BOLD}║              {t['rarity_table']:<40}              ║{Colors.ENDC}")
    print(f"{Colors.BOLD}╠═══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
    print(f"{Colors.BOLD}║  {t['rarity']:<13} │ {t['icon']:<6} │ {t['exp_per_level']:<8} │ {t['species_count']:<8} │ {t['color']:<10} ║{Colors.ENDC}")
    print(f"{Colors.BOLD}╠═══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
    
    rarity_info = {
        "Common": {"color": Colors.GRAY, "exp_req": 50, "icon": "⚪"},
        "Uncommon": {"color": Colors.OKGREEN, "exp_req": 75, "icon": "🟢"},
        "Rare": {"color": Colors.OKBLUE, "exp_req": 100, "icon": "🔵"},
        "Epic": {"color": Colors.HEADER, "exp_req": 150, "icon": "🟣"},
        "Mythical": {"color": Colors.WARNING, "exp_req": 200, "icon": "🟠"},
        "Legendary": {"color": Colors.FAIL, "exp_req": 350, "icon": "🔴"}
    }
    
    for rarity, info in rarity_info.items():
        animals_in_rarity = ANIMALS.get(rarity, [])
        count = len(animals_in_rarity)
        color = info["color"]
        icon = info["icon"]
        exp_req = info["exp_req"]
        
        print(f"{Colors.BOLD}║{Colors.ENDC}  {color}{rarity:<13}{Colors.ENDC} │  {icon}    │  {Colors.BOLD}{exp_req:>6}{Colors.ENDC}  │    {Colors.BOLD}{count:>2}{Colors.ENDC}     │ {color}{'█' * 10}{Colors.ENDC}  {Colors.BOLD}║{Colors.ENDC}")
    
    print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")

def check_requirements():
    """Kiểm tra yêu cầu hệ thống"""
    try:
        # Check Python version
        if sys.version_info < (3, 6):
            print(f"{Colors.FAIL}❌ Cần Python 3.6 trở lên!{Colors.ENDC}")
            sys.exit(1)
        return True
    except Exception as e:
        print(f"{Colors.FAIL}❌ Lỗi kiểm tra hệ thống: {e}{Colors.ENDC}")
        return False

# ==================== GAME CLASS ====================

class Game:
    def __init__(self):
        try:
            self.data = self.load_data()
            self.lang = self.load_language()
        except Exception as e:
            self.show_error("Lỗi khởi tạo game", e)
            sys.exit(1)
    
    def load_language(self):
        """Load ngôn ngữ"""
        try:
            if os.path.exists(LANG_FILE):
                with open(LANG_FILE, 'r', encoding='utf-8') as f:
                    lang_data = json.load(f)
                    lang_code = lang_data.get("current", "vi")
                    return LANGUAGES.get(lang_code, LANGUAGES["vi"])
            return LANGUAGES["vi"]
        except:
            return LANGUAGES["vi"]
    
    def save_language(self, lang_code):
        """Lưu ngôn ngữ"""
        try:
            with open(LANG_FILE, 'w', encoding='utf-8') as f:
                json.dump({"current": lang_code}, f, ensure_ascii=False, indent=2)
            self.lang = LANGUAGES[lang_code]
        except Exception as e:
            self.show_error("Lỗi lưu ngôn ngữ", e)
    
    def get_exp_needed(self, level):
        """Tính EXP cần để lên level"""
        return 100 + (level - 1) * 50
    
    def get_exp_percent(self):
        """Tính % EXP hiện tại"""
        exp_needed = self.get_exp_needed(self.data['level'])
        return (self.data['exp'] / exp_needed) * 100 if exp_needed > 0 else 0
    
    def show_error(self, message, error):
        """Hiển thị lỗi"""
        print(f"\n{Colors.FAIL}❌ {message}:{Colors.ENDC}")
        print(f"{Colors.GRAY}{type(error).__name__}: {str(error)}{Colors.ENDC}")
    
    def auto_save(self):
        """Tự động lưu (không hiển thị)"""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def save_data(self):
        """Lưu dữ liệu với thông báo"""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.show_error("Lỗi lưu dữ liệu", e)
    
    def create_new_data(self):
        """Tạo dữ liệu mới"""
        return {
            "coins": 100,
            "level": 1,
            "exp": 0,
            "last_daily": None,
            "daily_streak": 0,
            "total_daily_collected": 0,
            "inventory": [],
            "zoo": {},
            "pet_data": {},
            "team": [],
            "stats": {
                "total_coins_earned": 0,
                "days_played": 0,
                "battles_won": 0,
                "animals_caught": 0
            }
        }
    
    def load_data(self):
        """Tải dữ liệu"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
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
    
    def get_animal_data(self, animal_name):
        """Lấy thông tin động vật"""
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
        """Thêm EXP cho pet"""
        if animal_name not in self.data["pet_data"]:
            self.data["pet_data"][animal_name] = {"level": 1, "exp": 0}
        
        self.data["pet_data"][animal_name]["exp"] += exp_amount
        
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
        """Tính toán stats thực tế"""
        animal_data = self.get_animal_data(animal_name)
        if not animal_data:
            return {
                "hp": 500, "atk": 100, "pr": 0, "pr_percent": 0,
                "wp": 500, "mag": 100, "mr": 0, "mr_percent": 0
            }
        
        base_stats = animal_data["stats"]
        hp = 2 * base_stats["hp"] * level + 500
        atk = base_stats["atk"] * level + 100
        
        pr_stat = base_stats["pr"]
        pr_numerator = 25 + 2 * level * pr_stat
        pr_denominator = 125 + 2 * level * pr_stat
        pr_percent = 0.8 * (pr_numerator / pr_denominator) if pr_denominator != 0 else 0
        
        wp = 2 * base_stats["wp"] * level + 500
        mag = base_stats["mag"] * level + 100
        
        mr_stat = base_stats["mr"]
        mr_numerator = 25 + 2 * level * mr_stat
        mr_denominator = 125 + 2 * level * mr_stat
        mr_percent = 0.8 * (mr_numerator / mr_denominator) if mr_denominator != 0 else 0
        
        return {
            "hp": int(hp), "atk": int(atk), "pr": pr_stat, "pr_percent": pr_percent * 100,
            "wp": int(wp), "mag": int(mag), "mr": mr_stat, "mr_percent": mr_percent * 100
        }
    
    def settings_menu(self):
        """Menu cài đặt"""
        t = self.lang["translations"]
        
        while True:
            clear_screen()
            print(f"{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}║                      ⚙️  {t['settings']:<40}⚙️                       ║{Colors.ENDC}")
            print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
            
            print(f"\n{Colors.BOLD}1.{Colors.ENDC} 🌐 {t['language']}")
            print(f"{Colors.BOLD}0.{Colors.ENDC} 🔙 {t['back']}")
            
            choice = input(f"\n{Colors.OKCYAN}👉 {t['choose']}: {Colors.ENDC}").strip()
            
            if choice == "1":
                self.language_menu()
            elif choice == "0":
                return
    
    def language_menu(self):
        """Menu ngôn ngữ"""
        t = self.lang["translations"]
        
        while True:
            clear_screen()
            print(f"{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}║                     🌐 {t['language']:<40}🌐                      ║{Colors.ENDC}")
            print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
            
            print(f"\n{Colors.BOLD}Ngôn ngữ hiện tại:{Colors.ENDC} {self.lang['flag']} {self.lang['name']}\n")
            
            lang_list = list(LANGUAGES.items())
            for i, (code, lang) in enumerate(lang_list, 1):
                status = " ✓" if code == list(LANGUAGES.keys())[list(LANGUAGES.values()).index(self.lang)] else ""
                print(f"{Colors.BOLD}{i}.{Colors.ENDC} {lang['flag']} {lang['name']}{Colors.OKGREEN}{status}{Colors.ENDC}")
            
            print(f"\n{Colors.BOLD}0.{Colors.ENDC} 🔙 {t['back']}")
            
            choice = input(f"\n{Colors.OKCYAN}👉 {t['choose']}: {Colors.ENDC}").strip()
            
            if choice == "0":
                return
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(lang_list):
                    code, lang = lang_list[idx]
                    
                    # Simulate downloading
                    loading_animation(f"{t['downloading']} {lang['name']}", 1.5)
                    
                    # Confirm
                    confirm = input(f"\n{Colors.WARNING}{t['apply_language']} ({lang['flag']} {lang['name']}) (y/n): {Colors.ENDC}").strip().lower()
                    
                    if confirm == "y":
                        self.save_language(code)
                        print(f"\n{Colors.OKGREEN}✅ {t['language_applied']}{Colors.ENDC}")
                        t = self.lang["translations"]  # Reload translations
                        time.sleep(1.5)
                        return
            except ValueError:
                pass
    
    def game_info_menu(self):
        """Menu thông tin game"""
        t = self.lang["translations"]
        
        while True:
            clear_screen()
            print(f"{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}║                    ℹ️  {t['game_info']:<40}ℹ️                     ║{Colors.ENDC}")
            print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
            
            print(f"\n{Colors.BOLD}1.{Colors.ENDC} 📦 {t['version']}")
            print(f"{Colors.BOLD}2.{Colors.ENDC} ©️  {t['copyright']}")
            print(f"{Colors.BOLD}0.{Colors.ENDC} 🔙 {t['back']}")
            
            choice = input(f"\n{Colors.OKCYAN}👉 {t['choose']}: {Colors.ENDC}").strip()
            
            if choice == "1":
                self.show_version_info()
            elif choice == "2":
                self.show_copyright()
            elif choice == "0":
                return
    
    def show_version_info(self):
        """Hiển thị thông tin phiên bản"""
        t = self.lang["translations"]
        clear_screen()
        
        print(f"{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BOLD}║                      📦 {t['version']:<40}📦                       ║{Colors.ENDC}")
        print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}{t['version']}:{Colors.ENDC} {Colors.OKGREEN}{VERSION}{Colors.ENDC}")
        print(f"{Colors.BOLD}Ngày phát hành:{Colors.ENDC} 15/12/2024")
        print(f"{Colors.BOLD}Tác giả:{Colors.ENDC} {AUTHOR}")
        
        print(CHANGELOG)
        
        input(f"\n{Colors.GRAY}{t['press_enter']}{Colors.ENDC}")
    
    def show_copyright(self):
        """Hiển thị bản quyền"""
        t = self.lang["translations"]
        clear_screen()
        
        print(f"{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BOLD}║                     ©️  {t['copyright']:<40}©️                      ║{Colors.ENDC}")
        print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}🎮 GAME PHIÊU LƯU THÚ CƯNG{Colors.ENDC}")
        print(f"\n{Colors.BOLD}Phiên bản:{Colors.ENDC} {VERSION}")
        print(f"{Colors.BOLD}Tác giả:{Colors.ENDC} {AUTHOR}")
        print(f"\n{Colors.WARNING}Bản quyền © 2024 {AUTHOR}. All rights reserved.{Colors.ENDC}")
        print(f"\n{Colors.GRAY}Game này được phát triển bởi {AUTHOR}.{Colors.ENDC}")
        print(f"{Colors.GRAY}Mọi quyền sở hữu trí tuệ đều được bảo lưu.{Colors.ENDC}")
        
        input(f"\n{Colors.GRAY}{t['press_enter']}{Colors.ENDC}")
    
    def shop(self):
        """Cửa hàng"""
        t = self.lang["translations"]
        clear_screen()
        
        print(f"{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BOLD}║                        🏪 CỬA HÀNG 🏪                            ║{Colors.ENDC}")
        print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        print(f"\n{Colors.WARNING}{t['shop_coming_soon']}{Colors.ENDC}")
        print(f"\n{Colors.GRAY}Các tính năng đang được phát triển:{Colors.ENDC}")
        print(f"  • Mua vật phẩm đặc biệt")
        print(f"  • Nâng cấp pets")
        print(f"  • Skin cho pets")
        print(f"  • Và nhiều hơn nữa...")
        
        input(f"\n{Colors.GRAY}{t['press_enter']}{Colors.ENDC}")
    
    def manage_team(self):
        """Quản lý đội hình - với UI cải thiện"""
        t = self.lang["translations"]
        
        while True:
            clear_screen()
            print(f"{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
            print(f"{Colors.BOLD}║                   ⚔️  {t['team_setup']:<40}⚔️                    ║{Colors.ENDC}")
            print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
            
            # Show rarity table
            show_rarity_table(self.lang)
            
            # Current team
            print(f"{Colors.BOLD}{t['current_team']} ({len(self.data['team'])}/3):{Colors.ENDC}\n")
            
            if self.data["team"]:
                print(f"{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
                print(f"{Colors.BOLD}║ # │ Pet         │ Lv  │  HP  │ ATK │ MAG │ PR% │ MR% │ EXP       ║{Colors.ENDC}")
                print(f"{Colors.BOLD}╠═══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
                
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
                        
                        name_display = f"{animal_data['emoji']} {animal_name[:8]}"
                        
                        print(f"{Colors.BOLD}║{Colors.ENDC} {i} │ {color}{name_display:<11}{Colors.ENDC} │ {pet_level:>3} │ {stats['hp']:>4} │ {stats['atk']:>3} │ {stats['mag']:>3} │ {stats['pr_percent']:>3.0f}% │ {stats['mr_percent']:>3.0f}% │ {pet_exp}/{exp_needed:<5} {Colors.BOLD}║{Colors.ENDC}")
                
                print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
            else:
                print(f"  {Colors.GRAY}(Đội trống){Colors.ENDC}")
            
            print(f"\n{Colors.BOLD}1.{Colors.ENDC} {t['add_pet']}")
            print(f"{Colors.BOLD}2.{Colors.ENDC} {t['remove_pet']}")
            print(f"{Colors.BOLD}3.{Colors.ENDC} {t['view_details']}")
            print(f"{Colors.BOLD}0.{Colors.ENDC} {t['back']}")
            
            choice = input(f"\n{Colors.OKCYAN}👉 {t['choose']}: {Colors.ENDC}").strip()
            
            if choice == "1":
                self.add_pet_to_team()
            elif choice == "2":
                self.remove_pet_from_team()
            elif choice == "3":
                self.view_pet_details()
            elif choice == "0":
                return
    
    def view_pet_details(self):
        """Xem chi tiết pet"""
        t = self.lang["translations"]
        
        if not self.data["team"]:
            clear_screen()
            print(f"\n{Colors.FAIL}❌ Đội đang trống!{Colors.ENDC}")
            time.sleep(1.5)
            return
        
        clear_screen()
        print(f"{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BOLD}║                    👁️  XEM CHI TIẾT PET 👁️                         ║{Colors.ENDC}")
        print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Chọn pet để xem chi tiết:{Colors.ENDC}\n")
        
        for i, animal_name in enumerate(self.data["team"], 1):
            animal_data = self.get_animal_data(animal_name)
            if animal_data:
                pet_level = self.get_pet_level(animal_name)
                print(f"{Colors.BOLD}{i}.{Colors.ENDC} {animal_data['emoji']} {animal_name.capitalize()} (Lv.{pet_level})")
        
        print(f"\n{Colors.BOLD}0.{Colors.ENDC} {t['back']}")
        
        choice = input(f"\n{Colors.OKCYAN}👉 {t['choose']}: {Colors.ENDC}").strip()
        
        if choice == "0":
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.data["team"]):
                animal_name = self.data["team"][idx]
                self.show_detailed_pet_stats(animal_name)
        except ValueError:
            pass
    
    def show_detailed_pet_stats(self, animal_name):
        """Hiển thị stats chi tiết của pet"""
        t = self.lang["translations"]
        
        animal_data = self.get_animal_data(animal_name)
        if not animal_data:
            return
        
        pet_level = self.get_pet_level(animal_name)
        pet_exp = self.get_pet_exp(animal_name)
        exp_needed = self.get_pet_exp_needed(animal_name)
        stats = self.calculate_real_stats(animal_name, pet_level)
        rarity = self.get_animal_rarity(animal_name)
        base_stats = animal_data["stats"]
        
        clear_screen()
        print(f"{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BOLD}║               {animal_data['emoji']}  {animal_name.upper()} - CHI TIẾT{' ' * (38 - len(animal_name))}║{Colors.ENDC}")
        print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        rarity_colors = {
            "Common": Colors.GRAY,
            "Uncommon": Colors.OKGREEN,
            "Rare": Colors.OKBLUE
        }
        color = rarity_colors.get(rarity, Colors.ENDC)
        
        print(f"\n{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BOLD}║  THÔNG TIN CHUNG                                                  ║{Colors.ENDC}")
        print(f"{Colors.BOLD}╠═══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
        print(f"{Colors.BOLD}║{Colors.ENDC}  Độ hiếm:        {color}{rarity:<40}{Colors.ENDC}         {Colors.BOLD}║{Colors.ENDC}")
        print(f"{Colors.BOLD}║{Colors.ENDC}  Level:          {Colors.BOLD}{pet_level:<40}{Colors.ENDC}         {Colors.BOLD}║{Colors.ENDC}")
        print(f"{Colors.BOLD}║{Colors.ENDC}  EXP:            {pet_exp}/{exp_needed} ({(pet_exp/exp_needed*100):.1f}%)                          {Colors.BOLD}║{Colors.ENDC}")
        print(f"{Colors.BOLD}║{Colors.ENDC}  EXP/Level:      {RARITY_EXP_REQUIREMENTS[rarity]:<40}         {Colors.BOLD}║{Colors.ENDC}")
        print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BOLD}║  CHỈ SỐ CHIẾN ĐẤU (Lv.{pet_level})                                          ║{Colors.ENDC}")
        print(f"{Colors.BOLD}╠═══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
        print(f"{Colors.BOLD}║  Stat       │ Base │  Real │ Công thức                            ║{Colors.ENDC}")
        print(f"{Colors.BOLD}╠═══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
        print(f"{Colors.BOLD}║{Colors.ENDC}  HP         │  {base_stats['hp']:>2}  │ {stats['hp']:>5} │ 2 × base × lv + 500                   {Colors.BOLD}║{Colors.ENDC}")
        print(f"{Colors.BOLD}║{Colors.ENDC}  ATK        │  {base_stats['atk']:>2}  │ {stats['atk']:>5} │ base × lv + 100                       {Colors.BOLD}║{Colors.ENDC}")
        print(f"{Colors.BOLD}║{Colors.ENDC}  PR         │  {base_stats['pr']:>2}  │ {stats['pr_percent']:>4.0f}% │ 0.8 × ((25+2×lv×pr)/(125+2×lv×pr))    {Colors.BOLD}║{Colors.ENDC}")
        print(f"{Colors.BOLD}║{Colors.ENDC}  WP         │  {base_stats['wp']:>2}  │ {stats['wp']:>5} │ 2 × base × lv + 500                   {Colors.BOLD}║{Colors.ENDC}")
        print(f"{Colors.BOLD}║{Colors.ENDC}  MAG        │  {base_stats['mag']:>2}  │ {stats['mag']:>5} │ base × lv + 100                       {Colors.BOLD}║{Colors.ENDC}")
        print(f"{Colors.BOLD}║{Colors.ENDC}  MR         │  {base_stats['mr']:>2}  │ {stats['mr_percent']:>4.0f}% │ 0.8 × ((25+2×lv×mr)/(125+2×lv×mr))    {Colors.BOLD}║{Colors.ENDC}")
        print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        print(f"\n{Colors.GRAY}HP: Health Points | ATK: Attack | PR: Physical Resistance{Colors.ENDC}")
        print(f"{Colors.GRAY}WP: Willpower | MAG: Magic | MR: Magic Resistance{Colors.ENDC}")
        
        input(f"\n{Colors.GRAY}{t['press_enter']}{Colors.ENDC}")
    
    def add_pet_to_team(self):
        """Thêm pet vào đội"""
        t = self.lang["translations"]
        
        if len(self.data["team"]) >= 3:
            clear_screen()
            print(f"\n{Colors.FAIL}❌ Đội đã đầy (tối đa 3 pet)!{Colors.ENDC}")
            time.sleep(1.5)
            return
        
        if not self.data["zoo"]:
            clear_screen()
            print(f"\n{Colors.FAIL}❌ Bạn chưa có động vật nào!{Colors.ENDC}")
            time.sleep(1.5)
            return
        
        clear_screen()
        print(f"{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BOLD}║                   ➕ THÊM PET VÀO ĐỘI ➕                          ║{Colors.ENDC}")
        print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        show_rarity_table(self.lang)
        
        print(f"{Colors.BOLD}Động vật có sẵn:{Colors.ENDC}\n")
        
        available_animals = []
        index = 1
        
        for rarity in ["Common", "Uncommon", "Rare", "Epic", "Mythical", "Legendary"]:
            animals_in_rarity = []
            for animal_name in self.data["zoo"].keys():
                if animal_name not in self.data["team"] and self.get_animal_rarity(animal_name) == rarity:
                    animals_in_rarity.append(animal_name)
            
            if animals_in_rarity:
                rarity_colors = {
                    "Common": Colors.GRAY,
                    "Uncommon": Colors.OKGREEN,
                    "Rare": Colors.OKBLUE
                }
                color = rarity_colors.get(rarity, Colors.ENDC)
                print(f"{color}【{rarity}】{Colors.ENDC}")
                
                for animal_name in animals_in_rarity:
                    animal_data = self.get_animal_data(animal_name)
                    if animal_data:
                        pet_level = self.get_pet_level(animal_name)
                        stats = self.calculate_real_stats(animal_name, pet_level)
                        print(f"{Colors.BOLD}{index}.{Colors.ENDC} {animal_data['emoji']} {animal_name.capitalize():<12} Lv.{pet_level:>2}  HP:{stats['hp']:>4}  ATK:{stats['atk']:>3}  MAG:{stats['mag']:>3}")
                        available_animals.append(animal_name)
                        index += 1
                print()
        
        if not available_animals:
            print(f"\n{Colors.GRAY}Tất cả động vật đã ở trong đội!{Colors.ENDC}")
            input(f"\n{Colors.GRAY}{t['press_enter']}{Colors.ENDC}")
            return
        
        print(f"{Colors.BOLD}0.{Colors.ENDC} {t['cancel']}")
        
        try:
            pet_choice = input(f"\n{Colors.OKCYAN}👉 Chọn pet (số): {Colors.ENDC}").strip()
            
            if pet_choice == "0":
                return
            
            pet_idx = int(pet_choice) - 1
            if 0 <= pet_idx < len(available_animals):
                selected_pet = available_animals[pet_idx]
                self.data["team"].append(selected_pet)
                self.save_data()
                print(f"\n{Colors.OKGREEN}✅ Đã thêm {selected_pet} vào đội!{Colors.ENDC}")
                time.sleep(1.5)
        except ValueError:
            pass
    
    def remove_pet_from_team(self):
        """Xóa pet khỏi đội"""
        t = self.lang["translations"]
        
        if not self.data["team"]:
            clear_screen()
            print(f"\n{Colors.FAIL}❌ Đội đang trống!{Colors.ENDC}")
            time.sleep(1.5)
            return
        
        clear_screen()
        print(f"{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BOLD}║                   ➖ XÓA PET KHỎI ĐỘI ➖                           ║{Colors.ENDC}")
        print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Pet trong đội:{Colors.ENDC}\n")
        
        for i, animal_name in enumerate(self.data["team"], 1):
            animal_data = self.get_animal_data(animal_name)
            if animal_data:
                pet_level = self.get_pet_level(animal_name)
                print(f"{Colors.BOLD}{i}.{Colors.ENDC} {animal_data['emoji']} {animal_name.capitalize()} (Lv.{pet_level})")
        
        print(f"\n{Colors.BOLD}0.{Colors.ENDC} {t['cancel']}")
        
        try:
            remove_choice = input(f"\n{Colors.OKCYAN}👉 Chọn pet cần xóa (số): {Colors.ENDC}").strip()
            
            if remove_choice == "0":
                return
            
            remove_idx = int(remove_choice) - 1
            if 0 <= remove_idx < len(self.data["team"]):
                removed_pet = self.data["team"].pop(remove_idx)
                self.save_data()
                print(f"\n{Colors.OKGREEN}✅ Đã xóa {removed_pet} khỏi đội!{Colors.ENDC}")
                time.sleep(1.5)
        except ValueError:
            pass
    
    def reset_data(self):
        """Reset dữ liệu"""
        t = self.lang["translations"]
        
        clear_screen()
        print(f"{Colors.FAIL}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.FAIL}║                     ⚠️  RESET DỮ LIỆU  ⚠️                         ║{Colors.ENDC}")
        print(f"{Colors.FAIL}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
        print(f"\n{Colors.WARNING}{Colors.BOLD}CẢNH BÁO:{Colors.ENDC}")
        print(f"{Colors.WARNING}Thao tác này sẽ XÓA TOÀN BỘ dữ liệu game của bạn!{Colors.ENDC}")
        
        confirm1 = input(f"\n{Colors.WARNING}Bạn có chắc chắn muốn reset? (yes/no): {Colors.ENDC}").strip().lower()
        
        if confirm1 == "yes":
            confirm2 = input(f"{Colors.FAIL}Nhập 'RESET' (viết hoa) để xác nhận: {Colors.ENDC}").strip()
            
            if confirm2 == "RESET":
                loading_animation("Đang reset dữ liệu", 2)
                
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                
                self.data = self.create_new_data()
                self.save_data()
                
                clear_screen()
                print(f"{Colors.OKGREEN}✅ RESET THÀNH CÔNG!{Colors.ENDC}")
                print(f"\n{Colors.OKGREEN}Dữ liệu đã được reset về ban đầu!{Colors.ENDC}")
                
                input(f"\n{Colors.GRAY}{t['press_enter']}{Colors.ENDC}")
    
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


    def run(self):
        """Chạy game"""
        t = self.lang["translations"]
        
        try:
            clear_screen()
            print_with_effect("=" * 70, 0.01, Colors.OKCYAN)
            print_with_effect(t['game_title'], 0.03, Colors.BOLD)
            print_with_effect("=" * 70, 0.01, Colors.OKCYAN)
            time.sleep(1)
            
            while True:
                try:
                    clear_screen()
                    
                    # Header
                    print(f"{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
                    print(f"{Colors.BOLD}║              {t['game_title']:<40}              ║{Colors.ENDC}")
                    print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
                    
                    # Player info
                    exp_percent = self.get_exp_percent()
                    exp_needed = self.get_exp_needed(self.data['level'])
                    exp_bar_length = 20
                    exp_bar_filled = int((self.data['exp'] / exp_needed) * exp_bar_length)
                    exp_bar = "█" * exp_bar_filled + "░" * (exp_bar_length - exp_bar_filled)
                    
                    print(f"\n{Colors.BOLD}┌─ {t['player_info']} {'─' * 42}┐{Colors.ENDC}")
                    print(f"{Colors.BOLD}│{Colors.ENDC} 💰 {t['coins']}: {Colors.OKGREEN}{Colors.BOLD}{self.data['coins']:>8}{Colors.ENDC}  │  ⭐ {t['level']}: {Colors.BOLD}{self.data['level']:>3}{Colors.ENDC}  │  🔥 {t['streak']}: {Colors.WARNING}{self.data['daily_streak']:>3}{Colors.ENDC}")
                    print(f"{Colors.BOLD}│{Colors.ENDC} ✨ {t['exp']}: [{Colors.OKCYAN}{exp_bar}{Colors.ENDC}] {self.data['exp']}/{exp_needed} ({exp_percent:.1f}%)")
                    print(f"{Colors.BOLD}└{'─' * 67}┘{Colors.ENDC}")
                    
                    # Menu
                    print(f"\n{Colors.BOLD}╔═══════════════════════ {t['main_menu']} ═══════════════════════╗{Colors.ENDC}")
                    print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.OKBLUE}1.{Colors.ENDC} {t['menu_stats']:<25} {Colors.BOLD}│{Colors.ENDC}  {Colors.OKBLUE}6.{Colors.ENDC} {t['menu_zoo']:<22}  {Colors.BOLD}║{Colors.ENDC}")
                    print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.OKBLUE}2.{Colors.ENDC} {t['menu_shop']:<25} {Colors.BOLD}│{Colors.ENDC}  {Colors.OKBLUE}7.{Colors.ENDC} {t['menu_team']:<22}  {Colors.BOLD}║{Colors.ENDC}")
                    print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.OKBLUE}3.{Colors.ENDC} {t['menu_battle']:<25} {Colors.BOLD}│{Colors.ENDC}  {Colors.OKBLUE}8.{Colors.ENDC} {t['menu_settings']:<22}  {Colors.BOLD}║{Colors.ENDC}")
                    print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.OKBLUE}4.{Colors.ENDC} {t['menu_daily']:<25} {Colors.BOLD}│{Colors.ENDC}  {Colors.OKBLUE}9.{Colors.ENDC} {t['menu_info']:<22}  {Colors.BOLD}║{Colors.ENDC}")
                    print(f"{Colors.BOLD}║{Colors.ENDC}  {Colors.OKBLUE}5.{Colors.ENDC} {t['menu_hunt']:<25} {Colors.BOLD}│{Colors.ENDC}  {Colors.FAIL}0.{Colors.ENDC} {t['menu_exit']:<22}  {Colors.BOLD}║{Colors.ENDC}")
                    print(f"{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
                    
                    choice = input(f"\n{Colors.OKCYAN}👉 {t['choose']}: {Colors.ENDC}").strip().lower()
                    
                    if choice == "1":
                        pass  # self.show_stats() integrated
                    elif choice == "2":
                        self.shop()
                    elif choice == "3":
                        self.battle()
                    elif choice == "4":
                        self.check_daily_reward()
                    elif choice == "5":
                        self.hunt_animal()
                    elif choice == "6":
                        self.show_zoo()
                    elif choice == "7":
                        self.manage_team()
                    elif choice == "8":
                        self.settings_menu()
                    elif choice == "9":
                        self.game_info_menu()
                    elif choice == "xoadulieu":
                        self.reset_data()
                    elif choice == "0":
                        clear_screen()
                        print_with_effect(f"👋 {t['press_enter'].replace('Nhấn Enter để tiếp tục...', 'Tạm biệt! Hẹn gặp lại!')}", 0.03, Colors.OKGREEN)
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

# ==================== MAIN ====================

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
        sys.exit(1)
