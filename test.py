import re

class Chatbot:
    def __init__(self):
        self.subject_keywords = ["lab", "pt", "acft", "pt test", "ftx", "spring ftx", "fphysical training"]
        self.time_keywords = ["when", "where", "what", "tomorrow", "today", "next week", "week after next week", "week"]
        self.month_keywords = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
        self.day_keywords = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    def tokenize(self, message):
        tokens = re.findall(r"[\w']+", message)
        print(tokens)
        for token in tokens:
            print(token)

message = "What time is lab thursday"

bot = Chatbot()
bot.tokenize(message)
