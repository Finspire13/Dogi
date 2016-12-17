import cmd
from threading import Thread
from time import sleep
import sys
import string, os
import StringIO

strInput = StringIO.StringIO()

def threaded_function(arg):
    for i in range(arg):
        strInput.write("help")
        print i
        sleep(1)

class HelloWorld(cmd.Cmd):
    """Simple command processor example."""
    
    # Disable rawinput module use
    use_rawinput = False
    
    # Do not show a prompt after each command read
    prompt = ''
    
    def do_greet(self, line):
        print "hello,", line
    
    def do_EOF(self, line):
        print "EOF"

if __name__ == '__main__':



    thread = Thread(target = threaded_function, args = (10, ))
    thread.start()

    try:
        HelloWorld(stdin=strInput).cmdloop()
    finally:
        strInput.close()

# if __name__ == '__main__':
#     import sys
#     input = open(sys.argv[1], 'rt')
#     try:
#         HelloWorld(stdin=input).cmdloop()
#     finally:
#         input.close()