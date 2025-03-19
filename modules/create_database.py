from rich.console import Console
from rich.text import Text
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import track
from utils.sqlite import SQLite
from utils.title import Title
from utils.crypt import Crypt
import time
import sys
class Create_Database():
    def __init__(self):
        console = Console()
        console.clear()
        sqlite = SQLite()
        crypt = Crypt()
        Title(console)
        markdown = """
# REQUIRES ADMIN PERMISSIONS
## Create a database

Now you can create your password database, choose a good password to remember to use.

"""
        console.print(Panel(Markdown(markdown)))
        database_name = Prompt.ask('Introduce name of database')
        database = sqlite.create_database(database_name)
        if database:
            console.print(Text(f'Database {database_name} has been created successfully.', style='green'))
            markdown_options = f"""
# Database *{database_name}*

*Options:*
1. Insert credentials
2. Exit
"""
            console.print(Panel(Markdown(markdown_options)))
            option = Prompt.ask("Enter your option:", choices=["1", "2"], default="1")
            if option == '1':
                steps_markdown = """
# Steps to introduce data

1. Create master password
2. Introduce the data
"""
                console.print(Panel(Markdown(steps_markdown)))
                console.print(Text("1. Create master password", style='bold cyan'))
                master_password = Prompt.ask("Enter the master password", password=True)
                confimation = Confirm.ask("Are you sure you have set this password?")
                if not confimation:
                    master_password = Prompt.ask("Enter the master password", password=True)
                salt = crypt.generate_master_password(master_password)
                sqlite.save_salt_to_db(salt)
                for i in track(range(20), description="Processing..."):
                    time.sleep(1)
                console.print(Text("Master password created, remember it otherwise it will be impossible to access your database in the future.", style="bold green"))
                console.print(Text("2. Introduce the data", style='bold cyan'))
                o = 'y'
                index = 0
                while o == 'y':
                    name = Prompt.ask(f"[{index}] Enter the name")
                    password = Prompt.ask(f"[{index}] Enter the password", password=True)
                    encrypted_password = crypt.encrypt(password)
                    sqlite.insert_data(name, encrypted_password)
                    for i in track(range(5), description="Processing your data..."):
                        time.sleep(1)
                    console.print(Text('The information has been saved.', style='bold green'))
                    response = Prompt.ask('Do you want to continue?', choices=['y','n'], default='y')
                    o = response
                    index += 1
                sys.exit(0)
            elif option == '2':
                sys.exit(0)
            else:
                sys.exit(0)
        else:
            console.print(Text(f"Database {database_name} can't be created.", style='red'))
            sys.exit(0)