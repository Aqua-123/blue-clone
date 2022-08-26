class emeUser:
    def __init__(self, user_id, name, username, karma):
        self.id = user_id
        self.name = name
        self.username = username
        self.karma = karma


class constrains:
    def __init__(self):
        self.running = True
        self.greetStatus = True
        self.altUniverseToggle = False
        self.shortenedGreets = True
        self.guessingGameStatus = True
        self.insultControl = True
        self.spamCheckToggle = True
