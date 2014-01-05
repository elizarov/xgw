
from time import strftime, localtime

def fmt_time(secs):
    return strftime("%Y%m%dT%H%M%S", localtime(secs))
