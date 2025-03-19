import pyfiglet
from rich.text import Text

class Title():
    def __init__(self,console):
        self.font = pyfiglet.figlet_format("Ruby Vault", font="cosmic")
        console.print(Text(self.font, justify='left', style='bold red'))
