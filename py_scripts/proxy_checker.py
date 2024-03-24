import requests
import threading
import queue


q = queue.Queue()
valid_proxy = []

with open(f"py_scripts\\Free_Proxy_List.txt", "w", encoding='utf-8') as file:
    res = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
    file.write(res.text)

with open(f"py_scripts\\Free_Proxy_List.txt", "r", encoding='utf-8') as file:
    ip_add = file.read().split("\n")
    for p in ip_add:
        q.put(p)

def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("https://api.ipify.org",
                proxies={
                "http": f"http://{proxy}",
                "https": f"https://{proxy}",
            })
            if res.text == proxy:
                print(proxy)
                valid_proxy.append(proxy)
                print(res.text)
                with open(f"py_scripts\\Valid_Proxy_List.txt", "a", encoding='utf-8') as file:
                    file.write(proxy + "\n")
        except:
                continue
            

for t in range(10):
    threading.Thread(target=check_proxies).start()

