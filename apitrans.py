import requests
import time
import sys
from colorama import init, Fore, Style

init(autoreset=True)

def print_header():
    print(Fore.CYAN + Style.BRIGHT + "=" * 80)
    print(Fore.MAGENTA + Style.BRIGHT + "          API SPAMMER TOOL".center(80))
    print(Fore.CYAN + Style.BRIGHT + "=" * 80)
    print()

def get_http_method():
    print(Fore.YELLOW + "Choose Method:")
    print("   1. POST")
    print("   2. GET")
    print("   3. PUT")
    print("   4. DELETE")
    print("   5. PATCH")
    print("   6. HEAD")
    print("   7. OPTIONS")
    
    while True:
        choice = input(Fore.YELLOW + "\nEnter choice (1-7): " + Style.RESET_ALL).strip()
        methods = {
            '1': 'POST', '2': 'GET', '3': 'PUT', '4': 'DELETE',
            '5': 'PATCH', '6': 'HEAD', '7': 'OPTIONS'
        }
        if choice in methods:
            return methods[choice]
        print(Fore.RED + "Invalid choice." + Style.RESET_ALL)

def main():
    print_header()
    api_url = input(Fore.YELLOW + "Enter the API URL: " + Style.RESET_ALL).strip()
    if not api_url.startswith("http"):
        print(Fore.RED + "error1: URL must start with http:// or https://" + Style.RESET_ALL)
        sys.exit(1)

    method = get_http_method()
    payload = None
    if method in ['POST', 'PUT', 'PATCH']:
        message = input(Fore.YELLOW + "Enter payload: " + Style.RESET_ALL).strip()
        if message:
            try:
                if message.startswith(('{', '[')):
                    payload = eval(message) if not isinstance(message, dict) else message
                else:
                    payload = {"data": message}
            except:
                payload = {"message": message}

    try:
        times = int(input(Fore.YELLOW + "Number of Times to Send it; " + Style.RESET_ALL))
        if times < 1:
            print(Fore.RED + "Number Must Be 1 or Over." + Style.RESET_ALL)
            sys.exit(1)
    except ValueError:
        print(Fore.RED + "Incorrect Number." + Style.RESET_ALL)
        sys.exit(1)

    delay_input = input(Fore.YELLOW + "Delay between requests in seconds (press Enter for default 1.3s every 5 requests): " + Style.RESET_ALL).strip()
    manual_delay = float(delay_input) if delay_input else 0

    custom_ua = input(Fore.YELLOW + "uAgent (leave blank for 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36' ): " + Style.RESET_ALL).strip()
    
    headers = {
        "User-Agent": custom_ua if custom_ua else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }

    print(Fore.CYAN + f"\nStarting {method} spam to: {api_url}" + Style.RESET_ALL)
    print(Fore.CYAN + "-" * 90 + Style.RESET_ALL)

    success_count = 0

    for i in range(1, times + 1):
        try:
            if method == 'GET':
                response = requests.get(api_url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(api_url, json=payload, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(api_url, json=payload, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(api_url, headers=headers, timeout=10)
            elif method == 'PATCH':
                response = requests.patch(api_url, json=payload, headers=headers, timeout=10)
            elif method == 'HEAD':
                response = requests.head(api_url, headers=headers, timeout=10)
            else:
                response = requests.options(api_url, headers=headers, timeout=10)

            if response.status_code in [200, 201, 202, 204]:
                status = f"{Fore.GREEN} | {Style.RESET_ALL}"
                msg = f"{Fore.GREEN}Success{Style.RESET_ALL}"
                success_count += 1
            else:
                status = f"{Fore.RED} | {Style.RESET_ALL}"
                msg = f"{Fore.RED}Failed{Style.RESET_ALL} | Status: {response.status_code}"

        except requests.exceptions.Timeout:
            status = f"{Fore.YELLOW}| ? |{Style.RESET_ALL}"
            msg = f"{Fore.YELLOW}Timeout{Style.RESET_ALL}"
        except requests.exceptions.ConnectionError:
            status = f"{Fore.RED} | {Style.RESET_ALL}"
            msg = f"{Fore.RED}Connection Failed{Style.RESET_ALL}"
        except Exception as e:
            status = f"{Fore.YELLOW}| ? |{Style.RESET_ALL}"
            msg = f"{Fore.YELLOW}Error: {str(e)[:60]}{Style.RESET_ALL}"

        progress = f"{i}/{times}"
        print(f"{status} {method:<6} | {api_url[:55]:<55} | {msg:<35} | {progress:>8}")
        if manual_delay > 0:
            time.sleep(manual_delay)
        else:
            if i % 5 == 0 and i != times:
                print(Fore.BLUE + f"   → Pausing 1.3s (every 5 requests)..." + Style.RESET_ALL)
                time.sleep(1.3)
    print(Fore.CYAN + "\n" + "=" * 90 + Style.RESET_ALL)
    print(Fore.GREEN + f"Complete. {success_count}/{times} | Method: {method}" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 90 + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nSpam stopped by user." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\nUnexpected error: {e}" + Style.RESET_ALL)
