from math import modf

def terraria_to_24h(time, night=False):
    time /= 3600
    time += 4.5
    if night:
        time += 15
    time %= 24
    minutes, hours = modf(time)
    return "{0}:{1:0^2.0f}".format(int(hours), int(minutes*60))
