import random
import time
import os
import sys
import subprocess
from datetime import datetime
import platform
import socket

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Colors:
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def type_text(text, delay=0.015, color=Colors.GREEN):
    """Hiệu ứng typing"""
    for char in text:
        sys.stdout.write(f"{color}{char}{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_bar(text="Loading", duration=2, width=50):
    """Loading bar đơn giản và đẹp"""
    for i in range(width + 1):
        progress = i / width
        filled = int(width * progress)
        bar = "█" * filled + "░" * (width - filled)
        percentage = int(progress * 100)
        
        if percentage < 40:
            color = Colors.RED
        elif percentage < 75:
            color = Colors.YELLOW
        else:
            color = Colors.GREEN
        
        sys.stdout.write(f"\r  {color}[{bar}]{Colors.RESET} {percentage:3d}% {text}")
        sys.stdout.flush()
        time.sleep(duration / width)
    
    print(f"\r  {Colors.GREEN}[{'█' * width}]{Colors.RESET} 100% {text} {Colors.GREEN}✓{Colors.RESET}")

def check_and_install_dependencies():
    """Kiểm tra và cài đặt dependencies - CỰC ĐẸP"""
    clear()
    
    # Banner đẹp
    print(f"""
{Colors.CYAN}{Colors.BRIGHT}
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║            🔍 DEPENDENCY VERIFICATION SYSTEM 🔍         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
{Colors.RESET}
    """)
    
    time.sleep(0.5)
    
    required = {
        'psutil': 'System & hardware monitoring',
        'requests': 'HTTP library for API calls'
    }
    
    print(f"{Colors.YELLOW}  ► Scanning dependencies...{Colors.RESET}\n")
    time.sleep(0.8)
    
    results = {}
    missing = []
    
    # Kiểm tra từng package
    for pkg, desc in required.items():
        sys.stdout.write(f"  {Colors.CYAN}[SCAN]{Colors.RESET} {pkg:<12} - ")
        sys.stdout.flush()
        time.sleep(0.4)
        
        try:
            __import__(pkg)
            print(f"{Colors.GREEN}{Colors.BRIGHT}✓ OK{Colors.RESET}      ({desc})")
            results[pkg] = True
        except ImportError:
            print(f"{Colors.RED}{Colors.BRIGHT}✗ ERROR{Colors.RESET}   ({desc})")
            results[pkg] = False
            missing.append(pkg)
        
        time.sleep(0.3)
    
    print(f"\n{Colors.CYAN}{'─' * 60}{Colors.RESET}\n")
    
    # Nếu tất cả OK
    if not missing:
        print(f"  {Colors.GREEN}{Colors.BRIGHT}✓ ALL DEPENDENCIES INSTALLED{Colors.RESET}")
        print(f"  {Colors.GREEN}System is ready to launch!{Colors.RESET}\n")
        time.sleep(1.5)
        return True
    
    # Nếu thiếu packages
    print(f"  {Colors.RED}{Colors.BRIGHT}⚠ MISSING: {len(missing)} package(s){Colors.RESET}")
    print(f"  {Colors.RED}Required: {', '.join(missing)}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}  ╔════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.YELLOW}  ║                                                        ║{Colors.RESET}")
    print(f"{Colors.YELLOW}  ║  {Colors.BRIGHT}Would you like to install missing packages?{Colors.RESET}       {Colors.YELLOW}║{Colors.RESET}")
    print(f"{Colors.YELLOW}  ║                                                        ║{Colors.RESET}")
    print(f"{Colors.YELLOW}  ╠════════════════════════════════════════════════════════╣{Colors.RESET}")
    print(f"{Colors.YELLOW}  ║                                                        ║{Colors.RESET}")
    print(f"{Colors.GREEN}  ║  [1] YES - Auto install (Recommended)                 ║{Colors.RESET}")
    print(f"{Colors.RED}  ║  [2] NO  - Continue anyway  {Colors.BRIGHT}⚠ HIGH RISK{Colors.RESET}{Colors.RED}            ║{Colors.RESET}")
    print(f"{Colors.YELLOW}  ║                                                        ║{Colors.RESET}")
    print(f"{Colors.YELLOW}  ╚════════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    while True:
        try:
            choice = input(f"  {Colors.CYAN}Your choice [1/2]: {Colors.RESET}").strip()
            
            if choice == "1":
                print(f"\n{Colors.CYAN}{'─' * 60}{Colors.RESET}\n")
                print(f"  {Colors.GREEN}► Starting installation...{Colors.RESET}\n")
                time.sleep(0.5)
                
                success_count = 0
                for pkg in missing:
                    print(f"  {Colors.CYAN}Installing {pkg}...{Colors.RESET}")
                    
                    try:
                        result = subprocess.run(
                            [sys.executable, "-m", "pip", "install", pkg, "-q"],
                            capture_output=True,
                            timeout=60
                        )
                        
                        if result.returncode == 0:
                            print(f"  {Colors.GREEN}✓ {pkg} installed successfully{Colors.RESET}\n")
                            success_count += 1
                        else:
                            print(f"  {Colors.RED}✗ Failed to install {pkg}{Colors.RESET}\n")
                    except Exception as e:
                        print(f"  {Colors.RED}✗ Error: {str(e)[:40]}{Colors.RESET}\n")
                    
                    time.sleep(0.3)
                
                print(f"{Colors.CYAN}{'─' * 60}{Colors.RESET}\n")
                
                if success_count == len(missing):
                    print(f"  {Colors.GREEN}{Colors.BRIGHT}✓ Installation completed successfully!{Colors.RESET}\n")
                    input(f"  {Colors.DIM}Press Enter to verify installation...{Colors.RESET}")
                    return check_and_install_dependencies()  # Kiểm tra lại
                else:
                    print(f"  {Colors.YELLOW}⚠ Partial installation ({success_count}/{len(missing)}){Colors.RESET}\n")
                    input(f"  {Colors.DIM}Press Enter to continue...{Colors.RESET}")
                    return False
            
            elif choice == "2":
                print(f"\n{Colors.RED}{'─' * 60}{Colors.RESET}\n")
                print(f"  {Colors.RED}{Colors.BRIGHT}⚠ WARNING - RUNNING WITHOUT DEPENDENCIES ⚠{Colors.RESET}\n")
                print(f"  {Colors.RED}Consequences:{Colors.RESET}")
                print(f"  {Colors.RED}  • System Information will NOT work{Colors.RESET}")
                print(f"  {Colors.RED}  • Crypto Tracker limited to demo mode{Colors.RESET}")
                print(f"  {Colors.RED}  • Features may crash unexpectedly{Colors.RESET}\n")
                print(f"{Colors.RED}{'─' * 60}{Colors.RESET}\n")
                
                confirm = input(f"  {Colors.YELLOW}Type 'CONTINUE' to proceed: {Colors.RESET}").strip()
                if confirm.upper() == 'CONTINUE':
                    print(f"\n  {Colors.YELLOW}⚠ Proceeding with limited mode...{Colors.RESET}\n")
                    time.sleep(1.5)
                    return False
                else:
                    print(f"\n  {Colors.GREEN}✓ Good choice! Please install dependencies.{Colors.RESET}\n")
                    time.sleep(1)
                    sys.exit(0)
            else:
                print(f"  {Colors.RED}Invalid choice! Enter 1 or 2.{Colors.RESET}")
        
        except KeyboardInterrupt:
            print(f"\n\n  {Colors.RED}Installation cancelled.{Colors.RESET}\n")
            sys.exit(0)

def show_banner():
    """Banner khởi động - GỌN GÀN"""
    clear()
    
    print(f"""
{Colors.CYAN}{Colors.BRIGHT}
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║     ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗       ║
    ║     ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗      ║
    ║     ███████║███████║██║     █████╔╝ █████╗  ██████╔╝      ║
    ║     ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗      ║
    ║     ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║      ║
    ║     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝      ║
    ║                                                           ║
    ║         ████████╗███████╗██████╗ ███╗   ███╗              ║
    ║         ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║              ║
    ║            ██║   █████╗  ██████╔╝██╔████╔██║              ║
    ║            ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║              ║
    ║            ██║   ███████╗██║  ██║██║ ╚═╝ ██║              ║
    ║            ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝              ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
{Colors.RESET}
    """)
    
    loading_bar("Booting system", 1.8)
    
    print(f"\n  {Colors.GREEN}{Colors.BRIGHT}>>> SYSTEM ONLINE <<<{Colors.RESET}\n")
    time.sleep(0.8)

def menu_selection():
    """Menu gọn gàng"""
    options = [
        ("🌧️  Matrix Digital Rain", "matrix"),
        ("💰 Crypto Tracker [REAL-TIME]", "crypto"),
        ("🔐 Password Generator", "password"),
        ("🌈 Rainbow Text Effect", "rainbow"),
        ("🚀 Rocket Launch", "rocket"),
        ("🖥️  System Information", "sysinfo"),
        ("❌ Exit", "exit")
    ]
    
    while True:
        clear()
        print(f"\n{Colors.CYAN}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BRIGHT}  ║       🔥 CYBER CONTROL CENTER V3 🔥                ║{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        for idx, (desc, _) in enumerate(options, 1):
            if "REAL-TIME" in desc:
                print(f"  {Colors.CYAN}{Colors.BRIGHT}[{idx}]{Colors.RESET} {desc}")
            elif idx == len(options):
                print(f"  {Colors.RED}{Colors.BRIGHT}[{idx}]{Colors.RESET} {desc}")
            else:
                print(f"  {Colors.GREEN}[{idx}]{Colors.RESET} {desc}")
        
        now = datetime.now().strftime("%H:%M:%S")
        print(f"\n  {Colors.DIM}Time: {now} | Status: {Colors.GREEN}ONLINE{Colors.RESET}\n")
        
        try:
            choice = input(f"  {Colors.CYAN}root@terminal:~# {Colors.RESET}").strip()
            
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx][1]
            else:
                print(f"  {Colors.RED}✗ Invalid option!{Colors.RESET}")
                time.sleep(1)
        except (ValueError, KeyboardInterrupt):
            print(f"\n  {Colors.RED}✗ Invalid input!{Colors.RESET}")
            time.sleep(1)

def feature_crypto():
    """Crypto tracker - FIXED & BEAUTIFUL"""
    clear()
    
    print(f"\n{Colors.YELLOW}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BRIGHT}  ║        💰 CRYPTO PRICE TRACKER [LIVE] 💰           ║{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    # Check requests
    try:
        import requests
        has_requests = True
    except ImportError:
        has_requests = False
    
    if not has_requests:
        print(f"  {Colors.RED}✗ 'requests' not installed{Colors.RESET}")
        print(f"  {Colors.YELLOW}⚠ Running in DEMO mode...{Colors.RESET}\n")
        demo_mode = True
    else:
        loading_bar("Connecting to CoinGecko API", 1.5)
        
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,solana,cardano&vs_currencies=usd&include_24h_change=true"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            prices = {
                "BTC": {"price": data["bitcoin"]["usd"], "change": data["bitcoin"].get("usd_24h_change", 0)},
                "ETH": {"price": data["ethereum"]["usd"], "change": data["ethereum"].get("usd_24h_change", 0)},
                "BNB": {"price": data["binancecoin"]["usd"], "change": data["binancecoin"].get("usd_24h_change", 0)},
                "SOL": {"price": data["solana"]["usd"], "change": data["solana"].get("usd_24h_change", 0)},
                "ADA": {"price": data["cardano"]["usd"], "change": data["cardano"].get("usd_24h_change", 0)}
            }
            demo_mode = False
            print(f"  {Colors.GREEN}✓ Connected successfully!{Colors.RESET}\n")
        except Exception as e:
            demo_mode = True
            print(f"  {Colors.RED}✗ Connection failed{Colors.RESET}")
            print(f"  {Colors.YELLOW}⚠ Using DEMO mode{Colors.RESET}\n")
            prices = {
                "BTC": {"price": 45000, "change": 2.5},
                "ETH": {"price": 3000, "change": 1.8},
                "BNB": {"price": 450, "change": -0.5},
                "SOL": {"price": 100, "change": 3.2},
                "ADA": {"price": 0.5, "change": -1.1}
            }
    
    if demo_mode:
        prices = {
            "BTC": {"price": 45000, "change": 2.5},
            "ETH": {"price": 3000, "change": 1.8},
            "BNB": {"price": 450, "change": -0.5},
            "SOL": {"price": 100, "change": 3.2},
            "ADA": {"price": 0.5, "change": -1.1}
        }
    
    time.sleep(0.8)
    print(f"  {Colors.DIM}Press Ctrl+C to stop...{Colors.RESET}\n")
    time.sleep(0.8)
    
    coins = list(prices.keys())
    update_count = 0
    
    try:
        while True:
            # Update real data every 30 seconds
            if not demo_mode and update_count > 0 and update_count % 30 == 0:
                try:
                    response = requests.get(url, timeout=10)
                    data = response.json()
                    prices = {
                        "BTC": {"price": data["bitcoin"]["usd"], "change": data["bitcoin"].get("usd_24h_change", 0)},
                        "ETH": {"price": data["ethereum"]["usd"], "change": data["ethereum"].get("usd_24h_change", 0)},
                        "BNB": {"price": data["binancecoin"]["usd"], "change": data["binancecoin"].get("usd_24h_change", 0)},
                        "SOL": {"price": data["solana"]["usd"], "change": data["solana"].get("usd_24h_change", 0)},
                        "ADA": {"price": data["cardano"]["usd"], "change": data["cardano"].get("usd_24h_change", 0)}
                    }
                except:
                    pass
            
            update_count += 1
            now = datetime.now().strftime("%H:%M:%S")
            mode = f"{Colors.RED}[DEMO]{Colors.RESET}" if demo_mode else f"{Colors.GREEN}[LIVE]{Colors.RESET}"
            
            # Header
            print(f"  {Colors.CYAN}╔══════════════════════════════════════════════════╗{Colors.RESET}")
            print(f"  {Colors.CYAN}║{Colors.BRIGHT} MARKET {Colors.RESET}{mode} {Colors.DIM}{now}{Colors.RESET}                               {Colors.CYAN}║{Colors.RESET}")
            print(f"  {Colors.CYAN}╠══════════════════════════════════════════════════╣{Colors.RESET}")
            print(f"  {Colors.CYAN}║ {'COIN':^6} │ {'PRICE':^14} │ {'24H':^12} │ {'TREND':^7} ║{Colors.RESET}")
            print(f"  {Colors.CYAN}╠══════════════════════════════════════════════════╣{Colors.RESET}")
            
            # Data
            for coin in coins:
                if demo_mode:
                    delta = random.uniform(-0.2, 0.2)
                    prices[coin]["change"] += delta
                    prices[coin]["price"] *= (1 + delta/100)
                
                price = prices[coin]["price"]
                change = prices[coin]["change"]
                
                color = Colors.GREEN if change > 0 else Colors.RED
                arrow = "▲" if change > 0 else "▼"
                
                chart_len = int(min(abs(change), 7))
                chart = "█" * chart_len
                
                if price >= 1000:
                    price_str = f"${price:>12,.2f}"
                else:
                    price_str = f"${price:>12,.4f}"
                
                change_str = f"{arrow} {abs(change):>4.2f}%"
                
                print(f"  {Colors.CYAN}║{Colors.BRIGHT} {coin:^6}{Colors.RESET} {Colors.CYAN}│{Colors.RESET} {price_str} {Colors.CYAN}│{Colors.RESET} {color}{change_str:^12}{Colors.RESET} {Colors.CYAN}│{Colors.RESET} {color}{chart:^7}{Colors.RESET} {Colors.CYAN}║{Colors.RESET}")
            
            print(f"  {Colors.CYAN}╚══════════════════════════════════════════════════╝{Colors.RESET}")
            
            # Stats
            avg = sum(prices[c]["change"] for c in coins) / len(coins)
            trend = "🚀 BULL" if avg > 0 else "📉 BEAR"
            trend_color = Colors.GREEN if avg > 0 else Colors.RED
            
            print(f"\n  {Colors.DIM}Market: {trend_color}{trend}{Colors.RESET} {Colors.DIM}| Avg: {trend_color}{avg:+.2f}%{Colors.RESET}", end="")
            
            if not demo_mode:
                next_update = 30 - (update_count % 30)
                print(f" {Colors.DIM}| Next: {next_update}s{Colors.RESET}")
            else:
                print()
            
            print()
            
            time.sleep(1)
            
            # Clear previous display
            for _ in range(12):
                sys.stdout.write('\033[F\033[K')
    
    except KeyboardInterrupt:
        print(f"\n\n  {Colors.GREEN}✓ Tracker stopped{Colors.RESET}\n")
        time.sleep(1)

def feature_sysinfo():
    """System info - CLEAN"""
    clear()
    
    try:
        import psutil
        has_psutil = True
    except ImportError:
        has_psutil = False
    
    print(f"\n{Colors.MAGENTA}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║          🖥️  SYSTEM INFORMATION 🖥️                 ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    if not has_psutil:
        print(f"  {Colors.RED}✗ 'psutil' not installed!{Colors.RESET}")
        print(f"  {Colors.YELLOW}Install with: pip install psutil{Colors.RESET}\n")
        input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")
        return
    
    loading_bar("Scanning system", 1.5)
    print()
    
    # System
    print(f"  {Colors.CYAN}━━━ 💻 SYSTEM ━━━{Colors.RESET}\n")
    uname = platform.uname()
    print(f"  {Colors.GREEN}►{Colors.RESET} OS       : {Colors.CYAN}{uname.system} {uname.release}{Colors.RESET}")
    print(f"  {Colors.GREEN}►{Colors.RESET} Machine  : {Colors.CYAN}{uname.machine}{Colors.RESET}")
    print(f"  {Colors.GREEN}►{Colors.RESET} Hostname : {Colors.CYAN}{uname.node}{Colors.RESET}\n")
    
    # CPU
    print(f"  {Colors.CYAN}━━━ ⚡ CPU ━━━{Colors.RESET}\n")
    print(f"  {Colors.GREEN}►{Colors.RESET} Cores    : {Colors.CYAN}{psutil.cpu_count(logical=False)} Physical, {psutil.cpu_count(logical=True)} Logical{Colors.RESET}")
    
    cpu = psutil.cpu_percent(interval=1)
    cpu_color = Colors.RED if cpu > 80 else Colors.YELLOW if cpu > 50 else Colors.GREEN
    cpu_bar = int(cpu / 2)
    print(f"  {Colors.GREEN}►{Colors.RESET} Usage    : [{cpu_color}{'█' * cpu_bar}{'░' * (50 - cpu_bar)}{Colors.RESET}] {cpu_color}{cpu:.1f}%{Colors.RESET}\n")
    
    # Memory
    print(f"  {Colors.CYAN}━━━ 🧠 MEMORY ━━━{Colors.RESET}\n")
    mem = psutil.virtual_memory()
    
    def size(b):
        for u in ['B','KB','MB','GB','TB']:
            if b < 1024: return f"{b:.2f} {u}"
            b /= 1024
    
    print(f"  {Colors.GREEN}►{Colors.RESET} Total    : {Colors.CYAN}{size(mem.total)}{Colors.RESET}")
    print(f"  {Colors.GREEN}►{Colors.RESET} Available: {Colors.CYAN}{size(mem.available)}{Colors.RESET}")
    
    mem_color = Colors.RED if mem.percent > 80 else Colors.YELLOW if mem.percent > 50 else Colors.GREEN
    mem_bar = int(mem.percent / 2)
    print(f"  {Colors.GREEN}►{Colors.RESET} Usage    : [{mem_color}{'█' * mem_bar}{'░' * (50 - mem_bar)}{Colors.RESET}] {mem_color}{mem.percent:.1f}%{Colors.RESET}\n")
    
    # Disk
    print(f"  {Colors.CYAN}━━━ 💾 DISK ━━━{Colors.RESET}\n")
    for part in psutil.disk_partitions()[:1]:
        try:
            usage = psutil.disk_usage(part.mountpoint)
            print(f"  {Colors.GREEN}►{Colors.RESET} Device   : {Colors.CYAN}{part.device}{Colors.RESET}")
            print(f"  {Colors.GREEN}►{Colors.RESET} Total    : {Colors.CYAN}{size(usage.total)}{Colors.RESET}")
            print(f"  {Colors.GREEN}►{Colors.RESET} Free     : {Colors.CYAN}{size(usage.free)}{Colors.RESET}")
            
            disk_color = Colors.RED if usage.percent > 80 else Colors.YELLOW if usage.percent > 50 else Colors.GREEN
            disk_bar = int(usage.percent / 2)
            print(f"  {Colors.GREEN}►{Colors.RESET} Usage    : [{disk_color}{'█' * disk_bar}{'░' * (50 - disk_bar)}{Colors.RESET}] {disk_color}{usage.percent:.1f}%{Colors.RESET}\n")
        except:
            print(f"  {Colors.RED}✗ Access denied{Colors.RESET}\n")
    
    # Network
    print(f"  {Colors.CYAN}━━━ 🌐 NETWORK ━━━{Colors.RESET}\n")
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
        print(f"  {Colors.GREEN}►{Colors.RESET} Hostname : {Colors.CYAN}{hostname}{Colors.RESET}")
        print(f"  {Colors.GREEN}►{Colors.RESET} IP       : {Colors.CYAN}{ip}{Colors.RESET}\n")
    except:
        print(f"  {Colors.RED}✗ Network info unavailable{Colors.RESET}\n")
    
    print(f"  {Colors.GREEN}{'─' * 52}{Colors.RESET}")
    print(f"  {Colors.GREEN}✓ Scan complete!{Colors.RESET}")
    print(f"  {Colors.GREEN}{'─' * 52}{Colors.RESET}\n")
    
    input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")

def feature_matrix():
    """Matrix rain - SMOOTH"""
    clear()
    print(f"\n{Colors.GREEN}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BRIGHT}  ║            🌧️  MATRIX DIGITAL RAIN 🌧️              ║{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    loading_bar("Loading Matrix protocol", 1.5)
    print(f"\n  {Colors.DIM}Press Ctrl+C to exit...{Colors.RESET}\n")
    time.sleep(0.8)
    
    chars = "ｱｲｳｴｵ01アイウABCDEF"
    width = 54
    height = 18
    
    try:
        while True:
            for _ in range(height):
                line = "  " + "".join([
                    f"{Colors.BRIGHT if random.random() > 0.92 else ''}{Colors.GREEN}{random.choice(chars)}{Colors.RESET}"
                    for _ in range(width)
                ])
                print(line)
                time.sleep(0.04)
            
            sys.stdout.write(f"\033[{height}A")
    
    except KeyboardInterrupt:
        print(f"\n\n  {Colors.GREEN}✓ Matrix disconnected{Colors.RESET}\n")
        time.sleep(1)

def feature_password():
    """Password generator"""
    clear()
    print(f"\n{Colors.MAGENTA}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║       🔐 QUANTUM PASSWORD GENERATOR 🔐             ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    loading_bar("Initializing quantum engine", 1.2)
    print()
    
    import string
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    
    for i in range(5):
        password = ''.join(random.choice(chars) for _ in range(16))
        
        print(f"  {Colors.CYAN}[{i+1}]{Colors.RESET} Generating", end="")
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.2)
        
        print(f"\r  {Colors.GREEN}[{i+1}]{Colors.RESET} {Colors.BRIGHT}{password}{Colors.RESET}")
        time.sleep(0.3)
    
    print(f"\n  {Colors.GREEN}✓ Generation complete{Colors.RESET}\n")
    input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")

def feature_rainbow():
    """Rainbow text"""
    clear()
    
    print(f"\n{Colors.CYAN}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.CYAN}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.CYAN}  ║           🌈 RAINBOW TEXT EFFECT 🌈                ║{Colors.RESET}")
    print(f"{Colors.CYAN}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.CYAN}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    text = input(f"  {Colors.CYAN}Enter text: {Colors.RESET}")
    print()
    
    loading_bar("Applying effect", 1)
    print()
    
    colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
    
    for round in range(20):
        result = "  "
        for i, char in enumerate(text):
            color = colors[(i + round) % len(colors)]
            result += f"{color}{Colors.BRIGHT}{char}{Colors.RESET}"
        
        print(f"\r{result}", end="", flush=True)
        time.sleep(0.08)
    
    print(f"\n\n  {Colors.GREEN}✓ Complete{Colors.RESET}\n")
    input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")

def feature_rocket():
    """Rocket launch"""
    clear()
    print(f"\n{Colors.RED}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.RED}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.RED}{Colors.BRIGHT}  ║           🚀 ROCKET LAUNCH SEQUENCE 🚀             ║{Colors.RESET}")
    print(f"{Colors.RED}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.RED}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    stages = [
        "Pre-launch check",
        "Fuel loading",
        "Engine test",
        "Navigation online",
        "Final prep"
    ]
    
    for stage in stages:
        loading_bar(stage, 0.8)
        time.sleep(0.2)
    
    print(f"\n  {Colors.YELLOW}{Colors.BRIGHT}COUNTDOWN INITIATED{Colors.RESET}\n")
    time.sleep(0.5)
    
    for i in range(10, 0, -1):
        print(f"\r  {Colors.RED}{Colors.BRIGHT}T-{i:02d}{Colors.RESET}", end="", flush=True)
        time.sleep(0.5)
    
    print(f"\n\n  {Colors.RED}{Colors.BRIGHT}🚀 LIFTOFF! 🚀{Colors.RESET}\n")
    
    frames = ["    🚀", "   🚀 ", "  🚀  ", " 🚀   ", "🚀    "]
    for _ in range(5):
        for frame in frames:
            print(f"\r  {frame}", end="", flush=True)
            time.sleep(0.08)
    
    print(f"\n\n  {Colors.GREEN}✓ Launch successful!{Colors.RESET}\n")
    input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")

def main():
    """Main program"""
    try:
        # Check dependencies FIRST
        check_and_install_dependencies()
        
        # Show banner
        show_banner()
        
        # Main loop
        while True:
            choice = menu_selection()
            
            if choice == "exit":
                clear()
                print(f"\n  {Colors.CYAN}Shutting down...{Colors.RESET}\n")
                loading_bar("Disconnecting", 1.2)
                print(f"\n  {Colors.GREEN}✓ Goodbye! 👋{Colors.RESET}\n")
                break
            elif choice == "matrix":
                feature_matrix()
            elif choice == "crypto":
                feature_crypto()
            elif choice == "password":
                feature_password()
            elif choice == "rainbow":
                feature_rainbow()
            elif choice == "rocket":
                feature_rocket()
            elif choice == "sysinfo":
                feature_sysinfo()
            else:
                clear()
                print(f"\n  {Colors.YELLOW}⚠ Under development{Colors.RESET}\n")
                time.sleep(1)
    
    except KeyboardInterrupt:
        clear()
        print(f"\n  {Colors.RED}✗ Shutdown{Colors.RESET}\n")
        time.sleep(0.8)

if __name__ == "__main__":
    main()
