from pat import getPayload
from collections import Counter
from concurrent import futures
import requests, bs4
from tqdm import tqdm


def getPage(session, page):
    # print('getting page %d...' % page)
    url = 'http://www.patest.cn/contests/pat-b-practise/submissions?page=%d' % page
    res = session.get(url)

    try:
        res.raise_for_status()
    except requests.HTTPError as exc:
        if exc.response.status_code == 404:
            print('page {} encountered 404'.format(page))
        else:
            raise
    else:
        return res


def extractColumns(res):
    counter = Counter()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    table = soup.select('table')[0]
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        counter.update([cells[4].text])
    return counter


def getCount(payload, page):
    return extractColumns(getPage(payload, page))


if __name__ == '__main__':
    payload = getPayload()
    executor = futures.ThreadPoolExecutor(max_workers=100)
    fs = set()
    with requests.Session() as session:
        session.post('http://www.patest.cn/users/sign_in', data=payload)
        for i in range(1, 1001):
            future = executor.submit(getCount, session, i)
            fs.add(future)
        results = futures.as_completed(fs)
        results = tqdm(results, total=len(fs))

        # results = executor.map(partial(getCount, payload), range(1, 1000, 100))
        counter = Counter()
        for future in results:
            counter.update(future.result())
    print(counter)
