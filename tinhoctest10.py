#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import os
import sys
import subprocess
from datetime import datetime
import platform
import socket

def clear():
    """Clear screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def loading_bar(text="Loading", duration=2):
    """Simple loading bar"""
    width = 40
    for i in range(width + 1):
        filled = int((i / width) * width)
        bar = "█" * filled + "░" * (width - filled)
        percent = int((i / width) * 100)
        
        if percent < 40:
            color = Colors.RED
        elif percent < 75:
            color = Colors.YELLOW
        else:
            color = Colors.GREEN
        
        print(f"\r  {color}[{bar}]{Colors.RESET} {percent}% {text}", end="", flush=True)
        time.sleep(duration / width)
    
    print(f"\r  {Colors.GREEN}[{'█' * width}]{Colors.RESET} 100% {text} ✓")

def check_dependencies():
    """Check and install dependencies"""
    clear()
    
    print(f"""
{Colors.CYAN}{Colors.BRIGHT}
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║            🔍 DEPENDENCY VERIFICATION SYSTEM 🔍           ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
{Colors.RESET}
    """)
    
    time.sleep(0.5)
    
    required = {
        'psutil': 'System monitoring',
        'requests': 'HTTP library'
    }
    
    print(f"{Colors.YELLOW}  ► Scanning dependencies...{Colors.RESET}\n")
    time.sleep(0.5)
    
    missing = []
    
    for pkg, desc in required.items():
        print(f"  {Colors.CYAN}[SCAN]{Colors.RESET} {pkg:<12} - ", end="", flush=True)
        time.sleep(0.3)
        
        try:
            __import__(pkg)
            print(f"{Colors.GREEN}✓ OK{Colors.RESET}      ({desc})")
        except ImportError:
            print(f"{Colors.RED}✗ ERROR{Colors.RESET}   ({desc})")
            missing.append(pkg)
        
        time.sleep(0.2)
    
    print(f"\n{Colors.CYAN}{'─' * 60}{Colors.RESET}\n")
    
    if not missing:
        print(f"  {Colors.GREEN}{Colors.BRIGHT}✓ ALL DEPENDENCIES INSTALLED{Colors.RESET}")
        print(f"  {Colors.GREEN}System ready!{Colors.RESET}\n")
        time.sleep(1.5)
        return True
    
    print(f"  {Colors.RED}{Colors.BRIGHT}⚠ MISSING: {len(missing)} package(s){Colors.RESET}")
    print(f"  {Colors.RED}Required: {', '.join(missing)}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}  ╔════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.YELLOW}  ║  Would you like to install missing packages?          ║{Colors.RESET}")
    print(f"{Colors.YELLOW}  ╠════════════════════════════════════════════════════════╣{Colors.RESET}")
    print(f"{Colors.GREEN}  ║  [1] YES - Auto install (Recommended)                 ║{Colors.RESET}")
    print(f"{Colors.RED}  ║  [2] NO  - Continue anyway  ⚠ HIGH RISK                ║{Colors.RESET}")
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
                        subprocess.check_call([
                            sys.executable, "-m", "pip", "install", pkg, "-q"
                        ], timeout=60)
                        
                        print(f"  {Colors.GREEN}✓ {pkg} installed!{Colors.RESET}\n")
                        success_count += 1
                    except:
                        print(f"  {Colors.RED}✗ Failed to install {pkg}{Colors.RESET}\n")
                    
                    time.sleep(0.3)
                
                print(f"{Colors.CYAN}{'─' * 60}{Colors.RESET}\n")
                
                if success_count == len(missing):
                    print(f"  {Colors.GREEN}{Colors.BRIGHT}✓ Installation complete!{Colors.RESET}\n")
                    input(f"  {Colors.DIM}Press Enter to verify...{Colors.RESET}")
                    return check_dependencies()
                else:
                    input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")
                    return False
            
            elif choice == "2":
                print(f"\n{Colors.RED}{'─' * 60}{Colors.RESET}\n")
                print(f"  {Colors.RED}{Colors.BRIGHT}⚠ WARNING ⚠{Colors.RESET}\n")
                print(f"  {Colors.RED}Some features may not work!{Colors.RESET}\n")
                
                confirm = input(f"  {Colors.YELLOW}Type 'CONTINUE': {Colors.RESET}").strip()
                if confirm.upper() == 'CONTINUE':
                    print(f"\n  {Colors.YELLOW}⚠ Limited mode{Colors.RESET}\n")
                    time.sleep(1.5)
                    return False
                else:
                    print(f"\n  {Colors.GREEN}✓ Good choice!{Colors.RESET}\n")
                    sys.exit(0)
            else:
                print(f"  {Colors.RED}Invalid! Enter 1 or 2{Colors.RESET}")
        
        except KeyboardInterrupt:
            print(f"\n\n  {Colors.RED}Cancelled{Colors.RESET}\n")
            sys.exit(0)

def show_banner():
    """Show banner"""
    clear()
    
    print(f"""
{Colors.CYAN}{Colors.BRIGHT}
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ████████╗███████╗███╗   ██╗████████╗ ██████╗ ██████╗   ║
    ║   ╚══██╔══╝██╔════╝████╗  ██║╚══██╔══╝██╔═══██╗██╔══██╗  ║
    ║      ██║   █████╗  ██╔██╗ ██║   ██║   ██║   ██║██████╔╝  ║
    ║      ██║   ██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██╔══██╗  ║
    ║      ██║   ███████╗██║ ╚████║   ██║   ╚██████╔╝██║  ██║  ║
    ║      ╚═╝   ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝  ║
    ║                                                           ║
    ║         ████████╗███████╗ █████╗ ███╗   ███╗             ║
    ║         ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║             ║
    ║            ██║   █████╗  ███████║██╔████╔██║             ║
    ║            ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║             ║
    ║            ██║   ███████╗██║  ██║██║ ╚═╝ ██║             ║
    ║            ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝             ║
    ║                                                           ║
    ║              Credit by: Nguyễn Thanh Trứ                  ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
{Colors.RESET}
    """)
    
    loading_bar("Booting system", 1.5)
    
    print(f"\n  {Colors.GREEN}{Colors.BRIGHT}>>> SYSTEM ONLINE <<<{Colors.RESET}\n")
    time.sleep(0.8)

def show_menu():
    """Show main menu"""
    clear()
    
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BRIGHT}  ║         🔥 TENTOR TEAM CONTROL CENTER 🔥           ║{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    print(f"  {Colors.GREEN}[1]{Colors.RESET} 🌧️  Matrix Digital Rain")
    print(f"  {Colors.CYAN}{Colors.BRIGHT}[2]{Colors.RESET} 💰 Crypto Tracker [REAL-TIME]")
    print(f"  {Colors.GREEN}[3]{Colors.RESET} 🔐 Password Generator")
    print(f"  {Colors.GREEN}[4]{Colors.RESET} 🌈 Rainbow Text Effect")
    print(f"  {Colors.GREEN}[5]{Colors.RESET} 🚀 Rocket Launch")
    print(f"  {Colors.GREEN}[6]{Colors.RESET} 🖥️  System Information")
    print(f"  {Colors.MAGENTA}{Colors.BRIGHT}[7]{Colors.RESET} 📥 Download Tools")
    print(f"  {Colors.RED}{Colors.BRIGHT}[8]{Colors.RESET} ❌ Exit")
    
    now = datetime.now().strftime("%H:%M:%S")
    print(f"\n  {Colors.DIM}Time: {now} | Status: {Colors.GREEN}ONLINE{Colors.RESET}")
    print(f"  {Colors.DIM}Credit: Nguyễn Thanh Trứ{Colors.RESET}\n")

def download_menu():
    """Download tools menu"""
    clear()
    
    print(f"\n{Colors.MAGENTA}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║            📥 DOWNLOAD TOOLS MENU 📥               ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    print(f"  {Colors.CYAN}{Colors.BRIGHT}[1]{Colors.RESET} Download XWorld Tool {Colors.DIM}(by CTOOL){Colors.RESET}")
    print(f"  {Colors.RED}{Colors.BRIGHT}[2]{Colors.RESET} Back to Main Menu\n")
    
    print(f"  {Colors.DIM}{'─' * 52}{Colors.RESET}\n")

def download_xworld():
    """Download XWorld tool"""
    clear()
    
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BRIGHT}  ║          🌍 XWORLD TOOL DOWNLOADER 🌍              ║{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    print(f"  {Colors.GREEN}►{Colors.RESET} Tool    : {Colors.CYAN}XWorld{Colors.RESET}")
    print(f"  {Colors.GREEN}►{Colors.RESET} Author  : {Colors.CYAN}CTOOL{Colors.RESET}")
    print(f"  {Colors.GREEN}►{Colors.RESET} File    : {Colors.CYAN}main-xw.py{Colors.RESET}\n")
    
    print(f"  {Colors.DIM}{'─' * 52}{Colors.RESET}\n")
    
    try:
        import requests
    except ImportError:
        print(f"  {Colors.RED}✗ 'requests' not installed{Colors.RESET}")
        print(f"  {Colors.YELLOW}Install: pip install requests{Colors.RESET}\n")
        input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")
        return
    
    loading_bar("Connecting", 1)
    
    url = "https://raw.githubusercontent.com/C-Dev7929/Tools/refs/heads/main/main-xw.py"
    filename = "main-xw.py"
    
    try:
        print(f"\n  {Colors.CYAN}► Downloading...{Colors.RESET}")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"  {Colors.GREEN}✓ Success!{Colors.RESET}\n")
            
            print(f"  {Colors.DIM}{'─' * 52}{Colors.RESET}\n")
            print(f"  {Colors.GREEN}►{Colors.RESET} Saved   : {Colors.CYAN}{filename}{Colors.RESET}")
            print(f"  {Colors.GREEN}►{Colors.RESET} Size    : {Colors.CYAN}{len(response.text):,} bytes{Colors.RESET}")
            print(f"  {Colors.GREEN}►{Colors.RESET} Path    : {Colors.CYAN}{os.path.abspath(filename)}{Colors.RESET}\n")
            
            print(f"  {Colors.YELLOW}Run:{Colors.RESET} {Colors.CYAN}python {filename}{Colors.RESET}\n")
        else:
            print(f"  {Colors.RED}✗ Failed (Code: {response.status_code}){Colors.RESET}\n")
    
    except Exception as e:
        print(f"  {Colors.RED}✗ Error: {str(e)[:40]}{Colors.RESET}\n")
    
    input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")

def feature_crypto():
    """Crypto tracker"""
    clear()
    
    print(f"\n{Colors.YELLOW}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BRIGHT}  ║        💰 CRYPTO TRACKER [LIVE] 💰                 ║{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    try:
        import requests
        has_requests = True
    except:
        has_requests = False
    
    if not has_requests:
        print(f"  {Colors.RED}✗ 'requests' not installed{Colors.RESET}")
        print(f"  {Colors.YELLOW}⚠ DEMO mode{Colors.RESET}\n")
        demo_mode = True
    else:
        loading_bar("Connecting to API", 1.5)
        
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
            print(f"  {Colors.GREEN}✓ Connected!{Colors.RESET}\n")
        except:
            demo_mode = True
            print(f"  {Colors.YELLOW}⚠ DEMO mode{Colors.RESET}\n")
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
    
    time.sleep(0.5)
    print(f"  {Colors.DIM}Press Ctrl+C to stop{Colors.RESET}\n")
    time.sleep(0.5)
    
    coins = ["BTC", "ETH", "BNB", "SOL", "ADA"]
    count = 0
    
    try:
        while True:
            if not demo_mode and count > 0 and count % 30 == 0:
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
            
            count += 1
            now = datetime.now().strftime("%H:%M:%S")
            mode = f"{Colors.RED}[DEMO]{Colors.RESET}" if demo_mode else f"{Colors.GREEN}[LIVE]{Colors.RESET}"
            
            print(f"  {Colors.CYAN}╔══════════════════════════════════════════════════╗{Colors.RESET}")
            print(f"  {Colors.CYAN}║{Colors.BRIGHT} MARKET {Colors.RESET}{mode} {Colors.DIM}{now}{Colors.RESET}                               {Colors.CYAN}║{Colors.RESET}")
            print(f"  {Colors.CYAN}╠══════════════════════════════════════════════════╣{Colors.RESET}")
            print(f"  {Colors.CYAN}║ {'COIN':^6} │ {'PRICE':^14} │ {'24H':^12} │ {'CHART':^6} ║{Colors.RESET}")
            print(f"  {Colors.CYAN}╠══════════════════════════════════════════════════╣{Colors.RESET}")
            
            for coin in coins:
                if demo_mode:
                    delta = random.uniform(-0.2, 0.2)
                    prices[coin]["change"] += delta
                    prices[coin]["price"] *= (1 + delta/100)
                
                price = prices[coin]["price"]
                change = prices[coin]["change"]
                
                color = Colors.GREEN if change > 0 else Colors.RED
                arrow = "▲" if change > 0 else "▼"
                
                chart_len = int(min(abs(change), 6))
                chart = "█" * chart_len
                
                if price >= 1000:
                    price_str = f"${price:>12,.2f}"
                else:
                    price_str = f"${price:>12,.4f}"
                
                change_str = f"{arrow} {abs(change):>4.2f}%"
                
                print(f"  {Colors.CYAN}║{Colors.BRIGHT} {coin:^6}{Colors.RESET} {Colors.CYAN}│{Colors.RESET} {price_str} {Colors.CYAN}│{Colors.RESET} {color}{change_str:^12}{Colors.RESET} {Colors.CYAN}│{Colors.RESET} {color}{chart:^6}{Colors.RESET} {Colors.CYAN}║{Colors.RESET}")
            
            print(f"  {Colors.CYAN}╚══════════════════════════════════════════════════╝{Colors.RESET}\n")
            
            time.sleep(1)
            
            # Clear screen
            for _ in range(11):
                print('\033[F\033[K', end='')
    
    except KeyboardInterrupt:
        print(f"\n\n  {Colors.GREEN}✓ Stopped{Colors.RESET}\n")
        time.sleep(1)

def feature_matrix():
    """Matrix rain"""
    clear()
    
    print(f"\n{Colors.GREEN}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BRIGHT}  ║            🌧️  MATRIX DIGITAL RAIN 🌧️              ║{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    loading_bar("Loading Matrix", 1.2)
    print(f"\n  {Colors.DIM}Press Ctrl+C to exit{Colors.RESET}\n")
    time.sleep(0.5)
    
    chars = "01アイウABCDEF"
    width = 54
    height = 18
    
    try:
        while True:
            for _ in range(height):
                line = "  " + "".join([
                    f"{Colors.BRIGHT if random.random() > 0.9 else ''}{Colors.GREEN}{random.choice(chars)}{Colors.RESET}"
                    for _ in range(width)
                ])
                print(line)
                time.sleep(0.04)
            
            for _ in range(height):
                print('\033[F\033[K', end='')
    
    except KeyboardInterrupt:
        print(f"\n\n  {Colors.GREEN}✓ Stopped{Colors.RESET}\n")
        time.sleep(1)

def feature_password():
    """Password generator"""
    clear()
    
    print(f"\n{Colors.MAGENTA}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║       🔐 QUANTUM PASSWORD GENERATOR 🔐             ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    loading_bar("Initializing", 1)
    print()
    
    import string
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    
    for i in range(5):
        password = ''.join(random.choice(chars) for _ in range(16))
        
        print(f"  {Colors.CYAN}[{i+1}]{Colors.RESET} ", end="", flush=True)
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.2)
        
        print(f"\r  {Colors.GREEN}[{i+1}]{Colors.RESET} {Colors.BRIGHT}{password}{Colors.RESET}")
        time.sleep(0.3)
    
    print(f"\n  {Colors.GREEN}✓ Complete{Colors.RESET}\n")
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
    
    loading_bar("Applying", 1)
    print()
    
    colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.MAGENTA]
    
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
    
    stages = ["Pre-launch", "Fuel loading", "Engine test", "Navigation", "Final prep"]
    
    for stage in stages:
        loading_bar(stage, 0.8)
        time.sleep(0.2)
    
    print(f"\n  {Colors.YELLOW}{Colors.BRIGHT}COUNTDOWN{Colors.RESET}\n")
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
    
    print(f"\n\n  {Colors.GREEN}✓ Success!{Colors.RESET}\n")
    input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")

def feature_sysinfo():
    """System information"""
    clear()
    
    try:
        import psutil
    except ImportError:
        print(f"\n  {Colors.RED}✗ 'psutil' not installed{Colors.RESET}")
        print(f"  {Colors.YELLOW}Install: pip install psutil{Colors.RESET}\n")
        input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")
        return
    
    print(f"\n{Colors.MAGENTA}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║          🖥️  SYSTEM INFORMATION 🖥️                 ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    loading_bar("Scanning", 1.5)
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
    try:
        usage = psutil.disk_usage('/')
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
        print(f"  {Colors.RED}✗ Network unavailable{Colors.RESET}\n")
    
    print(f"  {Colors.GREEN}{'─' * 52}{Colors.RESET}")
    print(f"  {Colors.GREEN}✓ Scan complete!{Colors.RESET}")
    print(f"  {Colors.GREEN}{'─' * 52}{Colors.RESET}\n")
    
    input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")

def main():
    """Main program"""
    try:
        # Check dependencies
        check_dependencies()
        
        # Show banner
        show_banner()
        
        # Main loop
        while True:
            show_menu()
            
            try:
                choice = input(f"  {Colors.CYAN}root@tentor:~# {Colors.RESET}").strip()
                
                if choice == "1":
                    feature_matrix()
                elif choice == "2":
                    feature_crypto()
                elif choice == "3":
                    feature_password()
                elif choice == "4":
                    feature_rainbow()
                elif choice == "5":
                    feature_rocket()
                elif choice == "6":
                    feature_sysinfo()
                elif choice == "7":
                    # Download tools menu
                    while True:
                        download_menu()
                        dl_choice = input(f"  {Colors.CYAN}Select [1-2]: {Colors.RESET}").strip()
                        
                        if dl_choice == "1":
                            download_xworld()
                        elif dl_choice == "2":
                            break
                        else:
                            print(f"  {Colors.RED}✗ Invalid!{Colors.RESET}")
                            time.sleep(1)
                elif choice == "8":
                    clear()
                    print(f"\n  {Colors.CYAN}Shutting down...{Colors.RESET}\n")
                    loading_bar("Disconnecting", 1)
                    print(f"\n  {Colors.GREEN}✓ Goodbye! 👋{Colors.RESET}\n")
                    break
                else:
                    print(f"  {Colors.RED}✗ Invalid option!{Colors.RESET}")
                    time.sleep(1)
            
            except KeyboardInterrupt:
                print(f"\n  {Colors.YELLOW}Use option 8 to exit{Colors.RESET}")
                time.sleep(1)
    
    except KeyboardInterrupt:
        clear()
        print(f"\n  {Colors.RED}✗ Shutdown{Colors.RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
