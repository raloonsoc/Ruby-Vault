from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from utils.sqlite import SQLite
from utils.crypt import Crypt
from utils.title import Title
import os
import sys

DATABASES_FOLDER = './databases'

WELCOME_MESSAGE = """
# REQUIRES ADMIN PERMISSIONS
## Access a database

Select the database

"""
class Access_Database():
    def __init__(self):
        self.console = Console()
        self.sqlite = SQLite()
        self.console.clear()
        self.crypt = Crypt()
        Title(self.console)
    
    def display_welcome_message(self):
        self.console.print(Panel(Markdown(WELCOME_MESSAGE)))

    def check_databases_folder(self):
        if not os.path.exists(DATABASES_FOLDER):
            self.console.print(Text("Folder databases not found, first create a database in the main menu.", style='red'))
            sys.exit(0)
    
    def get_databases(self):
        databases = [f for f in os.listdir(DATABASES_FOLDER) if f.endswith('.db')]
        if not databases:
            self.console.print(Text("No databases found in the folder, first create a database in the main menu.", style='red'))
            sys.exit(0)
        return databases
    def display_databases(self, databases):
        table_db = Table(title="Available Databases")
        table_db.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table_db.add_column("Database Name", justify="center", style="green", no_wrap=True)
        for idx, db_name in enumerate(databases, start=1):
            table_db.add_row(str(idx), db_name)

        self.console.print(table_db)
        
    def select_database(self, databases):
        while True:
            try:
                opt_db = int(Prompt.ask('Enter the number of the database')) - 1
                if 0 <= opt_db < len(databases):
                    return databases[opt_db].replace('.db', '')
                self.console.print(Text("Invalid selection. Please try again.", style='red'))
            except ValueError:
                self.console.print(Text("Please enter a valid number.", style='red'))
    
    def connect_to_database(self, selected_database):
        try:
            self.sqlite.connect_database(selected_database)
            self.console.print(Text(f'{selected_database} is selected', style='cyan'))
            return True
        except Exception as e:
            self.console.print(Text(f"Error connecting to database: {e}", style='red'))
            return False
        
    def verify_master_password(self, max_attempts=3):
        self.console.print(Text('You have 3 attempts to introduce the master password', style='bold medium_purple'))
        salt, verifier = self.sqlite.get_master_from_db()
        for attempt in range(max_attempts):
            password = Prompt.ask(f'[{attempt + 1}] Enter the master password', password=True)
            if self.crypt.load_key(password, salt, verifier):
                self.console.print(Text('Master password is correct', style='bold green'))
                break
            self.console.print(Text('Master password is not correct', style='bold red'))
        self.console.print(Text('Maximum attempts reached. Exiting...', style='bold red'))
        return False
    
    def display_database_data(self, selected_database):
        view_data = self.sqlite.view_data()
        table = Table(title=f"{selected_database}'s data")
        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("NAME", justify="center", style="green", no_wrap=True)
        if not view_data:
            self.console.print(Text("Actually this database don't have any information", style='red'))
        for id, name in view_data:
            table.add_row(str(id), name)
        self.console.print(table)

    def run(self):
        self.display_welcome_message()
        self.check_databases_folder()
        databases = self.get_databases()
        self.display_databases(databases)
        selected_database = self.select_database(databases)
        if self.connect_to_database(selected_database):
            if self.verify_master_password():
                self.display_database_data(selected_database)

