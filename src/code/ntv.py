


import requests
import sys
import itertools
import threading
import time
import subprocess
import sys
import shutil


def nmap(domain, ip):

    if not shutil.which("nmap"):
        print("\n[Error]: Nmap not found. Please install it and try again.")
        sys.exit(1)

    command = ["nmap", "-p-", "-sV", "--open", "-T4", ip]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode != 0:  # Output: 0  (Success)
            print(f"\n[Error]: {error.decode().strip()}")
            sys.exit(1)

        print(output.decode())

    except Exception as e:
        print(f"\n[Error]: An unexpected error occurred - {str(e)}")
        sys.exit(1)


def handle_targets (targets = None  , user_agent = None) : 

    if  targets is  None  :
        print ("[Info]0 targets to scan ,  exit .. ")
        sys.exit() 

    if user_agent is not None  : 
        #Nmap user agent header 
        requests.Session().headers.update({"User-Agent": user_agent})
    

    Threads = []
    for k , v in targets.values() : 
        for t in v  :
            th = threading.Thread(target=nmap, args=(t[0] , t[1]))
            th.start()
            Threads.append(th)
    animation = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])

    while any(t.is_alive() for t in Threads):
        with lock:
            scanned = len([t for t in Threads if not t.is_alive()])
            sys.stdout.write(f"\r{'':<10}{next(animation)} {scanned} out of {len(targets)} targets scanner ")
            sys.stdout.flush()
        time.sleep(0.3)
    for t in Threads:
        t.join()