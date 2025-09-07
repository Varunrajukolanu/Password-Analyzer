import argparse
import random
import os
from zxcvbn import zxcvbn

def load_common_passwords():
    """Loads a list of common passwords from a text file."""
    file_path = os.path.join(os.path.dirname(__file__), "common_passwords.txt")
    if not os.path.exists(file_path):
        print("Warning: 'common_passwords.txt' not found. Password analysis will not check against common leaks.")
        return []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f.readlines()]

def analyze_password(password, common_passwords=None):
    """
    Analyzes a password using the zxcvbn library and a common password list.
    Returns a boolean for strength and a message with the score and suggestions.
    """
    # First, let's see if the password is on the list of top leaked passwords.
    if common_passwords and password in common_passwords:
        return False, "This password is in the top leaked list. Very weak."

    # Now we'll use zxcvbn to check for common patterns.
    results = zxcvbn(password)
    zxcvbn_score = results['score'] # Score from 0 (very weak) to 4 (very strong)

    # Let's make the score easier to understand for users.
    scaled_score = (zxcvbn_score + 1) * 2
    feedback = ", ".join(results['feedback']['suggestions'])

    if scaled_score < 6:
        return False, f"Password is too weak. Score: {scaled_score}/10. Suggestions: {feedback}"
    
    return True, f"Password is strong and secure. Score: {scaled_score}/10."

def suggest_passwords(password):
    """Generates simple suggestions by adding random characters."""
    valid_chars = "!@#$%^&*1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    suggestions = []
    # Let's add three suggestions to give the user a few options.
    for _ in range(3):
        pos = random.randint(0, len(password))
        char = random.choice(valid_chars)
        new_pass = password[:pos] + char + password[pos:]
        suggestions.append(new_pass)
    return suggestions

def generate_custom_wordlist(name, date, pet, output_file="custom_wordlist.txt"):
    """
    Generates a wordlist based on personal information to test against.
    This list contains common, weak password patterns.
    """
    base_words = [
        name.lower(),
        date,
        pet.lower(),
    ]
    
    leetspeak_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
    variations = set()

    # Now let's generate all the different variations.
    for word in base_words:
        variations.add(word)
        variations.add(word.capitalize())
        
        leeted_word = "".join([leetspeak_map.get(char, char) for char in word])
        variations.add(leeted_word)
        
        for year in ["2024", "2025", "1999", "2000"]:
            variations.add(word + year)
            variations.add(leeted_word + year)

    with open(output_file, "w") as f:
        for word in sorted(list(variations)):
            f.write(word + "\n")
    print(f"Custom wordlist generated in '{output_file}'")

def batch_mode(input_file, report=False):
    """Analyzes a list of passwords from a file and optionally generates a report."""
    common_passwords = load_common_passwords()
    results = []
    try:
        with open(input_file, "r") as f:
            for line in f:
                pwd = line.strip()
                strong, msg = analyze_password(pwd, common_passwords)
                results.append((pwd, strong, msg))
        if report:
            with open("batch_report.txt", "w") as out:
                for pwd, strong, msg in results:
                    out.write(f"{pwd} -> {msg}\n")
        return results
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return []

def main():
    """Main function to parse arguments and run the password analyzer."""
    parser = argparse.ArgumentParser(description="Password Strength Analyzer")
    parser.add_argument("-p", "--password", help="Password to analyze.")
    parser.add_argument("--batch", help="File with list of passwords to analyze in batch mode.")
    parser.add_argument("--report", action="store_true", help="Generate a batch report file.")
    parser.add_argument("--generate_wordlist", action="store_true", help="Generate a custom wordlist from user inputs.")
    parser.add_argument("--name", help="User's name for wordlist generation.")
    parser.add_argument("--date", help="User's date of birth or a significant date.")
    parser.add_argument("--pet", help="User's pet name.")
    args = parser.parse_args()

    common_passwords = load_common_passwords()

    if args.password:
        strong, msg = analyze_password(args.password, common_passwords)
        print(f"Password: {args.password}")
        print(f"Analysis: {msg}")
        if not strong:
            print("Suggestions:")
            for s in suggest_passwords(args.password):
                print(f"  - {s}")

    elif args.batch:
        results = batch_mode(args.batch, args.report)
        for pwd, strong, msg in results:
            print(f"{pwd} -> {msg}")
        if args.report and results:
            print("Batch report saved as batch_report.txt")

    elif args.generate_wordlist:
        if not all([args.name, args.date, args.pet]):
            print("Error: --generate_wordlist requires --name, --date, and --pet.")
        else:
            generate_custom_wordlist(args.name, args.date, args.pet)
            
    else:
        print("Please provide an argument. Use -h or --help for options.")
        print("For example: python password_analyzer.py --password MyCoolPassword!")

if __name__ == "__main__":
    main()