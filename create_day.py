import sys
import os 
import requests
n = str(int(sys.argv[1]))

n = n.zfill(2)
try:
    os.mkdir(n)
    paht = n + "/"
except:
    print("Already Existing Directory. Bye")
    exit()
with open(paht+"1.py", "w") as f:
    f.write("import sys\n")
    f.write("\n")
    f.write("path = sys.argv[1]\n")
    f.write("with open(path, 'r') as f:\n")
    f.write("    lines = f.readlines()\n")
    f.write("\n")

url = 'https://adventofcode.com/2021/day/' + str(int(n)) + '/input'
try:
    cookies = {
        '_ga': 'GA1.2.1834858622.1639001693',
        'session': '53616c7465645f5f4eb46166df8ef909fc2c803baba20b4adc1338545161513d1291005e4ebc0e5e25c321cccfdaf65e',
        '_gid': 'GA1.2.488913670.1639410633',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,fr;q=0.8,fr-FR;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://adventofcode.com/2021/day/7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'max-age=0',
        'TE': 'trailers',
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    with open(path + 'input.txt', 'w') as f:
        f.write(response.text)
except:
    print("No file of input")
