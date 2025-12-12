from datetime import datetime
from colorama import init, Fore, Back, Style            # type: ignore

autoreset=True

def my_info() -> None:
    name = "DeAnna Hoskins, Roland Carlisle, Michael Washington, Miguel Pena"
    school = "Justice Through Code @ Columbia University -- Capstone Project"
    proj_name = "Justice Navigator - Journal Companion"
    print(f"{Fore.WHITE}{"="*64}")
    print(f"\n{Fore.GREEN}{name}")
    print(f"{Fore.CYAN}{"="*13}{proj_name}{"="*14}")
    print(f"{Fore.YELLOW}{"*"*1}{school}{"*"*1}{Style.RESET_ALL}")

my_info()

def show_date() -> None:
    now = datetime.now()
    readable = now.strftime("%B %d, %Y at %I:%M:%S %p")
    print(f"{Fore.WHITE}{"="*16}{readable}{"="*16}\n")
    print(f"{Fore.WHITE}{"="*64}{Style.RESET_ALL}")

show_date()