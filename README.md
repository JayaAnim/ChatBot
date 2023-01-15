Tokenization ideas


class Chatbot:
    def __init__(self):
        self.question_keywords = {"when": 100, "where": 200, "what": 300}
        self.subject_keywords = {"lab": 10, "pt": 20, "acft": 30, "pt test": 40, "ftx": 50, "fphysical training": 60}
        self.time_keywords = {"tomorrow": 1, "today": 2, "next week": 3, "week after next week": 4, "week": 5, "month": 6, "day": 7}
        self.month_keywords = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}
        self.day_keywords = {"monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6, "sunday": 7}

    def tokenize(self, message):
        tokens = re.findall(r"[\w']+", message)
        question_value = None
        subject_value = None
        time_value = None
        month_value = None
        day_value = None
        for token in tokens:
            if token.lower() in self.question_keywords:
                question_value = self.question_keywords[token.lower()]
            if token.lower() in self.subject_keywords:
                subject_value = self.subject_keywords[token.lower()]
            if token.lower() in self.time_keywords:
