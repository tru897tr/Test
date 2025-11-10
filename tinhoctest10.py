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
    """Clear screen - safe"""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print('\n' * 50)

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def safe_print(text, end='\n'):
    """Safe print with error handling"""
    try:
        print(text, end=end, flush=True)
    except:
        try:
            print(text.encode('utf-8', errors='ignore').decode('utf-8'), end=end)
        except:
            pass

def safe_input(prompt):
    """Safe input with error handling"""
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        raise
    except:
        return ""

def loading_bar(text="Loading", duration=2):
    """Loading bar - ultra stable"""
    try:
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
            
            safe_print(f"\r  {color}[{bar}]{Colors.RESET} {percent}% {text}", end="")
            time.sleep(duration / width)
        
        safe_print(f"\r  {Colors.GREEN}[{'█' * width}]{Colors.RESET} 100% {text} ✓")
    except KeyboardInterrupt:
        safe_print(f"\n  {Colors.YELLOW}Interrupted{Colors.RESET}")
    except:
        safe_print(f"  Loading {text} complete")

def check_dependencies():
    """Check dependencies - never crash"""
    try:
        clear()
        
        safe_print(f"""
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
        
        safe_print(f"{Colors.YELLOW}  ► Scanning dependencies...{Colors.RESET}\n")
        time.sleep(0.5)
        
        missing = []
        
        for pkg, desc in required.items():
            safe_print(f"  {Colors.CYAN}[SCAN]{Colors.RESET} {pkg:<12} - ", end="")
            time.sleep(0.3)
            
            try:
                __import__(pkg)
                safe_print(f"{Colors.GREEN}✓ OK{Colors.RESET}      ({desc})")
            except:
                safe_print(f"{Colors.RED}✗ ERROR{Colors.RESET}   ({desc})")
                missing.append(pkg)
            
            time.sleep(0.2)
        
        safe_print(f"\n{Colors.CYAN}{'─' * 60}{Colors.RESET}\n")
        
        if not missing:
            safe_print(f"  {Colors.GREEN}{Colors.BRIGHT}✓ ALL DEPENDENCIES INSTALLED{Colors.RESET}")
            safe_print(f"  {Colors.GREEN}System ready!{Colors.RESET}\n")
            time.sleep(1.5)
            return True
        
        safe_print(f"  {Colors.RED}{Colors.BRIGHT}⚠ MISSING: {len(missing)} package(s){Colors.RESET}")
        safe_print(f"  {Colors.RED}Required: {', '.join(missing)}{Colors.RESET}\n")
        
        safe_print(f"{Colors.YELLOW}  ╔════════════════════════════════════════════════════════╗{Colors.RESET}")
        safe_print(f"{Colors.YELLOW}  ║  Would you like to install missing packages?          ║{Colors.RESET}")
        safe_print(f"{Colors.YELLOW}  ╠════════════════════════════════════════════════════════╣{Colors.RESET}")
        safe_print(f"{Colors.GREEN}  ║  [1] YES - Auto install (Recommended)                 ║{Colors.RESET}")
        safe_print(f"{Colors.RED}  ║  [2] NO  - Continue anyway  ⚠ HIGH RISK                ║{Colors.RESET}")
        safe_print(f"{Colors.YELLOW}  ╚════════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        while True:
            try:
                choice = safe_input(f"  {Colors.CYAN}Your choice [1/2]: {Colors.RESET}")
                
                if choice == "1":
                    safe_print(f"\n{Colors.CYAN}{'─' * 60}{Colors.RESET}\n")
                    safe_print(f"  {Colors.GREEN}► Starting installation...{Colors.RESET}\n")
                    time.sleep(0.5)
                    
                    for pkg in missing:
                        safe_print(f"  {Colors.CYAN}Installing {pkg}...{Colors.RESET}")
                        
                        try:
                            subprocess.check_call([
                                sys.executable, "-m", "pip", "install", pkg, "-q"
                            ], timeout=60)
                            safe_print(f"  {Colors.GREEN}✓ {pkg} installed!{Colors.RESET}\n")
                        except:
                            safe_print(f"  {Colors.RED}✗ Failed{Colors.RESET}\n")
                        
                        time.sleep(0.3)
                    
                    safe_print(f"{Colors.CYAN}{'─' * 60}{Colors.RESET}\n")
                    safe_input(f"  {Colors.DIM}Press Enter to verify...{Colors.RESET}")
                    return check_dependencies()
                
                elif choice == "2":
                    safe_print(f"\n{Colors.RED}{'─' * 60}{Colors.RESET}\n")
                    safe_print(f"  {Colors.RED}{Colors.BRIGHT}⚠ WARNING ⚠{Colors.RESET}\n")
                    
                    confirm = safe_input(f"  {Colors.YELLOW}Type 'CONTINUE': {Colors.RESET}")
                    if confirm.upper() == 'CONTINUE':
                        safe_print(f"\n  {Colors.YELLOW}⚠ Limited mode{Colors.RESET}\n")
                        time.sleep(1.5)
                        return False
                    else:
                        sys.exit(0)
                else:
                    safe_print(f"  {Colors.RED}Invalid!{Colors.RESET}")
            
            except KeyboardInterrupt:
                safe_print(f"\n\n  {Colors.RED}Cancelled{Colors.RESET}\n")
                sys.exit(0)
            except:
                safe_print(f"  {Colors.RED}Error occurred{Colors.RESET}")
    
    except:
        safe_print(f"\n  {Colors.RED}Check failed, continuing...{Colors.RESET}\n")
        time.sleep(1)
        return False

def show_banner():
    """Banner - never crash"""
    try:
        clear()
        
        safe_print(f"""
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
        
        safe_print(f"\n  {Colors.GREEN}{Colors.BRIGHT}>>> SYSTEM ONLINE <<<{Colors.RESET}\n")
        time.sleep(0.8)
    except:
        safe_print("\n  TENTOR TEAM - System Online\n")
        time.sleep(1)

def show_menu():
    """Menu - never crash"""
    try:
        clear()
        
        safe_print(f"\n{Colors.CYAN}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
        safe_print(f"{Colors.CYAN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.CYAN}{Colors.BRIGHT}  ║         🔥 TENTOR TEAM CONTROL CENTER 🔥           ║{Colors.RESET}")
        safe_print(f"{Colors.CYAN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.CYAN}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        safe_print(f"  {Colors.GREEN}[1]{Colors.RESET} 🌧️  Matrix Digital Rain")
        safe_print(f"  {Colors.CYAN}{Colors.BRIGHT}[2]{Colors.RESET} 💰 Crypto Tracker [REAL-TIME]")
        safe_print(f"  {Colors.GREEN}[3]{Colors.RESET} 🔐 Password Generator")
        safe_print(f"  {Colors.GREEN}[4]{Colors.RESET} 🌈 Rainbow Text Effect")
        safe_print(f"  {Colors.GREEN}[5]{Colors.RESET} 🚀 Rocket Launch")
        safe_print(f"  {Colors.GREEN}[6]{Colors.RESET} 🖥️  System Information [PC/Mobile]")
        safe_print(f"  {Colors.MAGENTA}{Colors.BRIGHT}[7]{Colors.RESET} 📥 Download Tools")
        safe_print(f"  {Colors.RED}{Colors.BRIGHT}[8]{Colors.RESET} ❌ Exit")
        
        now = datetime.now().strftime("%H:%M:%S")
        safe_print(f"\n  {Colors.DIM}Time: {now} | Status: {Colors.GREEN}ONLINE{Colors.RESET}")
        safe_print(f"  {Colors.DIM}Credit: Nguyễn Thanh Trứ{Colors.RESET}\n")
    except:
        safe_print("\n  Menu: [1-8]\n")

def detect_device_type():
    """Detect if device is PC or Mobile"""
    try:
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        # Check for Android (Termux)
        if os.path.exists('/data/data/com.termux'):
            return 'android'
        
        # Check for iOS
        if system == 'darwin' and ('iphone' in machine or 'ipad' in machine):
            return 'ios'
        
        # Check for Linux on ARM (possible mobile)
        if system == 'linux' and ('arm' in machine or 'aarch' in machine):
            # Additional check for Android
            try:
                with open('/proc/version', 'r') as f:
                    if 'android' in f.read().lower():
                        return 'android'
            except:
                pass
            return 'linux-arm'
        
        # Default: PC
        return 'pc'
    except:
        return 'unknown'

def check_root_status():
    """Check if Android device is rooted"""
    try:
        # Method 1: Check for su binary
        su_paths = ['/system/bin/su', '/system/xbin/su', '/sbin/su', '/su/bin/su']
        for path in su_paths:
            if os.path.exists(path):
                return True
        
        # Method 2: Try to execute su command
        try:
            result = subprocess.run(['su', '-c', 'id'], capture_output=True, timeout=2)
            if result.returncode == 0:
                return True
        except:
            pass
        
        # Method 3: Check for Magisk
        if os.path.exists('/data/adb/magisk'):
            return True
        
        return False
    except:
        return False

def get_mobile_info_unrooted():
    """Get Android info without root"""
    try:
        safe_print(f"  {Colors.CYAN}━━━ 📱 ANDROID DEVICE (UNROOTED) ━━━{Colors.RESET}\n")
        
        # Basic system info
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} System   : {Colors.CYAN}Android (Termux){Colors.RESET}")
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Machine  : {Colors.CYAN}{platform.machine()}{Colors.RESET}")
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Python   : {Colors.CYAN}{platform.python_version()}{Colors.RESET}\n")
        
        # Termux info
        try:
            result = subprocess.run(['getprop', 'ro.build.version.release'], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                safe_print(f"  {Colors.GREEN}►{Colors.RESET} Android  : {Colors.CYAN}{result.stdout.strip()}{Colors.RESET}")
        except:
            pass
        
        try:
            result = subprocess.run(['getprop', 'ro.product.model'], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                safe_print(f"  {Colors.GREEN}►{Colors.RESET} Model    : {Colors.CYAN}{result.stdout.strip()}{Colors.RESET}")
        except:
            pass
        
        try:
            result = subprocess.run(['getprop', 'ro.product.brand'], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                safe_print(f"  {Colors.GREEN}►{Colors.RESET} Brand    : {Colors.CYAN}{result.stdout.strip()}{Colors.RESET}\n")
        except:
            pass
        
        # Storage info
        safe_print(f"  {Colors.CYAN}━━━ 💾 STORAGE ━━━{Colors.RESET}\n")
        try:
            stat = os.statvfs('/')
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_bavail * stat.f_frsize
            used = total - free
            percent = (used / total) * 100
            
            def size(b):
                for u in ['B','KB','MB','GB','TB']:
                    if b < 1024: return f"{b:.2f} {u}"
                    b /= 1024
            
            safe_print(f"  {Colors.GREEN}►{Colors.RESET} Total    : {Colors.CYAN}{size(total)}{Colors.RESET}")
            safe_print(f"  {Colors.GREEN}►{Colors.RESET} Free     : {Colors.CYAN}{size(free)}{Colors.RESET}")
            
            color = Colors.RED if percent > 80 else Colors.YELLOW if percent > 50 else Colors.GREEN
            bar_len = int(percent / 2)
            bar = "█" * bar_len + "░" * (50 - bar_len)
            safe_print(f"  {Colors.GREEN}►{Colors.RESET} Usage    : [{color}{bar}{Colors.RESET}] {color}{percent:.1f}%{Colors.RESET}\n")
        except:
            safe_print(f"  {Colors.RED}✗ Storage info unavailable{Colors.RESET}\n")
        
        # Network
        safe_print(f"  {Colors.CYAN}━━━ 🌐 NETWORK ━━━{Colors.RESET}\n")
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            safe_print(f"  {Colors.GREEN}►{Colors.RESET} Hostname : {Colors.CYAN}{hostname}{Colors.RESET}")
            safe_print(f"  {Colors.GREEN}►{Colors.RESET} IP       : {Colors.CYAN}{ip}{Colors.RESET}\n")
        except:
            safe_print(f"  {Colors.RED}✗ Network unavailable{Colors.RESET}\n")
    
    except Exception as e:
        safe_print(f"  {Colors.RED}✗ Error: {str(e)[:30]}{Colors.RESET}\n")

def get_mobile_info_rooted():
    """Get Android info with root"""
    try:
        safe_print(f"  {Colors.CYAN}━━━ 📱 ANDROID DEVICE (ROOTED) 🔓 ━━━{Colors.RESET}\n")
        
        # Basic info
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} System   : {Colors.CYAN}Android (Rooted){Colors.RESET}")
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Machine  : {Colors.CYAN}{platform.machine()}{Colors.RESET}\n")
        
        # Device info with root access
        try:
            result = subprocess.run(['su', '-c', 'getprop ro.build.version.release'], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                safe_print(f"  {Colors.GREEN}►{Colors.RESET} Android  : {Colors.CYAN}{result.stdout.strip()}{Colors.RESET}")
        except:
            pass
        
        try:
            result = subprocess.run(['su', '-c', 'getprop ro.product.model'], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                safe_print(f"  {Colors.GREEN}►{Colors.RESET} Model    : {Colors.CYAN}{result.stdout.strip()}{Colors.RESET}")
        except:
            pass
        
        # CPU info with root
        safe_print(f"\n  {Colors.CYAN}━━━ ⚡ CPU (ROOT ACCESS) ━━━{Colors.RESET}\n")
        try:
            result = subprocess.run(['su', '-c', 'cat /proc/cpuinfo | grep "model name" | head -1'], 
                                  capture_output=True, text=True, timeout=2, shell=True)
            if result.returncode == 0 and result.stdout:
                cpu_info = result.stdout.split(':')[1].strip() if ':' in result.stdout else 'N/A'
                safe_print(f"  {Colors.GREEN}►{Colors.RESET} CPU      : {Colors.CYAN}{cpu_info}{Colors.RESET}")
        except:
            safe_print(f"  {Colors.YELLOW}►{Colors.RESET} CPU info unavailable")
        
        # Memory with root
        safe_print(f"\n  {Colors.CYAN}━━━ 🧠 MEMORY (ROOT ACCESS) ━━━{Colors.RESET}\n")
        try:
            result = subprocess.run(['su', '-c', 'free -m'], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                if len(lines) > 1:
                    mem_line = lines[1].split()
                    if len(mem_line) >= 3:
                        total = int(mem_line[1])
                        used = int(mem_line[2])
                        percent = (used / total) * 100
                        
                        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Total    : {Colors.CYAN}{total} MB{Colors.RESET}")
                        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Used     : {Colors.CYAN}{used} MB{Colors.RESET}")
                        
                        color = Colors.RED if percent > 80 else Colors.YELLOW if percent > 50 else Colors.GREEN
                        bar_len = int(percent / 2)
                        bar = "█" * bar_len + "░" * (50 - bar_len)
                        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Usage    : [{color}{bar}{Colors.RESET}] {color}{percent:.1f}%{Colors.RESET}\n")
        except:
            safe_print(f"  {Colors.RED}✗ Memory info unavailable{Colors.RESET}\n")
        
        # Root status
        safe_print(f"  {Colors.CYAN}━━━ 🔓 ROOT STATUS ━━━{Colors.RESET}\n")
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Status   : {Colors.GREEN}{Colors.BRIGHT}✓ ROOTED{Colors.RESET}")
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Superuser: {Colors.CYAN}Available{Colors.RESET}\n")
    
    except Exception as e:
        safe_print(f"  {Colors.RED}✗ Error: {str(e)[:30]}{Colors.RESET}\n")

def get_pc_info():
    """Get PC system info"""
    try:
        import psutil
    except:
        safe_print(f"  {Colors.RED}✗ 'psutil' not installed{Colors.RESET}")
        safe_print(f"  {Colors.YELLOW}Install: pip install psutil{Colors.RESET}\n")
        return
    
    try:
        # System
        safe_print(f"  {Colors.CYAN}━━━ 💻 SYSTEM (PC) ━━━{Colors.RESET}\n")
        uname = platform.uname()
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} OS       : {Colors.CYAN}{uname.system} {uname.release}{Colors.RESET}")
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Machine  : {Colors.CYAN}{uname.machine}{Colors.RESET}")
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Hostname : {Colors.CYAN}{uname.node}{Colors.RESET}\n")
        
        # CPU
        safe_print(f"  {Colors.CYAN}━━━ ⚡ CPU ━━━{Colors.RESET}\n")
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Cores    : {Colors.CYAN}{psutil.cpu_count(logical=False)} Physical, {psutil.cpu_count(logical=True)} Logical{Colors.RESET}")
        
        cpu = psutil.cpu_percent(interval=1)
        cpu_color = Colors.RED if cpu > 80 else Colors.YELLOW if cpu > 50 else Colors.GREEN
        cpu_bar = int(cpu / 2)
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Usage    : [{cpu_color}{'█' * cpu_bar}{'░' * (50 - cpu_bar)}{Colors.RESET}] {cpu_color}{cpu:.1f}%{Colors.RESET}\n")
        
        # Memory
        safe_print(f"  {Colors.CYAN}━━━ 🧠 MEMORY ━━━{Colors.RESET}\n")
        mem = psutil.virtual_memory()
        
        def size(b):
            for u in ['B','KB','MB','GB','TB']:
                if b < 1024: return f"{b:.2f} {u}"
                b /= 1024
        
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Total    : {Colors.CYAN}{size(mem.total)}{Colors.RESET}")
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Available: {Colors.CYAN}{size(mem.available)}{Colors.RESET}")
        
        mem_color = Colors.RED if mem.percent > 80 else Colors.YELLOW if mem.percent > 50 else Colors.GREEN
        mem_bar = int(mem.percent / 2)
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Usage    : [{mem_color}{'█' * mem_bar}{'░' * (50 - mem_bar)}{Colors.RESET}] {mem_color}{mem.percent:.1f}%{Colors.RESET}\n")
        
        # Disk
        safe_print(f"  {Colors.CYAN}━━━ 💾 DISK ━━━{Colors.RESET}\n")
        try:
            usage = psutil.disk_usage('/')
            safe_print(f"  {Colors.GREEN}►{Colors.RESET} Total    : {Colors.CYAN}{size(usage.total)}{Colors.RESET}")
            safe_print(f"  {Colors.GREEN}►{Colors.RESET} Free     : {Colors.CYAN}{size(usage.free)}{Colors.RESET}")
            
            disk_color = Colors.RED if usage.percent > 80 else Colors.YELLOW if usage.percent > 50 else Colors.GREEN
            disk_bar = int(usage.percent / 2)
            safe_print(f"  {Colors.GREEN}►{Colors.RESET} Usage    : [{disk_color}{'█' * disk_bar}{'░' * (50 - disk_bar)}{Colors.RESET}] {disk_color}{usage.percent:.1f}%{Colors.RESET}\n")
        except:
            safe_print(f"  {Colors.RED}✗ Disk info unavailable{Colors.RESET}\n")
        
        # Network
        safe_print(f"  {Colors.CYAN}━━━ 🌐 NETWORK ━━━{Colors.RESET}\n")
        hostname = socket.gethostname()
        try:
            ip = socket.gethostbyname(hostname)
            safe_print(f"  {Colors.GREEN}►{Colors.RESET} Hostname : {Colors.CYAN}{hostname}{Colors.RESET}")
            safe_print(f"  {Colors.GREEN}►{Colors.RESET} IP       : {Colors.CYAN}{ip}{Colors.RESET}\n")
        except:
            safe_print(f"  {Colors.RED}✗ Network unavailable{Colors.RESET}\n")
    
    except Exception as e:
        safe_print(f"  {Colors.RED}✗ Error: {str(e)[:30]}{Colors.RESET}\n")

def feature_sysinfo():
    """System information - PC or Mobile"""
    try:
        clear()
        
        safe_print(f"\n{Colors.MAGENTA}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
        safe_print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║          🖥️  SYSTEM INFORMATION 🖥️                 ║{Colors.RESET}")
        safe_print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        loading_bar("Detecting device type", 1)
        
        device_type = detect_device_type()
        
        safe_print(f"\n  {Colors.YELLOW}► Device Type: {Colors.CYAN}{Colors.BRIGHT}{device_type.upper()}{Colors.RESET}\n")
        time.sleep(0.5)
        
        if device_type == 'android':
            loading_bar("Checking root status", 1)
            is_rooted = check_root_status()
            
            safe_print(f"\n  {Colors.YELLOW}► Root Status: ", end="")
            if is_rooted:
                safe_print(f"{Colors.GREEN}{Colors.BRIGHT}✓ ROOTED{Colors.RESET}\n")
            else:
                safe_print(f"{Colors.RED}✗ NOT ROOTED{Colors.RESET}\n")
            
            time.sleep(0.5)
            loading_bar("Gathering device info", 1.5)
            safe_print()
            
            if is_rooted:
                get_mobile_info_rooted()
            else:
                get_mobile_info_unrooted()
        
        elif device_type == 'ios':
            safe_print(f"  {Colors.CYAN}━━━ 📱 iOS DEVICE ━━━{Colors.RESET}\n")
            safe_print(f"  {Colors.YELLOW}⚠ iOS limited access{Colors.RESET}")
            safe_print(f"  {Colors.GREEN}►{Colors.RESET} System   : {Colors.CYAN}iOS{Colors.RESET}")
            safe_print(f"  {Colors.GREEN}►{Colors.RESET} Machine  : {Colors.CYAN}{platform.machine()}{Colors.RESET}\n")
        
        else:
            loading_bar("Scanning system", 1.5)
            safe_print()
            get_pc_info()
        
        safe_print(f"  {Colors.GREEN}{'─' * 52}{Colors.RESET}")
        safe_print(f"  {Colors.GREEN}✓ Scan complete!{Colors.RESET}")
        safe_print(f"  {Colors.GREEN}{'─' * 52}{Colors.RESET}\n")
        
        safe_input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")
    
    except KeyboardInterrupt:
        safe_print(f"\n\n  {Colors.YELLOW}Interrupted{Colors.RESET}\n")
        time.sleep(1)
    except Exception as e:
        safe_print(f"\n  {Colors.RED}✗ Error occurred{Colors.RESET}\n")
        time.sleep(1)

def download_menu():
    """Download menu - never crash"""
    try:
        clear()
        
        safe_print(f"\n{Colors.MAGENTA}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
        safe_print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║            📥 DOWNLOAD TOOLS MENU 📥               ║{Colors.RESET}")
        safe_print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        safe_print(f"  {Colors.CYAN}{Colors.BRIGHT}[1]{Colors.RESET} Download XWorld Tool {Colors.DIM}(by CTOOL){Colors.RESET}")
        safe_print(f"  {Colors.RED}{Colors.BRIGHT}[2]{Colors.RESET} Back to Main Menu\n")
        
        safe_print(f"  {Colors.DIM}{'─' * 52}{Colors.RESET}\n")
    except:
        safe_print("\n  Download Menu\n  [1] XWorld  [2] Back\n")

def download_xworld():
    """Download XWorld - never crash"""
    try:
        clear()
        
        safe_print(f"\n{Colors.CYAN}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
        safe_print(f"{Colors.CYAN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.CYAN}{Colors.BRIGHT}  ║          🌍 XWORLD TOOL DOWNLOADER 🌍              ║{Colors.RESET}")
        safe_print(f"{Colors.CYAN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.CYAN}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Tool    : {Colors.CYAN}XWorld{Colors.RESET}")
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} Author  : {Colors.CYAN}CTOOL{Colors.RESET}")
        safe_print(f"  {Colors.GREEN}►{Colors.RESET} File    : {Colors.CYAN}main-xw.py{Colors.RESET}\n")
        
        safe_print(f"  {Colors.DIM}{'─' * 52}{Colors.RESET}\n")
        
        try:
            import requests
        except:
            safe_print(f"  {Colors.RED}✗ 'requests' not installed{Colors.RESET}")
            safe_print(f"  {Colors.YELLOW}Install: pip install requests{Colors.RESET}\n")
            safe_input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")
            return
        
        loading_bar("Connecting", 1)
        
        url = "https://raw.githubusercontent.com/C-Dev7929/Tools/refs/heads/main/main-xw.py"
        filename = "main-xw.py"
        
        try:
            safe_print(f"\n  {Colors.CYAN}► Downloading...{Colors.RESET}")
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                safe_print(f"  {Colors.GREEN}✓ Success!{Colors.RESET}\n")
                
                safe_print(f"  {Colors.DIM}{'─' * 52}{Colors.RESET}\n")
                safe_print(f"  {Colors.GREEN}►{Colors.RESET} Saved   : {Colors.CYAN}{filename}{Colors.RESET}")
                safe_print(f"  {Colors.GREEN}►{Colors.RESET} Size    : {Colors.CYAN}{len(response.text):,} bytes{Colors.RESET}")
                safe_print(f"  {Colors.GREEN}►{Colors.RESET} Path    : {Colors.CYAN}{os.path.abspath(filename)}{Colors.RESET}\n")
                
                safe_print(f"  {Colors.YELLOW}Run:{Colors.RESET} {Colors.CYAN}python {filename}{Colors.RESET}\n")
            else:
                safe_print(f"  {Colors.RED}✗ Failed (Code: {response.status_code}){Colors.RESET}\n")
        
        except Exception as e:
            safe_print(f"  {Colors.RED}✗ Error: {str(e)[:40]}{Colors.RESET}\n")
        
        safe_input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")
    except:
        safe_print(f"\n  {Colors.RED}Download failed{Colors.RESET}\n")
        time.sleep(1)

def feature_crypto():
    """Crypto tracker - ultra stable"""
    try:
        clear()
        
        safe_print(f"\n{Colors.YELLOW}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
        safe_print(f"{Colors.YELLOW}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.YELLOW}{Colors.BRIGHT}  ║        💰 CRYPTO TRACKER [LIVE] 💰                 ║{Colors.RESET}")
        safe_print(f"{Colors.YELLOW}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.YELLOW}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        try:
            import requests
            has_requests = True
        except:
            has_requests = False
        
        if not has_requests:
            safe_print(f"  {Colors.RED}✗ 'requests' not installed{Colors.RESET}")
            safe_print(f"  {Colors.YELLOW}⚠ DEMO mode{Colors.RESET}\n")
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
                safe_print(f"  {Colors.GREEN}✓ Connected!{Colors.RESET}\n")
            except:
                demo_mode = True
                safe_print(f"  {Colors.YELLOW}⚠ DEMO mode{Colors.RESET}\n")
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
        safe_print(f"  {Colors.DIM}Press Ctrl+C to stop{Colors.RESET}\n")
        time.sleep(0.5)
        
        coins = ["BTC", "ETH", "BNB", "SOL", "ADA"]
        count = 0
        
        while True:
            try:
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
                
                safe_print(f"  {Colors.CYAN}╔══════════════════════════════════════════════════╗{Colors.RESET}")
                safe_print(f"  {Colors.CYAN}║{Colors.BRIGHT} MARKET {Colors.RESET}{mode} {Colors.DIM}{now}{Colors.RESET}                               {Colors.CYAN}║{Colors.RESET}")
                safe_print(f"  {Colors.CYAN}╠══════════════════════════════════════════════════╣{Colors.RESET}")
                safe_print(f"  {Colors.CYAN}║ {'COIN':^6} │ {'PRICE':^14} │ {'24H':^12} │ {'CHART':^6} ║{Colors.RESET}")
                safe_print(f"  {Colors.CYAN}╠══════════════════════════════════════════════════╣{Colors.RESET}")
                
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
                    
                    safe_print(f"  {Colors.CYAN}║{Colors.BRIGHT} {coin:^6}{Colors.RESET} {Colors.CYAN}│{Colors.RESET} {price_str} {Colors.CYAN}│{Colors.RESET} {color}{change_str:^12}{Colors.RESET} {Colors.CYAN}│{Colors.RESET} {color}{chart:^6}{Colors.RESET} {Colors.CYAN}║{Colors.RESET}")
                
                safe_print(f"  {Colors.CYAN}╚══════════════════════════════════════════════════╝{Colors.RESET}\n")
                
                time.sleep(1)
                
                # Clear with error handling
                try:
                    for _ in range(11):
                        safe_print('\033[F\033[K', end='')
                except:
                    pass
            
            except KeyboardInterrupt:
                raise
            except:
                time.sleep(1)
    
    except KeyboardInterrupt:
        safe_print(f"\n\n  {Colors.GREEN}✓ Stopped{Colors.RESET}\n")
        time.sleep(1)
    except:
        safe_print(f"\n  {Colors.RED}Error occurred{Colors.RESET}\n")
        time.sleep(1)

def feature_matrix():
    """Matrix - never crash"""
    try:
        clear()
        
        safe_print(f"\n{Colors.GREEN}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
        safe_print(f"{Colors.GREEN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.GREEN}{Colors.BRIGHT}  ║            🌧️  MATRIX DIGITAL RAIN 🌧️              ║{Colors.RESET}")
        safe_print(f"{Colors.GREEN}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.GREEN}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        loading_bar("Loading Matrix", 1.2)
        safe_print(f"\n  {Colors.DIM}Press Ctrl+C to exit{Colors.RESET}\n")
        time.sleep(0.5)
        
        chars = "01アイウABCDEF"
        width = 54
        height = 18
        
        while True:
            try:
                for _ in range(height):
                    line = "  " + "".join([
                        f"{Colors.BRIGHT if random.random() > 0.9 else ''}{Colors.GREEN}{random.choice(chars)}{Colors.RESET}"
                        for _ in range(width)
                    ])
                    safe_print(line)
                    time.sleep(0.04)
                
                try:
                    for _ in range(height):
                        safe_print('\033[F\033[K', end='')
                except:
                    clear()
            
            except KeyboardInterrupt:
                raise
            except:
                time.sleep(0.1)
    
    except KeyboardInterrupt:
        safe_print(f"\n\n  {Colors.GREEN}✓ Stopped{Colors.RESET}\n")
        time.sleep(1)

def feature_password():
    """Password generator - stable"""
    try:
        clear()
        
        safe_print(f"\n{Colors.MAGENTA}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
        safe_print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║       🔐 QUANTUM PASSWORD GENERATOR 🔐             ║{Colors.RESET}")
        safe_print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.MAGENTA}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        loading_bar("Initializing", 1)
        safe_print()
        
        import string
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        
        for i in range(5):
            password = ''.join(random.choice(chars) for _ in range(16))
            
            safe_print(f"  {Colors.CYAN}[{i+1}]{Colors.RESET} ", end="")
            for _ in range(3):
                safe_print(".", end="")
                time.sleep(0.2)
            
            safe_print(f"\r  {Colors.GREEN}[{i+1}]{Colors.RESET} {Colors.BRIGHT}{password}{Colors.RESET}")
            time.sleep(0.3)
        
        safe_print(f"\n  {Colors.GREEN}✓ Complete{Colors.RESET}\n")
        safe_input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")
    except:
        safe_print(f"\n  {Colors.RED}Error{Colors.RESET}\n")
        time.sleep(1)

def feature_rainbow():
    """Rainbow - stable"""
    try:
        clear()
        
        safe_print(f"\n{Colors.CYAN}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
        safe_print(f"{Colors.CYAN}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.CYAN}  ║           🌈 RAINBOW TEXT EFFECT 🌈                ║{Colors.RESET}")
        safe_print(f"{Colors.CYAN}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.CYAN}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        text = safe_input(f"  {Colors.CYAN}Enter text: {Colors.RESET}")
        safe_print()
        
        loading_bar("Applying", 1)
        safe_print()
        
        colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.MAGENTA]
        
        for round in range(20):
            result = "  "
            for i, char in enumerate(text):
                color = colors[(i + round) % len(colors)]
                result += f"{color}{Colors.BRIGHT}{char}{Colors.RESET}"
            
            safe_print(f"\r{result}", end="")
            time.sleep(0.08)
        
        safe_print(f"\n\n  {Colors.GREEN}✓ Complete{Colors.RESET}\n")
        safe_input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")
    except:
        safe_print(f"\n  {Colors.RED}Error{Colors.RESET}\n")
        time.sleep(1)

def feature_rocket():
    """Rocket - stable"""
    try:
        clear()
        
        safe_print(f"\n{Colors.RED}{Colors.BRIGHT}  ╔════════════════════════════════════════════════════╗{Colors.RESET}")
        safe_print(f"{Colors.RED}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.RED}{Colors.BRIGHT}  ║           🚀 ROCKET LAUNCH SEQUENCE 🚀             ║{Colors.RESET}")
        safe_print(f"{Colors.RED}{Colors.BRIGHT}  ║                                                    ║{Colors.RESET}")
        safe_print(f"{Colors.RED}{Colors.BRIGHT}  ╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        stages = ["Pre-launch", "Fuel loading", "Engine test", "Navigation", "Final prep"]
        
        for stage in stages:
            loading_bar(stage, 0.8)
            time.sleep(0.2)
        
        safe_print(f"\n  {Colors.YELLOW}{Colors.BRIGHT}COUNTDOWN{Colors.RESET}\n")
        time.sleep(0.5)
        
        for i in range(10, 0, -1):
            safe_print(f"\r  {Colors.RED}{Colors.BRIGHT}T-{i:02d}{Colors.RESET}", end="")
            time.sleep(0.5)
        
        safe_print(f"\n\n  {Colors.RED}{Colors.BRIGHT}🚀 LIFTOFF! 🚀{Colors.RESET}\n")
        
        frames = ["    🚀", "   🚀 ", "  🚀  ", " 🚀   ", "🚀    "]
        for _ in range(5):
            for frame in frames:
                safe_print(f"\r  {frame}", end="")
                time.sleep(0.08)
        
        safe_print(f"\n\n  {Colors.GREEN}✓ Success!{Colors.RESET}\n")
        safe_input(f"  {Colors.DIM}Press Enter...{Colors.RESET}")
    except:
        safe_print(f"\n  {Colors.RED}Error{Colors.RESET}\n")
        time.sleep(1)

def main():
    """Main - ultra stable"""
    try:
        # Check dependencies
        check_dependencies()
        
        # Show banner
        show_banner()
        
        # Main loop
        while True:
            try:
                show_menu()
                
                choice = safe_input(f"  {Colors.CYAN}root@tentor:~# {Colors.RESET}")
                
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
                    # Download menu
                    while True:
                        try:
                            download_menu()
                            dl_choice = safe_input(f"  {Colors.CYAN}Select [1-2]: {Colors.RESET}")
                            
                            if dl_choice == "1":
                                download_xworld()
                            elif dl_choice == "2":
                                break
                            else:
                                safe_print(f"  {Colors.RED}✗ Invalid!{Colors.RESET}")
                                time.sleep(1)
                        except KeyboardInterrupt:
                            break
                        except:
                            safe_print(f"  {Colors.RED}Error{Colors.RESET}")
                            time.sleep(1)
                elif choice == "8":
                    clear()
                    safe_print(f"\n  {Colors.CYAN}Shutting down...{Colors.RESET}\n")
                    loading_bar("Disconnecting", 1)
                    safe_print(f"\n  {Colors.GREEN}✓ Goodbye! 👋{Colors.RESET}\n")
                    break
                else:
                    safe_print(f"  {Colors.RED}✗ Invalid option!{Colors.RESET}")
                    time.sleep(1)
            
            except KeyboardInterrupt:
                safe_print(f"\n  {Colors.YELLOW}Use option 8 to exit{Colors.RESET}")
                time.sleep(1)
            except Exception as e:
                safe_print(f"  {Colors.RED}Error: Continuing...{Colors.RESET}")
                time.sleep(1)
    
    except KeyboardInterrupt:
        clear()
        safe_print(f"\n  {Colors.RED}✗ Shutdown{Colors.RESET}\n")
        sys.exit(0)
    except:
        safe_print(f"\n  {Colors.RED}Fatal error - Exiting{Colors.RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
