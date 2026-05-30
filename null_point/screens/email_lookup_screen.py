from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Button, Label, RichLog
from textual.containers import Vertical
import re
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from email_lookup import run_tool

def strip_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

class EmailLookupScreen(Screen):
    CSS_PATH = "../theme.css"
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("q", "app.quit", "Quit"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(classes="tool-container"):
            yield Label("Email Lookup", id="title")
            yield Input(placeholder="Enter email address...", id="input_field")
            yield Button("Run", id="run_button", variant="primary")
            yield Button("Clear", id="clear_button")
            yield RichLog(id="output_area", highlight=True, markup=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run_button":
            val = self.query_one("#input_field", Input).value
            if val:
                output_area = self.query_one("#output_area", RichLog)
                output_area.clear()
                try:
                    result = run_tool(val)
                    output_area.write(strip_ansi(result))
                except Exception as e:
                    output_area.write(f"[red]Error: {str(e)}[/]")
            else:
                self.query_one("#output_area", RichLog).write("[red]Error: Input required.[/]")
        elif event.button.id == "clear_button":
            self.query_one("#output_area", RichLog).clear()
