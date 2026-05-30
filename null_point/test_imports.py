import importlib
import os
import sys

# Add root to sys.path
root_dir = r'D:\My-tools\Null-Point-Main\null_point'
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Categories from null_point.py (latest version)
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
},

failures = []
for cat, tools in TOOL_CATEGORIES.items():
    for name, screen_id in tools.items():
        try:
            importlib.import_module(f"screens.{screen_id}")
        except Exception as e:
            failures.append((screen_id, f"{type(e).__name__}: {str(e)}"))

if failures:
    print("FAILURES FOUND:")
    for sid, err in failures:
        print(f"{sid}: {err}")
    sys.exit(1)
else:
    print("ALL SCREENS IMPORTED SUCCESSFULLY")
    sys.exit(0)

