import time
import os
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def clear():
    """Clear screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_line():
    """Draw separator line"""
    print("    " + "─" * 60)

def draw_double_line():
    """Draw double separator line"""
    print("    " + "═" * 60)

def typewriter_effect(text, color="", delay=0.05):
    """Typewriter effect"""
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)

def draw_who_am_i():
    """Display 'who am i?' text - NO color"""
    text = "WHO AM I?"
    
    print("    ", end='')
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.08)
    print()

def draw_tentor_ascii():
    """Draw TENTOR ASCII art with purple color"""
    art = """    ████████╗███████╗███╗   ██╗████████╗ ██████╗ ██████╗ 
    ╚══██╔══╝██╔════╝████╗  ██║╚══██╔══╝██╔═══██╗██╔══██╗
       ██║   █████╗  ██╔██╗ ██║   ██║   ██║   ██║██████╔╝
       ██║   ██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██╔══██╗
       ██║   ███████╗██║ ╚████║   ██║   ╚██████╔╝██║  ██║
       ╚═╝   ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝"""
    
    lines = art.split('\n')
    for line in lines:
        print(Fore.MAGENTA + line)
        time.sleep(0.1)
    print(Style.RESET_ALL)

def main():
    clear()
    
    # Loading effect
    print("\n    Loading", end='', flush=True)
    for _ in range(5):
        time.sleep(0.3)
        print(".", end='', flush=True)
    print("\n")
    
    time.sleep(0.5)
    clear()
    
    print("\n")
    draw_double_line()
    print()
    
    # Display who am i? - NO color
    draw_who_am_i()
    print()
    
    draw_line()
    print()
    
    # Draw TENTOR with purple color
    draw_tentor_ascii()
    print()
    
    draw_line()
    print()
    
    # Credit with purple color
    print(Fore.MAGENTA + "              Credit by: Nguyen Thanh Tru" + Style.RESET_ALL)
    
    # Current time with purple color
    current_time = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
    print(Fore.MAGENTA + f"              Time: {current_time}" + Style.RESET_ALL)
    print()
    
    draw_double_line()
    print()
    
    print("    Press Enter to continue...")
    input()

if __name__ == "__main__":
    main()
