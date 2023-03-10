import requests
from parser.data_base import Parser_connection, Collection_connect
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
            try:
                name = topic.find('td', class_=None).find('a').text
                number = topic.find('td', class_='id').find('a').text
                number_of_passes = topic.find_all('a')[-1].text
                notices = ''
                difficulty = topic.find('span', class_='ProblemRating').text
                url = f"{topic_url}{topic.find('td', class_='id').find('a')['href']}"
            except Exception as e:
                print(f'[ERROR] {e}\n{topic.find("td", class_="id")}')
                break
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
    create_collection()


def create_collection() -> None:
    con = Collection_connect()
    topics = con.get_topic_without_collection()
    for topic in topics:
        collections = get_inc_collection(topic)
        if not collections:
            if len(topic[1].split(',')) == 1:
                con.create_collection(topic_id=topic[0],
                                      notices=topic[1],
                                      dif=topic[2])
            else:
                con.create_collection(topic_id=topic[0],
                                      notices=topic[1].split(',')[0],
                                      dif=topic[2])
        else:
            new_topic_id_list = f"{collections[2]}*{topic[0]}"
            con.update_collection(id=collections[0],
                                  topic_id=new_topic_id_list)
            con.set_topic_status(id=topic[0])


def get_inc_collection(topic: list) -> list or None:
    con = Collection_connect()
    if len(topic[1].split(',')) == 1:
        data = con.get_inc_collection(notices=topic[1],
                                      dif=topic[2])
        return data
    for info in topic[1].split(','):
        data = con.get_inc_collection(notices=info,
                                      dif=topic[2])
        if data:
            return data
    return None
