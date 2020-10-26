import time
import sys

# toolbar_width = 40

# setup toolbar
# sys.stdout.write("[%s]" % (" " * toolbar_width))
# sys.stdout.flush()
# sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

# for i in xrange(toolbar_width):
#     time.sleep(0.1) # do real work here
#     # update the bar
#     sys.stdout.write("-")
#     sys.stdout.flush()

# sys.stdout.write("]\n") # this ends the progress bar


def display_bar(percentage : float):
    bar_length = 40
    progress = int(percentage*bar_length)
    sys.stdout.write("\b" * (bar_length+2))
    sys.stdout.write("[%s]" % ("-"*progress+" "*(bar_length-progress-1)))
    sys.stdout.flush()

i = 0.0
while i <= 1.0:
    display_bar(i)
    time.sleep(0.1)
    i += 0.01
print()
