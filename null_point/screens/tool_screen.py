from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Button, Static, Label, RichLog
from textual.containers import Vertical, ScrollableContainer
from xss_scanner import run_tool as xss_run

class XssScannerScreen(Screen):
    CSS_PATH = "../theme.css"
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(classes="tool-container"):
            yield Label("XSS Scanner Tool", id="title")
            yield Input(placeholder="Enter URL (https://...)", id="input_field")
            yield Button("Run Scan", id="run_button")
            with ScrollableContainer(id="output-container"):
                yield Static("Results will appear here...", id="output_area")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run_button":
            val = self.query_one("#input_field", Input).value
            if val:
                output_area = self.query_one("#output_area", Static)
                output_area.update(f"[cyan]Scanning {val}...[/]")
                try:
                    result = xss_run(val)
                    output_area.update(result)
                except Exception as e:
                    output_area.update(f"[red]Error: {e}[/]")
