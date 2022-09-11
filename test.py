from requests import get
import random

while True:
    print(random.choice(get("https://www.mit.edu/~ecprice/wordlist.10000").content.splitlines()).decode("utf-8"))
    print('a')
