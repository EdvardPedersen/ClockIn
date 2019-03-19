import argparse
import time

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkin", action="store_true")
    parser.add_argument("--report", action="store_true")
    return parser.parse_args()
    

def make_report(options, database):
    timestamps = database.keys()
    fixed_time = [time.localtime(x) for x in timestamps]
    current_time = time.localtime()

    days = {}
    for cur_time in fixed_time:
        if not cur_time.tm_yday in days:
            days[cur_time.tm_yday] = []
        days[cur_time.tm_yday].append(time.mktime(cur_time))

    for day in days.keys():
        sorted_times = sorted(days[day])
        diff = 0
        for i in range(0,len(sorted_times), 2):
            try:
                diff += sorted_times[i+1] - sorted_times[i]
            except:
                print("Not checked out yet")
        print("Seconds worked on day {}: {}".format(day, diff))

if __name__ == "__main__":
    options = parse_arguments()
    if options.report:
        print("Make report")
    elif options.checkin:
        print("Checking in")
    else:
        print("Checking out")

    database = {123: ["checkin"], 4000: ["checkout"], 604500: ["checkin"], 605000: ["checkout"]}
    make_report(options, database)
