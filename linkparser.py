import re
from typing import Match, List, Any

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_message(courses_id, creds) -> str:
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
            latest_course_id = courses_id
            announcements = service.courses().announcements().list(courseId=latest_course_id).execute()
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


def get_link(message: str) -> str:
    try:
        link = re.findall(r'https.*', message)
        return link[0]
    except IndexError as error:
        return "В последнем сообщении курса нет нужных ссылок"
