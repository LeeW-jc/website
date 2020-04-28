from pyquery import PyQuery as pq
import os
import requests


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 '
                      'QQBrowser/10.5.3863.400',
    }
page = 0


def log(*args, **kwargs):
    with open("log22_utils.txt", "a", encoding="utf-8") as f:
        print(*args, file=f, **kwargs)


class Case(object):
    def __init__(self, doc):
        self.name = doc('.yp_bt').find('h1').text()
        item = pq(doc('.x_z')[0])
        self.information = item.find('a').attr('href')
        log(self.information + '\n')

    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


def response_cached_url(url):
    folder = 'websites'
    filename = url.split('/')[-2] + '.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return f.read()
    if not os.path.exists(folder):
        os.makedirs(folder)
    r = requests.get(url, headers=headers)
    with open(path, 'wb') as f:
        f.write(r.content)
        return r.content


def case_by_url(url):
    page = response_cached_url(url)
    doc = pq(page)
    print(Case(doc))


def run():
    for i in range(31201, 31400):
        print('page:', i)
        try:
            global page
            page = i
            url = 'https://8fql.com/html/{}/'.format(i)
            case_by_url(url)
        except Exception as result:
            print(result)


if __name__ == '__main__':
    run()


