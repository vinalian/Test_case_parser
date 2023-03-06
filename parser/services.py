import requests
from parser.data_base import Parser_connection
from psycopg2.errors import UniqueViolation


topic_url = 'https://codeforces.com'


def get_resource(url: str) -> requests.Response or None:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code != 200:
        return None
    return response


def add_to_db(html) -> None:
    for topic in html.find_all('tr'):
        if topic.find('td', class_='id'):
            name = topic.find('td', class_=None).find('a').text
            number = topic.find('td', class_='id').find('a').text
            number_of_passes = topic.find_all('a')[-1].text
            notices = ''
            difficulty = topic.find('span', class_='ProblemRating').text
            url = f"{topic_url}{topic.find('td', class_='id').find('a')['href']}"
            for notice in topic.find_all('a', class_='notice'):
                notices += notice.text + ', '
            notices = notices.strip()[:-1]
            try:
                con = Parser_connection()
                con.add_data_to_database(
                                name=name.strip(),
                                number=number.strip(),
                                number_of_passes=number_of_passes.strip()[1:],
                                notices=notices,
                                difficulty=difficulty,
                                url=url
                            )
            except UniqueViolation:
                con.cur.close()



