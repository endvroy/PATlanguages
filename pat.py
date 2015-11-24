import requests, bs4, json, threading, getpass
from collections import Counter


def getPayload():
    payload = {
        'user[remember_me]': 0
    }

    # TODO: get username and password
    username = input('Input your username: ')
    password = getpass.getpass('Input your password: ')
    payload['user[handle]'] = username
    payload['user[password]'] = password
    return payload


def getCount(startPage, endPage):
    with requests.Session() as s:
        p = s.post('http://www.patest.cn/users/sign_in', data=payload)
        # print(p.text)

        for page in range(startPage, endPage + 1):
            print('getting page %d...' % page)
            url = 'http://www.patest.cn/contests/pat-b-practise/submissions?page=%d' % page
            res = s.get(url)

            try:
                res.raise_for_status()
            except requests.HTTPError as exc:
                if exc.response.status_code == 404:
                    print('page {} encountered 404'.format(page))
                else:
                    raise

            soup = bs4.BeautifulSoup(res.text)

            table = soup.select('table')[0]
            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                counter.update([cells[4].text])


if __name__ == '__main__':
    counter = Counter()
    payload = getPayload()
    # TODO: multithreading
    getThreads = []
    for i in range(0, 1000, 100):
        getThread = threading.Thread(target=getCount, args=(i + 1, i + 100))
        getThreads.append(getThread)
        getThread.start()

    for thread in getThreads:
        thread.join()

    # TODO: print the result
    print('\n------------------------------------------------------------------------')
    # print(json.dumps(counter))
    for lang in counter.keys():
        print('%s : %d' % (lang, counter[lang]))
        # print(counter)
