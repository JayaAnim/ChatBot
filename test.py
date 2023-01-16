from datetime import datetime, timedelta
import calendar

class Tokenizer:
    def __init__(self, input_string):
        self.input_string = input_string.lower()
        self.tokens = self.input_string.split(" ")
        self.current_date = datetime.now()

        self.token_error = 0

        self.question_type = None
        self.subject = None

        self.time_frame_context_type = None
        self.time_frame_start = self.current_date.timetuple().tm_yday 
        self.time_frame_end = 364

    def tokenize(self):
        if "what" in self.tokens:
            self.question_type = 1
        elif "where" in self.tokens:
            self.question_type = 2
        elif "when" in self.tokens:
            self.question_type = 3

        if "lab" in self.tokens:
            self.subject = 1
        elif "pt" in self.tokens:
            self.subject = 2
        elif "acft" in self.tokens:
            self.subject = 3
        elif "ftx" in self.tokens:
            self.subject = 4

        if "next" in self.tokens:
            if any(month in self.tokens for month in calendar.month_name[1:]) and any(x.isdigit() for x in self.tokens):
                self.token_error = 1
            elif any(month in self.tokens for month in calendar.month_name[1:]):
                self.token_error = 1
            elif "week" in self.tokens:
                #self.time_frame_start becomes the year day for the closest monday that is not the current year day
                #self.time_frame_start becomes the year day for the sunday in the same week as self.time_frame_start
                self.time_frame_start = (self.current_date + timedelta(days=(7 - self.current_date.weekday()))).timetuple().tm_yday
                self.time_frame_end = self.time_frame_start + 6
            elif "month" in self.tokens:
                #self.time_frame_start becomes the year day for the first day of the upcoming month
                #self.time_frame_end becomes the year day for the last day of the upcoming month
                if self.current_date.month == 12:
                    next_month = self.current_date.replace(year=self.current_date.year+1, month=1)
                else:
                    next_month = self.current_date.replace(month=self.current_date.month+1)
                self.time_frame_start = (next_month - datetime(next_month.year, 1, 1) + timedelta(days=1)).days
                if next_month.month == 12:
                    last_day_of_next_month = datetime(year=next_month.year+1, month=1, day=1) - timedelta(days=1)
                else:
                    last_day_of_next_month = datetime(year=next_month.year, month=next_month.month+1, day=1) - timedelta(days=1)
                self.time_frame_end = (last_day_of_next_month - datetime(next_month.year, 1, 1) + timedelta(days=1)).days


        print(self.time_frame_start)
        print(self.time_frame_end)



input_string = "What lab is next month"
tokenizer = Tokenizer(input_string)
tokenizer.tokenize()