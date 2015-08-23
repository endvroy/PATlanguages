import requests, bs4, collections, threading, getpass

payload = {
    'user[remember_me]': 0
}

# TODO: get username and password
username = input('Input your username: ')
password = getpass.getpass('Input your password: ')
payload['user[handle]'] = username
payload['user[password]'] = password

counter = collections.Counter()


def getData(startPage, endPage):
    with requests.Session() as s:
        p = s.post('http://www.patest.cn/users/sign_in', data=payload)
        # print(p.text)

        for page in range(startPage, endPage + 1):
            print('getting page %d...' % page)
            url = 'http://www.patest.cn/contests/pat-b-practise/submissions?page=%d' % page
            res = s.get(url)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text)

            table = soup.select('table')[0]
            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                counter.update([cells[4].text])


# TODO: multithreading
getThreads = []
for i in range(0, 1000, 100):
    getThread = threading.Thread(target=getData, args=(i + 1, i + 100))
    getThreads.append(getThread)
    getThread.start()

for thread in getThreads:
    thread.join()

# TODO: print the result
print('\n------------------------------------------------------------------------')
for lang in counter.keys():
    print('%s : %d' % (lang, counter[lang]))
    # print(counter)
