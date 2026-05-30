import io
import contextlib
import phonenumbers
from phonenumbers import geocoder, carrier

def phone_number_lookup(phone_number: str) -> None:
    """
    Performs a basic phone number lookup.
    """
    try:
        parsed_number = phonenumbers.parse(phone_number)
        print(f"[i] Analysis for Phone Number: {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        
        # Geographical Region
        region = geocoder.description_for_number(parsed_number, "en") 
        print(f"[i] Geographical Region: {region or 'Not found.'}")

        # Mobile network operator
        service_provider = carrier.name_for_number(parsed_number, "en")
        print(f"[i] Mobile Network Operator: {service_provider or 'Not found.'}")

        # Validity of the number
        if phonenumbers.is_valid_number(parsed_number):
            print("[+] The phone number is valid.")
        else:
            print("[!] The phone number is invalid.")

    except phonenumbers.NumberParseException as e:
        print(f"[!] Error parsing the phone number: {e}")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")

def run_tool(args_str: str) -> str:
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print(f"Null Point: Phone Number Lookup")
        phone_number_lookup(args_str)
    return f.getvalue()
