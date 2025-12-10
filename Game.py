import json
import os
from datetime import datetime, timedelta
import random

# File lưu dữ liệu
DATA_FILE = "game_data.json"

class Game:
    def __init__(self):
        self.data = self.load_data()
        
    def load_data(self):
        """Tải dữ liệu từ file hoặc tạo mới nếu chưa có"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                print("⚠️  Không thể đọc file dữ liệu, tạo dữ liệu mới...")
                return self.create_new_data()
        else:
            print("🎮 Chào mừng đến với game! Tạo dữ liệu mới...")
            return self.create_new_data()
    
    def create_new_data(self):
        """Tạo dữ liệu mới cho người chơi"""
        return {
            "coins": 0,
            "level": 1,
            "exp": 0,
            "last_daily": None,
            "inventory": [],
            "stats": {
                "total_coins_earned": 0,
                "days_played": 0,
                "battles_won": 0
            }
        }
    
    def save_data(self):
        """Lưu dữ liệu vào file"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        print("💾 Dữ liệu đã được lưu!")
    
    def check_daily_reward(self):
        """Kiểm tra và nhận phần thưởng hàng ngày"""
        now = datetime.now()
        last_daily = self.data.get("last_daily")
        
        if last_daily:
            last_time = datetime.fromisoformat(last_daily)
            time_diff = now - last_time
            
            if time_diff < timedelta(hours=24):
                remaining = timedelta(hours=24) - time_diff
                hours = remaining.seconds // 3600
                minutes = (remaining.seconds % 3600) // 60
                print(f"⏰ Bạn đã nhận daily rồi!")
                print(f"⏳ Quay lại sau {hours} giờ {minutes} phút")
                return False
        
        # Nhận thưởng
        self.data["coins"] += 1000
        self.data["stats"]["total_coins_earned"] += 1000
        self.data["stats"]["days_played"] += 1
        self.data["last_daily"] = now.isoformat()
        self.save_data()
        
        print("=" * 50)
        print("🎁 PHẦN THƯỞNG HÀNG NGÀY 🎁")
        print("=" * 50)
        print("✨ Bạn đã nhận: +1000 coins!")
        print(f"💰 Tổng coins hiện tại: {self.data['coins']}")
        print("=" * 50)
        return True
    
    def show_stats(self):
        """Hiển thị thông tin người chơi"""
        print("\n" + "=" * 50)
        print("📊 THÔNG TIN NGƯỜI CHƠI")
        print("=" * 50)
        print(f"💰 Coins: {self.data['coins']}")
        print(f"⭐ Level: {self.data['level']}")
        print(f"✨ EXP: {self.data['exp']}/100")
        print(f"🎒 Túi đồ: {len(self.data['inventory'])} vật phẩm")
        print("\n📈 Thống kê:")
        print(f"  • Tổng coins kiếm được: {self.data['stats']['total_coins_earned']}")
        print(f"  • Số ngày chơi: {self.data['stats']['days_played']}")
        print(f"  • Trận thắng: {self.data['stats']['battles_won']}")
        print("=" * 50)
    
    def shop(self):
        """Cửa hàng mua vật phẩm"""
        items = {
            "1": {"name": "Kiếm sắt", "price": 500, "desc": "Vũ khí cơ bản"},
            "2": {"name": "Áo giáp", "price": 800, "desc": "Tăng phòng thủ"},
            "3": {"name": "Thuốc hồi máu", "price": 200, "desc": "Hồi 50 HP"},
            "4": {"name": "Bùa may mắn", "price": 1500, "desc": "Tăng tỷ lệ critical"}
        }
        
        print("\n" + "=" * 50)
        print("🏪 CỬA HÀNG")
        print("=" * 50)
        print(f"💰 Coins của bạn: {self.data['coins']}")
        print("\nVật phẩm có sẵn:")
        for key, item in items.items():
            print(f"{key}. {item['name']} - {item['price']} coins")
            print(f"   {item['desc']}")
        print("0. Quay lại")
        print("=" * 50)
        
        choice = input("\n👉 Chọn vật phẩm muốn mua: ").strip()
        
        if choice in items:
            item = items[choice]
            if self.data["coins"] >= item["price"]:
                self.data["coins"] -= item["price"]
                self.data["inventory"].append(item["name"])
                self.save_data()
                print(f"\n✅ Đã mua {item['name']}!")
            else:
                print("\n❌ Không đủ coins!")
        elif choice == "0":
            return
        else:
            print("\n❌ Lựa chọn không hợp lệ!")
    
    def battle(self):
        """Chiến đấu với quái vật"""
        monsters = [
            {"name": "Slime", "hp": 30, "reward": 100},
            {"name": "Goblin", "hp": 50, "reward": 200},
            {"name": "Orc", "hp": 80, "reward": 350},
            {"name": "Dragon", "hp": 150, "reward": 1000}
        ]
        
        monster = random.choice(monsters)
        player_hp = 100
        
        print("\n" + "=" * 50)
        print(f"⚔️  BẮT GẶP {monster['name'].upper()}!")
        print("=" * 50)
        print(f"👹 {monster['name']} HP: {monster['hp']}")
        print(f"👤 Your HP: {player_hp}")
        print("=" * 50)
        
        while monster["hp"] > 0 and player_hp > 0:
            print("\n1. Tấn công")
            print("2. Bỏ chạy")
            choice = input("👉 Chọn hành động: ").strip()
            
            if choice == "1":
                damage = random.randint(15, 30)
                monster["hp"] -= damage
                print(f"\n⚔️  Bạn gây {damage} sát thương!")
                
                if monster["hp"] > 0:
                    enemy_damage = random.randint(10, 20)
                    player_hp -= enemy_damage
                    print(f"💥 {monster['name']} phản công gây {enemy_damage} sát thương!")
                    print(f"❤️  HP của bạn: {player_hp}")
                    print(f"👹 HP {monster['name']}: {monster['hp']}")
            elif choice == "2":
                print("\n🏃 Bạn đã bỏ chạy!")
                return
            else:
                print("\n❌ Lựa chọn không hợp lệ!")
                continue
        
        if player_hp > 0:
            print("\n" + "=" * 50)
            print("🎉 CHIẾN THẮNG!")
            print("=" * 50)
            print(f"💰 +{monster['reward']} coins")
            print(f"✨ +50 EXP")
            self.data["coins"] += monster["reward"]
            self.data["exp"] += 50
            self.data["stats"]["total_coins_earned"] += monster["reward"]
            self.data["stats"]["battles_won"] += 1
            
            # Level up
            if self.data["exp"] >= 100:
                self.data["level"] += 1
                self.data["exp"] = 0
                print(f"🎊 LEVEL UP! Bạn đạt Level {self.data['level']}!")
            
            self.save_data()
        else:
            print("\n" + "=" * 50)
            print("💀 BẠN ĐÃ THUA!")
            print("=" * 50)
    
    def run(self):
        """Chạy game"""
        print("\n" + "=" * 60)
        print("🎮 CHÀO MỪNG ĐÃ ĐẾN VỚI GAME PHIÊU LƯU!")
        print("=" * 60)
        
        while True:
            print("\n" + "=" * 50)
            print("MENU CHÍNH")
            print("=" * 50)
            print("1. Xem thông tin")
            print("2. Cửa hàng")
            print("3. Chiến đấu")
            print("4. Nhận daily (odaily/owo daily)")
            print("0. Thoát game")
            print("=" * 50)
            
            choice = input("\n👉 Nhập lựa chọn: ").strip().lower()
            
            if choice == "1":
                self.show_stats()
            elif choice == "2":
                self.shop()
            elif choice == "3":
                self.battle()
            elif choice in ["4", "odaily", "owo daily", "daily"]:
                self.check_daily_reward()
            elif choice == "0":
                print("\n👋 Tạm biệt! Hẹn gặp lại!")
                self.save_data()
                break
            else:
                print("\n❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    game = Game()
    game.run()
