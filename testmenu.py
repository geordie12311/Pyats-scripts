from __future__ import division
import sys
import time
from rich import print as rprint

def add():
    print("this is option A")
def multiply():
    pass
def divide():
    pass
def multiply():
    pass
def quit():
    rprint("The menu will now wait...")
    time.sleep(2)
    sys.exit()

def menu():
    rprint("*****Main Menu*****")
    time.sleep(1)

choice = input("""
        A: Show version
        B: show IP interface brief
        C: Show Running Configuration
        Q: Quit programme

        Please make a selection from above menu
""")
if choice == "A" or choice == "a":
    import show_version
elif choice == "B" or choice == "b":
    import show_ip_intbrief
elif choice == "C" or choice == "c":
    import show_run
elif choice == "Q" or choice == "q":
    menu()
else:
    rprint("Error you must enter a valid option from the Menu")

menu