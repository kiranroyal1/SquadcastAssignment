# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# main.py
from SayHello.hello import Hello
def print_hi(name):
    print(f'Hi, {name}')

if __name__ == '__main__':
    print_hi('PyCharm')
    hello_instance = Hello()
    hello_result = hello_instance.say_hi()  # Corrected this line
    print(hello_result)

