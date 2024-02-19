from datetime import datetime
from datetime import timedelta
import random


class Post:
    def __init__(self, id, title, subtitle, body, image_url, author):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.body = body
        self.image_url = image_url
        self.post_date = self.get_random_date()
        self.author = author

    @staticmethod
    def get_random_date():
        today = datetime.now()
        from_date = datetime.strptime(f"1/1/{today.year-1}", "%d/%m/%Y")
        to_date = datetime.strptime(f"{today.day}/{today.month}/{today.year}", "%d/%m/%Y")

        delta_time = to_date - from_date
        int_delta_time = (delta_time.days * 24 * 60 * 60) + delta_time.seconds
        random_seconds_num = random.randrange(int_delta_time)

        return (from_date + timedelta(seconds=random_seconds_num)).strftime("%B %d, %Y")  # e.g. July 8, 2023
