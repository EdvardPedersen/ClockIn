import argparse
import time

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkin", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--detail", action="store_true")
    return parser.parse_args()
    

def get_hms(seconds):
    '''
    Given a number of seconds, return the hours, minutes and seconds
    '''
    h, remainder = divmod(seconds, 60*60)
    m, s = divmod(remainder, 60)
    return h, m, s


def make_report(options, database):
    timestamps = database.keys()
    fixed_time = [time.localtime(x) for x in timestamps]

    # Put the checkin and checkout times in a day-based dictionary
    days = {}
    for cur_time in fixed_time:
        if not cur_time.tm_yday in days:
            days[cur_time.tm_yday] = []
        days[cur_time.tm_yday].append(time.mktime(cur_time))

    # Make a report for each day
    for day in sorted(days.keys()):
        sorted_times = sorted(days[day])
        diff = 0
        for i in range(0,len(sorted_times), 2):
            try:
                diff += sorted_times[i+1] - sorted_times[i]
                if options.detail:
                    time_start = time.localtime(sorted_times[i])
                    time_stop = time.localtime(sorted_times[i+1])
                    start_text = time.strftime("%H:%M:%S", time_start)
                    stop_text = time.strftime("%H:%M:%S", time_stop)
                    print("Check in at {}, out at {}".format(start_text, stop_text))

            except:
                print("Not checked out yet")
        hours, minutes, seconds = get_hms(diff)
        current_day = time.strftime("%Y-%m-%d",time.localtime(days[day][0]))
        text = ": Time at work: "
        hours_text = "{:{fill}>2}:".format(int(hours), fill="0")
        minutes_text = "{:{fill}>2}:".format(int(minutes), fill="0")
        seconds_text = "{:{fill}>2}".format(int(seconds), fill="0")
        print("{}{}{}{}".format(current_day, text, minutes_text, seconds_text))

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
