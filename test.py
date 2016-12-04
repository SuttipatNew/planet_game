class EventListenner :
    def __init__(self) :
        self.__handlers = []

    def add(self, handler) :
        self.__handlers.append(handler)

    def notify(self, *args, **keywargs) :
        for handler in self.__handlers :
            handler(*args, **keywargs)

class MyTest:
    def __init__(self) :
        self.listenner = EventListenner()

    def update(self) :
        for i in range(0,10) :
            if i % 2 == 0 :
                self.listenner.notify(i)
