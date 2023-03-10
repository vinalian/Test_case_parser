from parser import services
from bs4 import BeautifulSoup
import threading


def parser():
    for i in range(1, 15):
        url = f'https://codeforces.com/problemset/page/{i}?order=BY_SOLVED_DESC&locale=ru'
        response = services.get_resource(url)
        html = BeautifulSoup(response.content, 'html.parser')
        services.add_to_db(html.find('table', class_='problems'))
        print(f'[LOG] page {i} completed')
    threading.Timer(60*60, parser).start()


if __name__ == '__main__':
    parser()
