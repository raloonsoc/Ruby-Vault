from rich.console import Console
from rich.text import Text
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import track
from utils.sqlite import SQLite
from utils.title import Title
from utils.crypt import Crypt
import time


INSERT_DATA = "1"
EXIT = "2"

WELCOME_MESSAGE = """
# REQUIRES ADMIN PERMISSIONS
## Create a database

Now you can create your password database, choose a good password to remember to use.

"""
OPTIONS_MESSAGE = """
# Database

*Options:*
1. Insert credentials
2. Exit
"""

STEPS_MESSAGE = """
# Steps to introduce data

1. Create master password
2. Introduce the data
"""

class Create_Database():
    def __init__(self):
        self.console = Console()
        self.sqlite = SQLite()
        self.crypt = Crypt()
        self.console.clear()
        Title(self.console)
    
    def display_welcome_message(self):
        self.console.print(Panel(Markdown(WELCOME_MESSAGE)))

    def create_database(self):
        while True:
            database_name = Prompt.ask('Introduce name of database')
            if database_name.strip():
                break
            self.console.print(Text("Database name cannot be empty.", style='red'))
        try:
            database = self.sqlite.create_database(database_name)
            if database:
                self.console.print(Text(f'Database {database_name} has been created successfully.', style='green'))
                return True
            else:
                self.console.print(Text(f"Database {database_name} can't be created.", style='red'))
                return False
        except Exception as e:
            self.console.print(Text(f"Error creating database: {e}", style='red'))
            return False
        
    def get_user_options(self):

        self.console.print(Panel(Markdown(OPTIONS_MESSAGE)))
        return Prompt.ask("Enter your option:", choices=[INSERT_DATA, EXIT], default=INSERT_DATA)
    
    def create_master_password(self):
        self.console.print(Text("1. Create master password", style='bold cyan'))
        while True:
            master_password = Prompt.ask("Enter the master password", password=True)
            if Confirm.ask("Are you sure you have set this password?"):
                break
        salt, verifier = self.crypt.generate_master_password(master_password)
        self.sqlite.save_master_to_db(salt, verifier)
        for _ in track(range(20), description="Processing..."):
            time.sleep(0.1)
        self.console.print(Text("Master password created, remember it otherwise it will be impossible to access your database in the future.", style="bold green"))

    def insert_credentials(self):
        self.console.print(Text("2. Introduce the data", style='bold cyan'))
        index = 0
        while True:
            name = Prompt.ask(f"[{index}] Enter the name")
            password = Prompt.ask(f"[{index}] Enter the password", password=True)
            encrypted_password = self.crypt.encrypt(password)
            self.sqlite.insert_data(name, encrypted_password)
            for _ in track(range(5), description="Processing your data..."):
                time.sleep(0.1)
            self.console.print(Text('The information has been saved.', style='bold green'))
            if not Confirm.ask('Do you want to continue?', default=True):
                break
            index += 1

    def run(self):
        self.display_welcome_message()
        database = self.create_database()
        if database:
            option = self.get_user_options()
            if option == INSERT_DATA:
                self.console.print(Panel(Markdown(STEPS_MESSAGE)))
                self.create_master_password()
                self.insert_credentials()
            elif option == EXIT:
                self.console.print("[bold green]Exiting Ruby Vault. Goodbye![/bold green]")
            else:
                self.console.print("[bold red]Invalid option. Exiting...[/bold red]")