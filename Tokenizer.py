from datetime import datetime, timedelta, date
import calendar

class Tokenizer:
    def __init__(self):
        self.input_string = None
        self.tokens = None

        #keeps track of question errors when tockenizing
        self.token_error = 0

        #keeps track of question type
        self.question_type = None
        #keeps track of question subject
        self.subject = None
        #keeps track of sql range to search for based on tockenization
        self.time_frame_start = None
        self.time_frame_end = None

        #which query results to include in message
        self.use_all = True

    def tokenize(self, input_string):
        self.input_string = input_string.lower()
        self.tokens = self.input_string.split(" ")
        self.current_date = datetime.now()
        self.time_frame_start = self.current_date.timetuple().tm_yday 
        self.time_frame_end = self.current_date.replace(month=12, day=31).timetuple().tm_yday
        month_names = [m.lower() for m in calendar.month_name[1:]]

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
            if any(month in self.tokens for month in month_names) and any(x.isdigit() for x in self.tokens):
                self.token_error = 1
            elif any(month in self.tokens for month in month_names):
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
            if any(month in self.tokens for month in month_names) and any(x.isdigit() for x in self.tokens):
                #if month and day specified are before current date assign self.token_error to 2
                #if month and day specified are invalid assign self.token_error to 3
                #self.time_frame_start becomes exact date specified
                #self.time_frame_end becomes exact date specified
                month = None
                day = None
                for token in self.tokens:
                    if token in month_names:
                        month = token
                    elif token.isdigit():
                        day = token
                month = month.capitalize()
                if month and day:
                    specified_date = datetime(self.current_date.year, list(calendar.month_name).index(month), int(day))
                    if specified_date < self.current_date:
                        self.token_error = 2
                        print('date is less than current date')
                    else:
                        self.time_frame_start = specified_date.timetuple().tm_yday
                        self.time_frame_end = self.time_frame_start
                else:
                    print('data is invalid')
                    self.token_error = 3
            elif any(month in self.tokens for month in month_names):
                #if month specified is before current date assign self.token_error to 2
                #self.time_frame_start becomes first anual day of month specified or the current anual day if the month is the current month
                #self.time_frame_end becomes last anual day of month specified
                month = None
                for token in self.tokens:
                    if token in month_names:
                        month = token
                month = month.capitalize()
                if month:
                    specified_date = datetime(self.current_date.year, list(calendar.month_name).index(month), self.current_date.day)
                    if specified_date.day < self.current_date.day:
                        self.token_error = 2
                        print('date is less than current date')
                    elif specified_date.month == self.current_date.month:
                        self.time_frame_start = specified_date.timetuple().tm_yday
                        specified_date = specified_date.replace(day=1)
                        self.time_frame_end = specified_date.timetuple().tm_yday + calendar.monthrange(specified_date.year, specified_date.month)[1] - 1
                    else:
                        specified_date = specified_date.replace(day=1)
                        self.time_frame_start = specified_date.timetuple().tm_yday
                        self.time_frame_end = self.time_frame_start + calendar.monthrange(specified_date.year, specified_date.month)[1] - 1
            elif "week" in self.tokens:
                #self.time_frame_start becomes the year day for the closest monday that is not the current year day
                #self.time_frame_start becomes the year day for the sunday in the same week as self.time_frame_start
                self.time_frame_start = self.current_date.timetuple().tm_yday - self.current_date.weekday()
                self.time_frame_end = self.time_frame_start + 6
            elif "month" in self.tokens:
                #self.time_frame_start becomes the year day for the first day of the upcoming month
                #self.time_frame_end becomes the year day for the last day of the upcoming month
                this_month = self.current_date.replace(day=1)
                self.time_frame_start = this_month.timetuple().tm_yday
                self.time_frame_end = self.time_frame_start + calendar.monthrange(this_month.year, this_month.month)[1] - 1
            else:
                #self.time_frame_start becomes current year day
                #self.time_frame_end becomes last year day of year
                self.time_frame_start = self.current_date.timetuple().tm_yday
                self.time_frame_end = self.current_date.replace(month=12, day=31).timetuple().tm_yday
                self.use_all = False

    def resetBot(self):
        self.input_string = None
        self.tokens = None

        #keeps track of question errors when tockenizing
        self.token_error = 0

        #keeps track of question type
        self.question_type = None
        #keeps track of question subject
        self.subject = None
        #keeps track of sql range to search for based on tockenization
        self.time_frame_start = None
        self.time_frame_end = None

        #which query results to include in message
        self.use_all = True

    def generateResponse(self):
        #Check for tokenization error codes
        if self.token_error == 1:
            return 'Im sorry the date you requested is not this year, I am only able to handle dates this year'
        elif self.token_error == 2:
            return 'Im sorry the date you requested is before the current date please ask information on events after the current date'
        elif self.token_error == 3:
            return 'Im sorry the date you requested is invalid please ask me for information using a valid date'
        #return the requested information if no error present
        if self.question_type == 1:
            if self.subject == 1:
                return 'It looks like you are asking me what lab is ' + str(self.time_frame_start) + ' ' + str(self.time_frame_end)
            elif self.subject == 2:
                return 'It looks like you are asking me what pt is ' + str(self.time_frame_start) + ' ' + str(self.time_frame_end)
            elif self.subject == 3:
                return 'It looks like you are asking me what acft is ' + str(self.time_frame_start) + ' ' + str(self.time_frame_end)
            elif self.subject == 4:
                return 'It looks like you are asking me what ftx is ' + str(self.time_frame_start) + ' ' + str(self.time_frame_end)
        elif self.question_type == 2:
            if self.subject == 1:
                return 'It looks like you are asking me where lab is ' + str(self.time_frame_start) + ' ' + str(self.time_frame_end)
            elif self.subject == 2:
                return 'It looks like you are asking me where pt is ' + str(self.time_frame_start) + ' ' + str(self.time_frame_end)
            elif self.subject == 3:
                return 'It looks like you are asking me where acft is ' + str(self.time_frame_start) + ' ' + str(self.time_frame_end)
            elif self.subject == 4:
                return 'It looks like you are asking me where ftx is ' + str(self.time_frame_start) + ' ' + str(self.time_frame_end)
        elif self.question_type == 3:
            if self.subject == 1:
                return 'It looks like you are asking me when lab is ' + str(self.time_frame_start) + ' ' + str(self.time_frame_end)
            elif self.subject == 2:
                return 'It looks like you are asking me when pt is ' + str(self.time_frame_start) + ' ' + str(self.time_frame_end)
            elif self.subject == 3:
                return 'It looks like you are asking me when acft is ' + str(self.time_frame_start) + ' ' + str(self.time_frame_end)
            elif self.subject == 4:
                return 'It looks like you are asking me when ftx is ' + str(self.time_frame_start) + ' ' + str(self.time_frame_end)
        else:
            return 'Im sorry it looks like you are not asking me a question, please use what where or when to ask questions'
