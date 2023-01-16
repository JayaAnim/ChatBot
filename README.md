Chatbot to assist Army ROTC detachment at UWF with distributing uniform information to the battalion

Functionality:
    Chatbot is hosted on Google App Engine and responds to all messages in relavant chats that begin with "Argo"
    Chatbot is connected to Google's SQL API to maintain data on Army ROTC Battalion plans for the year
    Chatbot can distribute relevant information requested

Methods:
    Chatbot uses simplistic word tokenization to dissect information requested by users and display relevant feedback
    Chatbot handles Groupme API calls using flask and App Engine hosting to send quick responses which vertically and horizontally scale
    Chatbot handles incorrect requests by users by dissecting requests in relevant order and matching tokens to current context of conversation

Use Cases:
    If a user needs information on upcoming training event, this week/month, next week/month, or at a specific date
    Example: Argo when is lab this week

Upcoming functionality:
    Handle days of week i.e "Argo when is lab this Thursday"
    Handle requested schedule by cadre i.e Argo bot sends information on lab for the week every Wednesday