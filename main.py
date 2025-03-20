from rich.console import Console
from rich.panel import Panel
from utils.title import Title
from rich.markdown import Markdown
from rich.prompt import Prompt
from modules.create_database import Create_Database
from modules.access_database import Access_Database
import sys

CREATE_DATABASE_OPTION = "1"
ACCESS_DATABASE_OPTION = "2"
EXIT_OPTION = "3"

def display_welcome_message(console):
    Title(console)
    options_markdown = """
# Welcome to Ruby Vault, this is a Password Manager built in Python

*Options:*
1. Create a password database.
2. Access to a database.
3. Exit


🖥️ Made by [Raúl Alonso](https://github.com/raloonsoc)
    """
    markdown = Markdown(options_markdown)
    console.print(Panel(markdown))

def get_user_option():
    return Prompt.ask("Enter your option:", choices=[CREATE_DATABASE_OPTION, ACCESS_DATABASE_OPTION, EXIT_OPTION], default=CREATE_DATABASE_OPTION)


def main():
    console = Console()

    try:
        display_welcome_message(console)

        option = get_user_option()

        if option == CREATE_DATABASE_OPTION:
            Create_Database().run()
        elif option == ACCESS_DATABASE_OPTION:
            Access_Database().run()
        elif option == EXIT_OPTION:
            console.print("[bold green]Exiting Ruby Vault. Goodbye![/bold green]")
            sys.exit(0)
        else:
            console.print("[bold red]Invalid option. Exiting...[/bold red]")
            sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
