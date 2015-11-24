from pat import getPayload
from collections import Counter
from concurrent import futures
import requests, bs4
from functools import partial

step = 100


def getCount(payload, startPage):
    endPage = startPage + step
    counter = Counter()
    with requests.Session() as s:
        s.post('http://www.patest.cn/users/sign_in', data=payload)

        for page in range(startPage, endPage):
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
    return counter


if __name__ == '__main__':
    payload = getPayload()
    executor = futures.ThreadPoolExecutor(max_workers=50)
    results = executor.map(partial(getCount, payload), range(1, 1000, step))
    counter = Counter()
    for result in results:
        counter.update(result)
    print(counter)
