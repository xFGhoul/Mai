import os
import sys
import time

import yaml
import psutil
import subprocess

from inquirer import *
from download import download

from utils.console import console
from utils.ASCII import *

from timeit import default_timer as Timer

start = Timer()

console.print(
    """[cyan1]


    ███╗   ███╗ █████╗ ██╗    ██╗      █████╗ ██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗███████╗██████╗       ██╗██████╗ 
    ████╗ ████║██╔══██╗██║    ██║     ██╔══██╗██║   ██║████╗  ██║██╔════╝██║  ██║██╔════╝██╔══██╗     ██╔╝╚════██╗
    ██╔████╔██║███████║██║    ██║     ███████║██║   ██║██╔██╗ ██║██║     ███████║█████╗  ██████╔╝    ██╔╝  █████╔╝
    ██║╚██╔╝██║██╔══██║██║    ██║     ██╔══██║██║   ██║██║╚██╗██║██║     ██╔══██║██╔══╝  ██╔══██╗    ╚██╗  ╚═══██╗
    ██║ ╚═╝ ██║██║  ██║██║    ███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╗██║  ██║███████╗██║  ██║     ╚██╗██████╔╝
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝      ╚═╝╚═════╝ 
                                            VERSION: 1.0                                                                    
[/cyan1]"""
)

console.print(
    "\n[cyan1]WELCOME TO THE MAI LAUNCHER, MAI WILL NOW CHECK INSTALLATIONS AND FILES TO MAKE SURE THE BOT CAN RUN SMOOTHLY.[/cyan1]\n\n"
)

# System Check

console.print(
    "[cyan1]CHECKING OPERATING SYSTEM FOR COMPATIBILITY IN DEVELOPMENT.[/cyan1]\n"
)

if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
    time.sleep(2)
    os.system("cls")
    print_error()
    print_line()
    console.print("[red]THIS BOT CAN ONLY RUN ON WINDOWS.[/red]")
    time.sleep(5)
    raise SystemExit
else:
    console.print(
        f"[cyan1]OPERATING SYSTEM IS [red]{sys.platform}[/red] AND IS COMPATIBILE FORDEVELOPMENT.[/cyan1]\n"
    )

# REDIS

console.print("[cyan1]CHECKING IF REDIS IS RUNNING...[/cyan1]\n")

