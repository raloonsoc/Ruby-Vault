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

class Access_Database():
    def __init__(self):
        sqlite = SQLite()
        console = Console()
        console.clear()
        Title(console)
        markdown = """
# REQUIRES ADMIN PERMISSIONS
## Access a database

Select the database

"""
        console.print(Panel(Markdown(markdown)))
        databases_folder = './databases'
        if not os.path.exists(databases_folder):
            console.print(Text("Folder databases not found, first create a database in the main menu.", style='red'))
            sys.exit(0)
        databases = [f for f in os.listdir(databases_folder) if f.endswith('.db')]
        if not databases:
            console.print(Text("No databases found in the folder, first create a database in the main menu.", style='red'))
            sys.exit(0)
        table_db = Table(title="Available Databases")
        table_db.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table_db.add_column("Database Name", justify="center", style="green", no_wrap=True)
        for idx, db_name in enumerate(databases, start=1):
            table_db.add_row(str(idx), db_name)
        console.print(table_db)
        opt_db = int(Prompt.ask('Enter the number of the database')) - 1
        selected_db = databases[opt_db].replace('.db', '')
        sqlite.connect_database(selected_db)
        view_data = sqlite.view_data()
        table = Table(title=f"{selected_db}'s data")
        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("NAME", justify="center", style="green", no_wrap=True)
        if not view_data:
            console.print(Text("Actually this database don't have any information", style='red'))
        for id, name in view_data:
            table.add_row(str(id), name)
        console.print(table)