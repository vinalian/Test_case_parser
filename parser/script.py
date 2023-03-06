from parser import services
from bs4 import BeautifulSoup
import threading

url = 'https://codeforces.com/problemset/page/1?order=BY_SOLVED_DESC&locale=ru'


def parser():
    response = services.get_resource(url)
    html = BeautifulSoup(response.content, 'html.parser')
    services.add_to_db(html.find('table', class_='problems'))
    threading.Timer(60*60*60, parser).start()


if __name__ == '__main__':
    parser()