redis_running = "redis-server.exe" in (p.name() for p in psutil.process_iter())
if not redis_running:

    console.print("[red]REDIS NOT FOUND.[/red]\n")
    time.sleep(2)
    os.system("cls")
    print_error()
    print_line()

    console.print(
        "[cyan1]ATTEMPTING TO SEE IF REDIS IS INSTALLED AT [red]C:/Redis[/red].[/cyan1]\n"
    )
    if os.path.exists("C:/Redis"):
        console.print("[cyan1]FOUND REDIS AT [red]C:/Redis[/red].[/cyan1]\n")
        console.print("[cyan1]LAUNCHING REDIS...[/cyan1]\n")
        subprocess.Popen(
            ["cd", "C:/Redis"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            shell=True,
        )
        subprocess.Popen(
            ["redis-server"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            shell=True,
        )
        console.print("[cyan1]REDIS IS RUNNING AND FUNCTIONING[/cyan1]\n")
    else:
        question = [
            Confirm("redis", message="Should I Install(And Run) Redis?", default=True)
        ]
        answer = prompt(question)
        if answer:
            console.print("\n[cyan1]DOWNLOADING REDIS....[/cyan1]\n\n")
            redis_for_win_url = "https://github.com/microsoftarchive/redis/releases/download/win-3.2.100/Redis-x64-3.2.100.zip"
            download(
                redis_for_win_url,
                path="C:/Redis",
                kind="zip",
                progressbar=True,
                replace=True,
                verbose=False,
            )
            console.print(
                "\n[cyan1]REDIS HAS BEEN INSTALLED AND EXTRACTED TO [red]C:/Redis[/red].\n"
            )
            question = [
                Confirm(
                    "run_redis",
                    message="Should I Install(And Run) Redis?",
                    default=True,
                )
            ]
            answer = prompt(question)
            if answer:
                console.print("[cyan1]LAUNCHING REDIS...[/cyan1]\n")
                subprocess.Popen(
                    ["cd", "C:/Redis"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                    shell=True,
                )
                subprocess.Popen(
                    ["redis-server"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                    shell=True,
                )
                console.print("[cyan1]REDIS IS RUNNING AND FUNCTIONING[/cyan1]\n")
                time.sleep(2)
                os.system("cls")
            else:
                pass
        else:
            console.print(
                "[cyan1]USER DECIDED TO NOT INSTALL REDIS, THE BOT WILL FAIL AT STARTUP, I RECOMMEND YOU INSTALL.[/cyan1]"
            )
            raise SystemExit
else:
    console.print("[cyan1]REDIS IS INSTALLED AND RUNNING, CONTINUING....[/cyan1]\n")


# FILE CHECKS

console.print("[cyan1]CHECKING IF POETRY.LOCK EXISTS...[/cyan1]\n")

if not os.path.exists("poetry.lock"):
    time.sleep(2)
    os.system("cls")
    print_error()
    print_line()

    console.print(
        "[red]POETRY.LOCK NOT FOUND, ASSUMING NO POETRY PACKAGES HAVE BEEN INSTALLED, INSTALLING POETRY...[/red]\n"
    )
    subprocess.call(
        ["pip", "install", "poetry"],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    console.print(f"[red]POETRY INSTALLED, INSTALLING PACKAGES...[/red]\n")
    subprocess.call(
        ["poetry", "install"],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    console.print(f"[red]INSTALLED POETRY PACKAGES AND ACTIVATED VIRUAL ENV.[/red]\n")
    time.sleep(2)
    os.system("cls")
else:
    console.print(f"[cyan1]POETRY INSTALLED AND PACKAGES ARE UPDATED.[/cyan1]\n")

console.print("[cyan1]CHECKING IF CONFIG.YAML EXISTS...[/cyan1]\n")


if not os.path.exists("config/config.yaml"):
    console.print("[red]COFNIG FILE NOT FOUND.[/red]\n")
    time.sleep(2)
    os.system("cls")
    print_error()
    print_line()

    console.print("[cyan1]STARTING CONFIG GENERATOR....[/cyan1]\n")

    conf = {
        "DISCORD_TOKEN": "",
        "DISCORD_ID": "",
        "DATABASE_URI": "",
        "REDIS_URI": "",
    }

    if (
        str(
            console.input(
                "[cyan1]Would You Like To Enter Config Values Now?[/cyan1] ",
                markup=True,
            )
        ).lower()
        == "y"
        or "yes"
        or "Y"
        or "Yes"
    ):
        for key in conf.keys():
            conf[key] = console.input(
                f"\n[cyan1]Please enter the desired value for key '{key}': [/cyan1]",
                markup=True,
            )

    with open("config/config.yaml", "w+") as f:
        console.print("[cyan1]DUMPING DATA TO CONFIG.YAML[/cyan1]")
        yaml.dump(conf, f, yaml.Dumper)
        console.print("[cyan1]DATA DUMPED.[/cyan1]")
        time.sleep(2)
        os.system("cls")
else:
    console.print("[cyan1]CONFIG FILE EXISTS, CONTINUING....[/cyan1]\n")


console.print("[cyan1]CHECKING FOR AERICH.INI (TORTOISE)...[/cyan1]\n")

if not os.path.exists("aerich.ini"):
    console.print("[red]DATABASE DATA NOT FOUND[/red]\n")
    time.sleep(2)
    os.system("cls")
    print_error()
    print_line()

    console.print("[cyan1]BUILDING DATABASE WITH CONFIG DATA.[/cyan]\n")
    subprocess.Popen(
        ["cd", "scripts"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        shell=True,
    )
    subprocess.call(
        ["build_database"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        shell=True,
    )
    console.print("[cyan1]DATABASE BUILT WITH CONFIG DATA.[/cyan1]")
    time.sleep(2)
    os.system("cls")
else:
    console.print("[cyan1]AERICH CONFIG FILE EXISTS, CONTINUING....[/cyan1]\n")


console.print("[cyan1]FINISHED ALL CHECKS, NOW RUNNING MAIN BOT...[/cyan1]\n")

end = Timer()

elasped = end - start

console.print(f"[cyan1]TOOK {elasped} seconds to complete.[/cyan1]\n")

try:
    time.sleep(3)
    os.system("cls")
    subprocess.call(["python", "mai.py"])
except Exception as e:
    time.sleep(2)
    os.system("cls")
    print_error()
    print_line()
    console.print(f"[red]BOT COULD NOT RUN, ERROR {e}[/red]")
    raise SystemExit
