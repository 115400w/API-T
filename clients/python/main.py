import requests
import time
import sys
from colorama import init, Fore, Style
init(autoreset=True)

def print_header():
    print(Fore.WHITE + Style.BRIGHT + "=" * 80)
    print(Fore.WHITE + Style.BRIGHT + " API-T".center(80))
    print(Fore.WHITE + Style.BRIGHT + "=" * 80)
    print()

def get_http_method():
    print(Fore.WHITE + "Choose Method:")
    print(" 1. POST")
    print(" 2. GET")
    print(" 3. PUT")
    print(" 4. DELETE")
    print(" 5. PATCH")
    print(" 6. HEAD")
    print(" 7. OPTIONS")
    print(" 8. PUT (form-data)")
    print(" 9. POST (form-data)")
    print("10. POST (raw text)")
   
    while True:
        choice = input(Fore.WHITE + "\nEnter choice (1-10): " + Style.RESET_ALL).strip()
        methods = {
            '1': 'POST', '2': 'GET', '3': 'PUT', '4': 'DELETE', '5': 'PATCH',
            '6': 'HEAD', '7': 'OPTIONS', '8': 'PUT_FORM', '9': 'POST_FORM', '10': 'POST_RAW'
        }
        if choice in methods:
            return methods[choice]
        print(Fore.RED + "Invalid choice." + Style.RESET_ALL)

def main():
    print_header()
    api_url = input(Fore.WHITE + "Enter the API URL: " + Style.RESET_ALL).strip()
    if not api_url.startswith("http"):
        print(Fore.RED + "error1: URL must start with http:// or https://" + Style.RESET_ALL)
        sys.exit(1)

    method = get_http_method()

    payload = None
    files = None
    data = None

    if method in ['POST', 'PUT', 'PATCH', 'POST_FORM', 'PUT_FORM', 'POST_RAW']:
        message = input(Fore.WHITE + "Enter payload (JSON, text, or leave blank): " + Style.RESET_ALL).strip()
        
        if message:
            if method in ['POST_FORM', 'PUT_FORM']:
                try:
                    data = eval(message) if message.startswith('{') else {"data": message}
                except:
                    data = {"data": message}
            elif method == 'POST_RAW':
                data = message
            else:
                try:
                    if message.startswith(('{', '[')):
                        payload = eval(message)
                    else:
                        payload = {"data": message}
                except:
                    payload = {"message": message}

    try:
        times = int(input(Fore.WHITE + "Number of Times to Send it; " + Style.RESET_ALL))
        if times < 1:
            print(Fore.RED + "Number Must Be 1 or Over." + Style.RESET_ALL)
            sys.exit(1)
    except ValueError:
        print(Fore.RED + "Incorrect Number." + Style.RESET_ALL)
        sys.exit(1)

    delay_input = input(Fore.WHITE + "Delay between requests in seconds (press Enter for default 1.3s every 5): " + Style.RESET_ALL).strip()
    manual_delay = float(delay_input) if delay_input else 0

    custom_ua = input(Fore.WHITE + "uAgent (leave blank for default): " + Style.RESET_ALL).strip()
   
    headers = {
        "User-Agent": custom_ua if custom_ua else "Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0"
    }

    print(Fore.GREEN + f"\nStarting {method.replace('_', ' ')} to: {api_url}" + Style.RESET_ALL)
    print(Fore.WHITE + "-" * 90 + Style.RESET_ALL)

    success_count = 0
    session = requests.Session()
    session.headers.update(headers)

    for i in range(1, times + 1):
        try:
            if method == 'GET':
                response = session.get(api_url, timeout=10)
            elif method == 'POST':
                response = session.post(api_url, json=payload, timeout=10)
            elif method == 'PUT':
                response = session.put(api_url, json=payload, timeout=10)
            elif method == 'DELETE':
                response = session.delete(api_url, timeout=10)
            elif method == 'PATCH':
                response = session.patch(api_url, json=payload, timeout=10)
            elif method == 'HEAD':
                response = session.head(api_url, timeout=10)
            elif method == 'OPTIONS':
                response = session.options(api_url, timeout=10)
            elif method == 'POST_FORM':
                response = session.post(api_url, data=data, timeout=10)
            elif method == 'PUT_FORM':
                response = session.put(api_url, data=data, timeout=10)
            elif method == 'POST_RAW':
                response = session.post(api_url, data=data, headers={**headers, "Content-Type": "text/plain"}, timeout=10)

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
        print(f"{status} {method.replace('_FORM','').replace('_RAW',''):<6} | {api_url[:55]:<55} | {msg:<35} | {progress:>8}")

        if manual_delay > 0:
            time.sleep(manual_delay)
        elif i % 5 == 0 and i != times:
            time.sleep(1.3)

    print(Fore.WHITE + "\n" + "=" * 90 + Style.RESET_ALL)
    print(Fore.GREEN + f"Complete. {success_count}/{times} | Method: {method.replace('_', ' ')}" + Style.RESET_ALL)
    print(Fore.WHITE + "=" * 90 + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nStopped by User." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\nUnexpected error: {e}" + Style.RESET_ALL)
