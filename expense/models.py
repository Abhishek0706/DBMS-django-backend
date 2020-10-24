from django.db import connection

# Create your models here.


class Expense:

    def __init__(self, week_number: int, year_number: int, amount: float):
        self.week_number = week_number
        self.year_number = year_number
        self.amount = amount

    def save(self):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO public.expense VALUES (%s, %s, %s)", [self.week_number, self.year_number, self.amount])
            connection.commit()

    @classmethod
    def from_week_year(cls, week_no: int, year_no: int):
        with connection.cursor() as cursor:
            cursor.execute("SELECT week_number, year_number, amount FROM public.expense WHERE (week_number=%s AND year_number=%s)", [week_no, year_no])
            expense = cursor.fetchone()
            
        return cls(*expense)
