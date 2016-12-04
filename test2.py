from test import EventListenner, MyTest
# import test

def on_event(i) :
    print(i)

my_test = MyTest()
my_test.listenner.add(on_event)
my_test.update()
