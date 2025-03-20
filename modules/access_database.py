from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import track
from rich.prompt import Confirm
from rich.prompt import Prompt
from utils.sqlite import SQLite
from utils.crypt import Crypt
from utils.title import Title
import os
import sys
import time
import pyperclip

INSERT_CREDENTIALS = "1"
VIEW_DATA = "2"
GET_PASSWORD = "3"
EXIT = "4"
DELETE_DATABASE = "5"

DATABASES_FOLDER = './databases'

WELCOME_MESSAGE = """
# REQUIRES ADMIN PERMISSIONS
## Access a database

Select the database

"""

OPTIONS_MESSAGE = """
# Database

*Options:*
1. Insert credentials
2. View data
3. Get password
4. Exit
5. Delete database
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
                return True
            self.console.print(Text('Master password is not correct', style='bold red'))
        self.console.print(Text('Maximum attempts reached. Exiting...', style='bold red'))
        return False
    
    def get_user_option(self):
        self.console.print(Panel(Markdown(OPTIONS_MESSAGE)))
        return Prompt.ask("Enter your option:", choices=[INSERT_CREDENTIALS,VIEW_DATA,GET_PASSWORD,EXIT,DELETE_DATABASE], default=INSERT_CREDENTIALS)
    
    def insert_credentials(self):
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
    
    def get_password(self, selected_database):
        self.display_database_data(selected_database)
        choices= [str(id) for id, _ in self.sqlite.view_data()] 
        opt = int(Prompt.ask('Select the credential', choices=choices))
        try:
            encrypted_password = self.sqlite.get_password(opt)
            password = self.crypt.decrypt(encrypted_password)
            self.console.print(Text(f"Password: {password}", style='bold green'))
            pyperclip.copy(password)
            self.console.print(Text("Password copied to clipboard for 10 seconds.", style='bold cyan'))
            for _ in track(range(10), description="The clipboard password will be deleted..."):
                time.sleep(1)
            pyperclip.copy(" ")
            self.console.print(Text("Clipboard cleared.", style='bold yellow'))
            self.menu(selected_database)
        except Exception as e:
            self.console.print(Text(f"An error occurred while getting password from the database: {e}", style='bold red'))
            self.menu(selected_database)
    
    def menu(self, selected_database):
        option = self.get_user_option()
        if option == INSERT_CREDENTIALS:
            self.insert_credentials()
            self.sqlite.exit()
        elif option == VIEW_DATA:
            self.display_database_data(selected_database)
            self.sqlite.exit()
        elif option == GET_PASSWORD:
            self.get_password(selected_database)
        elif option == EXIT:
            self.sqlite.exit()
            self.console.print("[bold green]Exiting Ruby Vault. Goodbye![/bold green]")
        elif option == DELETE_DATABASE:
            self.delete_database(selected_database)
        else:
            self.sqlite.exit()
            self.console.print("[bold red]Invalid option. Exiting...[/bold red]")

    def delete_database(self, selected_database):
        if Confirm.ask(f'Are you sure you want to delete "{selected_database}"? (ALL DATA WILL BE REMOVED)'):
            try:
                if self.sqlite.delete_database(selected_database):
                    self.console.print(Text(f'The database "{selected_database}" has been successfully removed.', style='bold green'))
                else:
                    self.console.print(Text(f'The database "{selected_database}" could not be removed. Please check your admin permissions or try again.', style='bold red'))
                    self.menu(selected_database)
            except Exception as e:
                self.console.print(Text(f"An error occurred while removing the database: {e}", style='bold red'))
                self.menu(selected_database)
        else:
            self.console.print(Text("Database deletion canceled.", style='bold yellow'))
            self.menu(selected_database)
        
    def run(self):
        self.display_welcome_message()
        self.check_databases_folder()
        databases = self.get_databases()
        self.display_databases(databases)
        selected_database = self.select_database(databases)
        if self.connect_to_database(selected_database):
            if self.verify_master_password():
                self.menu(selected_database)


