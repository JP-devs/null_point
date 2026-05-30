import os
import sys
import subprocess
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Header, Footer, Static, Tree, Label, Input
from textual.binding import Binding
import importlib
import inspect

# Add local directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Categorized tool list
TOOL_CATEGORIES = {
    "🌐 Network": {
        "Vulnerability": "website_vulnerability_scanner_screen",
        "Info Scanner": "website_info_scanner_screen",
        "Url Scanner": "website_url_scanner_screen",
        "IP Scanner": "ip_scanner_screen",
        "Port Scanner": "ip_port_scanner_screen",
        "IP Pinger": "ip_pinger_screen",
        "Traffic Analyzer": "network_traffic_analyzer_screen",
        "DNS Lookup": "dns_lookup_screen",
        "WHOIS Query": "whois_query_screen",
        "Subnet Calc": "subnet_calculator_screen"
    },
    "👁️ OSINT": {
        "Google Dorking": "google_dorking_screen",
        "User Tracker": "username_tracker_screen",
        "Email Tracker": "email_tracker_screen",
        "Email Lookup": "email_lookup_screen",
        "Phone Lookup": "phone_number_lookup_screen",
        "IP Lookup": "ip_lookup_screen",
        "Social Scanner": "social_media_scanner_screen",
        "Temp Mail": "tempmail_screen",
        "User Agent Gen": "user_agent_gen_screen"
    },
    "🛡️ Security": {
        "Phishing Sim": "phishing_simulator_screen",
        "Password Crack": "password_cracker_screen",
        "Hash Analyzer": "hash_analyzer_screen",
        "SQLi Tester": "sql_injection_tester_screen",
        "XSS Scanner": "xss_scanner_screen",
        "File Integrity": "file_integrity_checker_screen",
        "VPN Checker": "vpn_checker_screen",
        "Proxy Verifier": "proxy_verifier_screen",
        "MAC Spoofer": "mac_spoofer_screen",
        "DNS Spoof Det.": "dns_spoof_detector_screen"
    },
    "🕵️ Stealth & Privacy": {
        "IP Leak Test": "ip_leak_test_screen",
        "DNS Leak Test": "dns_leak_test_screen",
        "UA Rotator": "user_agent_rotator_screen"
    },
    "🛠️ Dev Tools": {
        "JSON Pretty": "json_pretty_print_screen",
        "JWT Decoder": "jwt_decoder_screen",
        "URL Enc/Dec": "url_encode_decode_screen"
    },
    "📊 Sys Monitor": {
        "Process Mem": "process_memory_usage_screen",
        "Disk Usage": "disk_usage_analyzer_screen",
        "Net Interface": "network_interface_stats_screen"
    },
    "🌐 Advanced Intel": {
        "Crt.sh Lookup": "crtsh_lookup_screen",
        "URL Expander": "url_expander_screen"
    },
    "🔍 Forensics": {
        "Image Meta": "image_meta_screen",
        "File Hex": "file_hex_viewer_screen",
        "Exif Rem": "exif_remover_screen",
        "String Ext": "string_extractor_screen",
        "PDF Meta": "pdf_meta_extractor_screen",
        "PCAP Analyz": "pcap_analyzer_screen"
    },
    "📁 File Systems": {
        "Hash Calc": "file_hash_calc_screen",
        "Duplicate Find": "duplicate_finder_screen",
        "Size Analyzer": "file_size_analyzer_screen"
    },
    "🌐 Web Analysis": {
        "Header Check": "http_header_checker_screen",
        "Robots Viewer": "robots_txt_viewer_screen",
        "Sitemap Parse": "sitemap_parser_screen"
    },
    "🛡️ System Hardening": {
        "Port Listen": "port_listener_check_screen",
        "Apps List": "installed_apps_list_screen",
        "Firewall Stat": "firewall_status_screen"
    },
    "🔐 Crypto": {
        "Base64 Tool": "base64_tool_screen",
        "AES Enc/Dec": "aes_enc_dec_screen",
        "RSA Key Gen": "rsa_key_gen_screen",
        "ROT13 Tool": "rot13_tool_screen",
        "XOR Cipher": "xor_cipher_screen",
        "Hash Cracker": "hash_cracker_screen"
    },
    "🛠️ Utils": {
        "Password Gen": "password_gen_screen",
        "UA Generator": "user_agent_gen_screen",
        "Sys Info": "sys_info_tool_screen",
        "Text to Bin": "text_to_binary_screen",
        "Unit Convert": "unit_converter_screen",
        "Clip Manager": "clipboard_mgr_screen",
        "File Renamer": "file_renamer_screen"
    },
    "📝 Text Utilities": {
        "Summarizer": "text_summarizer_screen",
        "Keyword Ext": "keyword_extractor_screen",
        "Chat Mock": "chat_mock_screen",
        "Sentiment": "sentiment_analysis_screen",
        "Translator": "text_translator_screen"
    },
    "⚙️ DevOps": {
        "S3 Scanner": "s3_scanner_screen",
        "Docker Lister": "docker_lister_screen",
        "SSH Key Gen": "ssh_key_gen_screen",
        "Env Checker": "env_var_checker_screen",
        "API Fuzzer": "api_fuzzer_screen"
    },
    "🎮 Games": {
        "Roblox Cookie": "roblox_cookie_info_screen",
        "Roblox ID": "roblox_id_info_screen",
        "Roblox User": "roblox_user_info_screen",
        "Server Scan": "game_server_scanner_screen",
        "Profile Analyzer": "player_profile_analyzer_screen",
        "Item Checker": "item_value_checker_screen",
        "Trade Tracker": "trade_history_tracker_screen",
        "Gun LoL Check": "gun_lol_checker_screen",
        "Aniworld Scan": "aniworld_scanner_screen",
        "TikTok OSINT": "tiktok_osint_screen",
        "Steam OSINT": "steam_osint_screen",
        "Valo OSINT": "valorant_osint_screen"
    }
}

