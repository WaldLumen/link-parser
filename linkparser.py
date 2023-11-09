import re
import configparser

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

COURSES_ID = [["eng", "637129488148"],
              ["math", "635843353358"],
              ["hist", "620797854331"],
              ["phy", "620408593297"],
              ["ukrlit", "544956500670"]]

config = configparser.ConfigParser()
config.read('/home/sylvia/.local/bin/links.ini')


def get_message(course_id: str, creds) -> str:
    """

    :param course_id: str
    :param creds: str
    :return:
    """
    try:
        """
        DONE Вынести ету консрукцию в отдельную от мейна функцию, добавив ей аргументы id: Vec<u32> и creds
        TODO Узнать как работают и возмлжно написать свой хендлер отслежтвающий изменения в курсе
        TODO Добавить логи 
        """
        service = build("classroom", "v1", credentials=creds)

        # Call the Classroom API
        results = service.courses().list().execute()
        courses = results.get("courses", [])

        if courses:
            announcements = service.courses().announcements().list(courseId=course_id).execute()
            if announcements.get('announcements', []):
                latest_announcement = announcements['announcements'][0]
                # print('Последнее сообщение в курсе: {}'.format(latest_announcement['text']))
                return latest_announcement["text"]
            else:
                print('В данном курсе нет объявлений.')
        else:
            print('Нет доступных курсов.')


    except HttpError as error:
        print(f"An error occurred: {error}")
    print()


def get_link(message: str, course: str) -> str:
    try:
        link = re.findall(r'https.*', message)
        return link[0]
    except IndexError:
        print(f"В последнем сообщении курса {course} нет нужных ссылок")
        return " "


def get_all_links(creds, list, id=0):
    for i in range(len(COURSES_ID)):
        element = []
        link = get_link(get_message(COURSES_ID[id][1], creds), COURSES_ID[id][0])
        element.append(COURSES_ID[id][0])
        element.append(link)
        if element not in list:
            if element[0] in list:
                list[id][1] = link
            else:
                list.append(element)
        id += 1
    print(list)


def get_update(links, links_new, id=0):
    if links_new != links:
        for i in range(len(links)):
            if links_new[id] == links[id]:
                links[id] = links_new[id]
                config.set("links", f"{links[id][0]}", f"{links[id][1]}")
                with open('/home/sylvia/.local/bin/links.ini', 'w') as configfile:
                    config.write(configfile)
                print("save data")
            id += 1
