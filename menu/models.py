from django.db import connection
from datetime import datetime, timedelta, date

# Create your models here.

class Menu:
    def __init__(self, menu_date: datetime, title_name: str, items: list, **kwargs):
        self.menu_date = datetime.combine(menu_date.date(), datetime.min.time())
        with connection.cursor() as cursor:
            cursor.execute("SELECT title_id, start_time, end_time FROM public.title WHERE title_name=%s", [title_name])
            self.title_id, self.start_time, self.end_time = cursor.fetchone()
        self.title_name = title_name
        self.items = items

    def save(self):
        with connection.cursor() as cursor:
            for item in self.items:
                cursor.execute("INSERT INTO public.menu VALUES (DEFAULT, %s, %s, %s)", [self.menu_date, self.title_id, item])
            connection.commit()

    @classmethod
    def from_day(cls, given_date: datetime):
        day = datetime.combine(given_date.date(), datetime.min.time())
        with connection.cursor() as cursor:
            print(day)
            cursor.execute("SELECT title.title_name, array_agg(menu.item) FROM (SELECT title_id, item, menu_date FROM public.menu) as menu NATURAL JOIN (SELECT title_id, title_name FROM public.title) as title WHERE menu.menu_date=%s GROUP BY title.title_name", [day])
            results = cursor.fetchall()
        menus = []
        for result in results:
            menus.append(cls(day,*result))
        return menus