class ToolApp(App):
    CSS_PATH = "theme.css"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("escape", "pop_screen", "Back"),
    ]

    def action_pop_screen(self) -> None:
        if len(self._screen_stack) > 1:
            self.pop_screen()

    def update_tree(self, search_text: str = "") -> None:
        tree = self.query_one("#tool_tree", Tree)
        # Remove all existing children of the root
        for child in list(tree.root.children):
            child.remove()
        
        tree.show_root = False
        expand = bool(search_text)
        for category, tools in TOOL_CATEGORIES.items():
            filtered_tools = {k: v for k, v in tools.items() if search_text.lower() in k.lower()}
            if filtered_tools:
                cat_node = tree.root.add(category, expand=expand)
                for tool_name, screen_id in filtered_tools.items():
                    cat_node.add_leaf(tool_name, data=screen_id)

    def on_mount(self) -> None:
        self.update_tree()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with ScrollableContainer(id="sidebar"):
                yield Label("Null Point Framework", id="sidebar-title")
                yield Input(placeholder="Search tools...", id="tool_search")
                yield Tree("", id="tool_tree")
            with Container(id="content"):
                yield Static("""
[bold cyan]Null Point Core Initialized[/]
-------------------------
[dim]Advanced OSINT & Security Engine[/]

Use the sidebar tree to select and execute tools.
                """, id="info")
        yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "tool_search":
            self.update_tree(event.value)

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        screen_id = event.node.data
        if screen_id:
            self.launch_tool(screen_id)

    def launch_tool(self, screen_id):
        try:
            module = importlib.import_module(f"screens.{screen_id}")
            
            screen_class = None
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__name__.endswith("Screen") and obj.__name__ != "Screen":
                    screen_class = obj
                    break
            
            if screen_class:
                self.push_screen(screen_class())
            else:
                self.query_one("#info", Static).update(f"[bold red]No Screen class found in {screen_id}[/]")
        except Exception as e:
            self.query_one("#info", Static).update(f"[bold red]Error launching {screen_id}:[/] {e}")

if __name__ == "__main__":
    app = ToolApp()
    app.run()
