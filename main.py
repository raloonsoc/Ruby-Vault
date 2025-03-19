from rich.console import Console
from rich.panel import Panel
from utils.title import Title
from rich.markdown import Markdown
from rich.prompt import Prompt
from modules.create_database import Create_Database
from modules.access_database import Access_Database
import sys

if __name__ == "__main__":
    console = Console()
    Title(console)
    options_markdown = """
# Welcome to Ruby Vault, this is a Password Manager built in Python

*Options:*
1. Create a password database.
2. Access to a database.
3. Exit


🖥️ Made by [Raúl Alonso](https://github.com/raloonsoc)
    """
    mark = Markdown(options_markdown)
    main_panel = Panel(mark)
    console.print(main_panel)
    option = Prompt.ask("Enter your option:", choices=["1", "2", "3"], default="1")
    if option == '1':
        Create_Database()
    elif option == '2':
        Access_Database()
    elif option == '3':
        sys.exit(0)
    else:
        sys.exit(0)
