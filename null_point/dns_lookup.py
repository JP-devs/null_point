import dns.resolver
import socket
import sys
import argparse
import io
import contextlib
from null_point_theme import print_banner, print_success, print_error, print_input, print_info

from concurrent.futures import ThreadPoolExecutor

def get_dns_records(hostname: str):
    resolver = dns.resolver.Resolver()
    resolver.timeout = 2
    resolver.lifetime = 2
    
    records = ['A', 'AAAA', 'MX', 'NS', 'CNAME', 'TXT']
    results = {}
    
    def query_record(rtype):
        try:
            answers = resolver.resolve(hostname, rtype)
            return rtype, [rdata.to_text() for rdata in answers], None
        except (dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            return rtype, None, None
        except dns.resolver.NXDOMAIN:
            return "NXDOMAIN", None, "Hostname does not exist"
        except Exception as e:
            return rtype, None, str(e)

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(query_record, r) for r in records]
        for future in as_completed(futures):
            rtype, res, err = future.result()
            if rtype == "NXDOMAIN":
                return None
            if err:
                results[rtype] = f"Error: {err}"
            else:
                results[rtype] = res
                
    return results

def dns_lookup(hostname: str):
    results = get_dns_records(hostname)
    if results is None:
        print_error(f"Hostname {hostname} does not exist.")
        return

    print_info(f"DNS Records for {hostname}:")
    for rtype in ['A', 'AAAA', 'MX', 'NS', 'CNAME', 'TXT']:
        res = results.get(rtype)
        if res is None:
            print_info(f"No {rtype}-Records found.")
        elif isinstance(res, list):
            print_success(f"{rtype}-Records:")
            for rdata in res:
                print(f"- {rdata}")
        else:
            print_error(f"Error querying {rtype}: {res}")

def run_tool(hostname: str):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        dns_lookup(hostname)
    return buffer.getvalue()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modern DNS Lookup Tool")
    parser.add_argument("hostname", nargs='?', help="Hostname to lookup")
    args = parser.parse_args()

    print_banner("DNS Lookup Tool")

    hostname = args.hostname
    if not hostname:
        hostname = print_input("Please enter the hostname: ").strip()
        if not hostname:
            print_error("Hostname is required.")
            sys.exit(1)

    print(run_tool(hostname))
