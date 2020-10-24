from django.db import connection
from datetime import datetime, timedelta

# Create your models here.


def get_date_range_from_week_year(week_no: int, year_no: int):
    first_day = datetime.strptime(f"{year_no}-W{week_no-1}-1", "%Y-W%W-%w").date()
    last_day = first_day + timedelta(days=6.9)
    return first_day, last_day


class DailyWastage:

    def __init__(self, curr_date: datetime, amount: float, waste_weight: float):
        self.curr_date = curr_date
        self.amount = amount
        self.waste_weight = waste_weight

    def save(self):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO public.dailywastage VALUES (%s, %s, %s)", [self.curr_date, self.amount, self.waste_weight])
            connection.commit()

    @classmethod
    def from_week_year(cls, week_no: int, year_no: int):
        first_day, last_day = get_date_range_from_week_year(week_no, year_no)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM public.dailywastage WHERE curr_date BETWEEN %s and %s", [first_day, last_day])
            wastages = cursor.fetchall()
        res = []
        for wastage in wastages:
            res.append(cls(*wastage))
        return res

