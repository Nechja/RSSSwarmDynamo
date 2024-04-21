from rich.console import Console
from rich.text import Text
from rich import print
from rich.panel import Panel
import logging
import sys


class LoggerService:
    def __init__(self,console=True):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.handler = logging.StreamHandler()
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.console = Console()
        self.print = print

    def console(self, message):
        text = Text(message)
        text.stylize("bold cyan", 0, 6)
        self.console.print(text)

    def panel(self, message, title, border_style):
        text = Text(message)
        text.stylize("bold cyan", 0, 6)
        self.print(Panel.fit(text, title=title, border_style=border_style))

    def info(self, message):
        self.logger.info(message)
        text = Text(message)
        text.stylize("bold green", 0, 6)
        self.print(Panel.fit(text, title="Info", border_style="green"))
        
    def error(self, message):
        self.logger.error(message)
        text = Text(message)
        text.stylize("bold yellow", 0, 6)
        self.print(Panel.fit(text, title="Error", border_style="yellow"))

    def warning(self, message):
        self.logger.warning(message)
        text = Text(message)
        text.stylize("bold red", 0, 6)
        self.print(Panel.fit(text, title="Warning", border_style="red"))