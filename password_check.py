import csv
from pathlib import Path


def load_common_passwords(file_path):
    """
    Load a list of common passwords from a CSV file.

    :param file_path: path to the CSV file containing passwords (one per row)
    :return: set of common passwords or None if file not found
    """
    common_passwords = set()
    path = Path(file_path)

    if not path.is_file():
        print(f"Error: could not find file '{file_path}'")
        return None

    try:
        with path.open('r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    pw = row[0].strip()
                    if pw:
                        common_passwords.add(pw)
    except Exception as e:
        print(f"Error reading '{file_path}': {e}")
        return None

    return common_passwords


def estimate_crack_time(password, common_passwords):
    """
    Estimate the crack time for a password given attacker speeds.

    :param password: the password to test
    :param common_passwords: set of known common passwords
    :return: dict mapping attack tier to time in seconds or Instant
    """
    # Instant if password is too common
    if password in common_passwords:
        return {"Instant": True}

    # determine which character groups are used
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    # compute alphabet size
    char_size = 0
    if has_lower:
        char_size += 26
    if has_upper:
        char_size += 26
    if has_digit:
        char_size += 10
    if has_special:
        char_size += 32  # approximate special chars

    length = len(password)
    if length == 0 or char_size == 0:
        raise ValueError("Password must contain at least one valid character")

    # brute-force space
    total_combinations = char_size ** length

    # attacker tiers (hashes/sec)
    speeds = {
        "Basic (CPU)":     100_000_000,           # ~100 MH/s
        "Advanced (GPU)":  50_000_000_000,        # ~50 GH/s
        "High-End (ASIC)": 400_000_000_000_000,   # ~400 TH/s
    }

    results = {}
    for tier, rate in speeds.items():
        results[tier] = total_combinations / rate
    
    suggestions = []
    if length < 8:
        suggestions.append("Increase password length to at least 8 characters.")
    if not has_lower:
        suggestions.append("Add lowercase letters.")
    if not has_upper:
        suggestions.append("Add uppercase letters.")
    if not has_digit:
        suggestions.append("Include digits (0-9).")
    if not has_special:
        suggestions.append("Use special characters (e.g. !, @, #, $).")

    return results, suggestions


def display_results(password, results, suggestions):
    """
    Print human-friendly crack time estimates.

    :param password: the password tested
    :param results: dict from estimate_crack_time()
    """
    print(f"Password: {password}")
    print(f"Length: {len(password)}")

    if results.get("Instant"):
        print("Estimated Crack Time: Instant (common password)")
        return

    print("Estimated Crack Times:")
    for tier, secs in results.items():
        if secs < 60:
            time_str = "less than a minute"
        elif secs < 3600:
            time_str = f"{secs/60:.2f} minutes"
        elif secs < 86400:
            time_str = f"{secs/3600:.2f} hours"
        elif secs < 31536000:
            time_str = f"{secs/86400:.2f} days"
        else:
            time_str = f"{secs/31536000:.2f} years"

        print(f"- {tier}: {time_str}")
    
    if suggestions == []:
        print("\nYour password is strong.")
    else:
        print("\nSuggestions to improve password strength:")
        for suggestion in suggestions:
            print(f"- {suggestion}")


if __name__ == "__main__":
    common_passwords = load_common_passwords("common_passwords.csv")
    if not common_passwords:
        exit(1)

    pwd = input("Enter a password to check: ").strip()
    try:
        results, suggestions = estimate_crack_time(pwd, common_passwords)
        display_results(pwd, results, suggestions)
    except ValueError as ve:
        print(f"Error: {ve}")
