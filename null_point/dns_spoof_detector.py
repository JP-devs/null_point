from collections import defaultdict
from collections import defaultdict
import io
import contextlib
import dns.resolver
import argparse
import time
import sys
from null_point_theme import print_banner, print_success, print_error, print_input, print_info

def run_tool(args_str: str) -> str:
    """Callable function for the screen tool"""
    detector = DNSSpoofDetector()
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        # We need to parse args_str which is just the domain for now
        # If there are more args, this needs to be more robust
        domain = args_str.strip()
        if domain:
            detector.get_local_dns()
            detector.check_for_spoofing(domain)
            detector.print_summary()
        else:
            detector.run_tests()
    return f.getvalue()

class DNSSpoofDetector:
    def __init__(self):
        self.trusted_dns_servers = ['8.8.8.8', '1.1.1.1', '9.9.9.9', '208.67.222.222']
        self.local_dns_server = None
        self.results = defaultdict(list)
        self.test_domains = ['google.com', 'facebook.com', 'amazon.com', 'microsoft.com', 'youtube.com']
        self.detected_anomalies = 0

    def get_local_dns(self):
        """Get the local DNS server from system configuration or prompt user."""
        try:
            # Try to get from resolv.conf (Unix)
            import platform
            if platform.system() != 'Windows':
                with open('/etc/resolv.conf', 'r') as f:
                    for line in f:
                        if line.startswith('nameserver'):
                            self.local_dns_server = line.split()[1]
                            print_info(f"Detected local DNS server: {self.local_dns_server}")
                            return
        except Exception:
            pass
        
        try:
            # Try to get from ipconfig (Windows)
            import subprocess
            output = subprocess.check_output(['ipconfig', '/all']).decode('utf-8')
            for line in output.split('\n'):
                if 'DNS Servers' in line:
                    self.local_dns_server = line.split(':')[-1].strip()
                    print_info(f"Detected local DNS server: {self.local_dns_server}")
                    return
        except Exception:
            pass
        
        print_error("Could not detect local DNS server automatically")
        self.local_dns_server = print_input("Please enter your local DNS server IP: ").strip()

    def query_dns(self, server, domain, record_type='A'):
        """Query a DNS server for a specific record."""
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [server]
            resolver.lifetime = 2  
            answers = resolver.resolve(domain, record_type)
            return sorted([str(r) for r in answers])
        except Exception as e:
            print_error(f"Error querying {server} for {domain}: {e}")
            return None

    def check_for_spoofing(self, domain):
        """Check for DNS spoofing on a specific domain."""
        print_info(f"Testing domain: {domain}")
        
        trusted_responses = []
        for server in self.trusted_dns_servers:
            response = self.query_dns(server, domain)
            if response:
                trusted_responses.append(response)
                print_success(f"{server} response: {response}")
            time.sleep(0.5)  
        
        if not trusted_responses:
            print_error("Could not get responses from trusted servers")
            return
        
        consensus = max(set(tuple(r) for r in trusted_responses), 
                       key=lambda x: trusted_responses.count(list(x)))
        
        local_response = self.query_dns(self.local_dns_server, domain)
        if not local_response:
            print_error("Could not get response from local DNS server")
            return
        
        print_success(f"Local DNS ({self.local_dns_server}) response: {local_response}")
        
        if tuple(local_response) != consensus:
            print_error("POTENTIAL DNS SPOOFING DETECTED!")
            print(f"    Expected: {list(consensus)}")
            print(f"    Received: {local_response}")
            self.detected_anomalies += 1
            self.results[domain].append({
                'expected': list(consensus),
                'received': local_response,
                'server': self.local_dns_server
            })
        else:
            print_success("No spoofing detected for this domain")

    def run_tests(self):
        """Run DNS spoofing tests on all test domains."""
        if not self.local_dns_server:
            self.get_local_dns()
        
        print_info("Starting DNS spoofing detection tests...")
        for domain in self.test_domains:
            self.check_for_spoofing(domain)
            time.sleep(1)  
        
        self.print_summary()

    def print_summary(self):
        """Print summary of test results."""
        print_success("Test Summary:")
        print("="*50)
        print(f"Total domains tested: {len(self.test_domains)}")
        print(f"Potential spoofing cases detected: {self.detected_anomalies}")
        
        if self.detected_anomalies:
            print_error("Details of potential spoofing cases:")
            for domain, anomalies in self.results.items():
                for anomaly in anomalies:
                    print(f"\nDomain: {domain}")
                    print(f"DNS Server: {anomaly['server']}")
                    print(f"Expected IPs: {', '.join(anomaly['expected'])}")
                    print(f"Received IPs: {', '.join(anomaly['received'])}")
        
        print_info("Recommendations:")
        if self.detected_anomalies:
            print("- Your DNS responses appear to be manipulated")
            print("- Consider using a trusted DNS service like Google (8.8.8.8) or Cloudflare (1.1.1.1)")
            print("- Check your network for possible MITM attacks")
            print("- Use DNS-over-HTTPS or DNS-over-TLS for secure DNS resolution")
        else:
            print("- No DNS spoofing detected in your network")
            print("- For maximum security, consider using encrypted DNS protocols")

def main():
    parser = argparse.ArgumentParser(description='DNS Spoofing Detector Tool')
    parser.add_argument('-d', '--domain', help='Test a specific domain')
    parser.add_argument('-s', '--server', help='Specify a DNS server to test')
    
    args = parser.parse_args()
    
    print_banner('DNS Spoofing Detector')
    print("DNS Spoofing Detector Tool - For detecting DNS cache poisoning and spoofing attacks")
    print("="*90)
    print("DISCLAIMER: Use only for legitimate network monitoring and security testing.\n")
    
    detector = DNSSpoofDetector()
    
    if args.server:
        detector.local_dns_server = args.server
    
    if args.domain:
        if not detector.local_dns_server:
            detector.get_local_dns()
        detector.check_for_spoofing(args.domain)
        detector.print_summary()
    else:
        detector.run_tests()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"An error occurred: {e}")
        sys.exit(1)

