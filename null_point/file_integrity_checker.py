import hashlib
import os
import shlex
import argparse
import sys

def generate_checksum(file_path, algorithm='sha256'):
    """Generate a checksum for a given file."""
    try:
        hash_func = getattr(hashlib, algorithm)()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest(), None
    except Exception as e:
        return None, f"Error generating hash for {file_path}: {e}"

def save_checksums(directory, output_file, algorithm='sha256'):
    """Generate and save checksums for all files in a directory."""
    output = []
    output.append(f"Generating checksums for files in: {directory}")
    try:
        with open(output_file, 'w') as f:
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    checksum, error = generate_checksum(file_path, algorithm)
                    if checksum:
                        f.write(f"{file_path}:{checksum}\n")
                    elif error:
                        output.append(error)
        output.append(f"Checksums saved to: {output_file}")
    except Exception as e:
        output.append(f"Error saving checksums: {e}")
    return "\n".join(output)

def load_checksums(checksum_file):
    """Load checksums from a file."""
    checksums = {}
    try:
        with open(checksum_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    checksums[parts[0]] = parts[1]
    except Exception as e:
        return None, f"Error loading checksums: {e}"
    return checksums, None

def verify_directory(directory, checksum_file, algorithm='sha256'):
    """Verify the integrity of files in a directory against a checksum file."""
    output = []
    output.append(f"Verifying integrity for files in: {directory}")
    checksums, error = load_checksums(checksum_file)
    if error:
        output.append(error)
        return "\n".join(output)
    
    if not checksums:
        output.append("No checksums loaded.")
        return "\n".join(output)

    for file_path, stored_checksum in checksums.items():
        if not os.path.exists(file_path):
            output.append(f"File not found: {file_path}")
            continue
            
        current_checksum, error = generate_checksum(file_path, algorithm)
        if error:
            output.append(error)
            continue
            
        if current_checksum != stored_checksum:
            output.append(f"Integrity check failed for: {file_path}")
        else:
            output.append(f"Integrity check passed for: {file_path}")
    return "\n".join(output)

def run_tool(args_str):
    """Run the tool with the provided arguments."""
    parser = argparse.ArgumentParser(description='File Integrity Checker', exit_on_error=False)
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate checksums for a directory')
    gen_parser.add_argument('directory', help='Directory to scan')
    gen_parser.add_argument('-o', '--output', default='checksums.txt', help='Output file')

    # Verify command
    ver_parser = subparsers.add_parser('verify', help='Verify directory integrity')
    ver_parser.add_argument('directory', help='Directory to verify')
    ver_parser.add_argument('-c', '--checksums', default='checksums.txt', help='Checksum file')

    try:
        args = parser.parse_args(shlex.split(args_str))
        if args.command == 'generate':
            return save_checksums(args.directory, args.output)
        elif args.command == 'verify':
            return verify_directory(args.directory, args.checksums)
        else:
            return "Invalid command. Usage: generate <dir> | verify <dir>"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Keeping the original main for compatibility, but updated to use run_tool logic if possible
    # Actually, for now, let's keep it separate or just call run_tool with sys.argv[1:]
    # For now, I'll just keep it simple.
    print(run_tool(" ".join(sys.argv[1:])))
