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
                    self.time_frame_start = 1
                    self.time_frame_end = 31
                else:
                    next_month = self.current_date.replace(month=self.current_date.month+1, day=1)
                    self.time_frame_start = next_month.timetuple().tm_yday
                    self.time_frame_end = self.time_frame_start + calendar.monthrange(next_month.year, next_month.month)[1] - 1
        else:
            if any(month in self.tokens for month in calendar.month_name[1:]) and any(x.isdigit() for x in self.tokens):
                #if month and day specified are before current date assign self.token_error to 2
                #if month and day specified are invalid assign self.token_error to 3
                #self.time_frame_start becomes exact date specified
                #self.time_frame_end becomes exact date specified
            elif any(month in self.tokens for month in calendar.month_name[1:]):
                #if month specified is before current date assign self.token_error to 2
                #self.time_frame_start becomes first anual day of month specified or the current anual day if the month is the current month
                #self.time_frame_end becomes last anual day of month specified
            elif "week" in self.tokens:
                #self.time_frame_start becomes the year day for the closest monday that is not the current year day
                #self.time_frame_start becomes the year day for the sunday in the same week as self.time_frame_start
            elif "month" in self.tokens:
                #self.time_frame_start becomes the year day for the first day of the upcoming month
                #self.time_frame_end becomes the year day for the last day of the upcoming month
            else:
                #self.time_frame_start becomes current year day
                #self.time_frame_end becomes last year day of year

                
                


        print(self.time_frame_start)
        print(self.time_frame_end)



input_string = "What lab is next week"
tokenizer = Tokenizer(input_string)
tokenizer.tokenize()