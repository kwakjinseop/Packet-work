x = []


class A:
    def func_1(self):
        #populate the x variable
        global x
        x.append(1)
class B:
    def func_2(self):
        global x
        print(x)