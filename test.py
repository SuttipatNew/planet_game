class EventListenner :
    def __init__(self) :
        self.mes = 'hello'

    def __del__(self) :
        print('abc')

a = EventListenner()
print(a.mes)
del a
# print(a.mes)
