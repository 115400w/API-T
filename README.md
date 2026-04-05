# API-T 
Send multiple HTTP requests to test APIs.

**GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS**
- Payload=JSON/TEXT


- Default User Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36

<img width="891" height="120" alt="image" src="https://github.com/user-attachments/assets/4e91d308-1405-49fd-bd41-a5f3dd2e4a71" />

## How To Run:

**Extract API-T-main.zip**,

**Open cmd.exe**,
**cd downloads**,
**cd API-T-main**,
**cd clients\python**,
**python main.py**

--------------------------------------------------------------

# Requirements:
**Python 3.8+**

**requests**

**colorama**

--------------------------------------------------------------

- Do not use this tool to spam, overload, or attack any service.
- Only test APIs that you own or have written permission to test.
- Misuse of this tool may violate the terms of service of the target API and can result in account suspension or legal consequences
- Use responsibly and only on APIs you own or have explicit permission to test.
- **__The author is not responsible for any misuse of this software.__**
--------------------------------------------------------------

## Issues?

**EXAMPLE PAYLOAD:** {"type": "giveaway", "username": "hello this is my message!"}
You need to know the *standard* payload format (e.g. {"type": "logs", "message": "logged 1 user"}).

**Most API's Are Limited to A Certain Request Only!**


<img width="211" height="136" alt="image" src="https://github.com/user-attachments/assets/eb292a2f-844c-4043-8d3f-d226e4604c3f" />


Example from A Script:
``def send_request(username):
    payload = {
        "type": "giveaway",
        "username": username
    }``




    
