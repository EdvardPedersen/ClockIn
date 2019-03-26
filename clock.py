#!/usr/bin/env python3
'''
Application for measuring time spent at work, and time spent
in front of the computer.

Designed to be activated on unlocking the screen, and deactivated
on locking the screen.
'''

import time
import pickle
import argparse

def parse_arguments():
    '''
    Parses command-line arguments, returns an options object
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkin", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--detail", action="store_true")
    return parser.parse_args()


def get_hms(seconds):
    '''
    Given a number of seconds, return the hours, minutes and seconds
    '''
    hour, remainder = divmod(seconds, 60*60)
    minute, second = divmod(remainder, 60)

    hours_text = "{:{fill}>2}:".format(int(hour), fill="0")
    minutes_text = "{:{fill}>2}:".format(int(minute), fill="0")
    seconds_text = "{:{fill}>2}".format(int(second), fill="0")
    return "".join([hours_text, minutes_text, seconds_text])


def order_times_by_day(times):
    '''
    Sort the list of times into a dictionary using days as
    the key
    '''
    days = {}
    for cur_time in times:
        if not cur_time.tm_yday in days:
            days[cur_time.tm_yday] = []
        days[cur_time.tm_yday].append(time.mktime(cur_time))
    return days


def make_report_for_single_day(day_key, days, options):
    '''
    Make a report for a single day, given by day_key,
    from the list of days in days, and the options
    '''
    sorted_times = sorted(days[day_key])
    diff = 0
    for i in range(0, len(sorted_times), 2):
        try:
            diff += sorted_times[i+1] - sorted_times[i]
            if options.detail:
                time_start = time.localtime(sorted_times[i])
                time_stop = time.localtime(sorted_times[i+1])
                start_text = time.strftime("%H:%M:%S", time_start)
                stop_text = time.strftime("%H:%M:%S", time_stop)
                print("Check in at {}, out at {}".format(start_text, stop_text))

        except IndexError:
            print("Not checked out yet")
    current_day = time.strftime("%Y-%m-%d", time.localtime(days[day_key][0]))
    text = ": Time at computer: "

    hms = get_hms(diff)
    print("{}{}{}".format(current_day, text, hms))

    full_diff = max(sorted_times) - min(sorted_times)
    hms = get_hms(full_diff)
    print("{}: Total work time: {}".format(current_day, hms))


def make_report(options, database):
    '''
    Given options and database, make a report for each day
    printed to stdout
    '''
    timestamps = database.keys()
    fixed_time = [time.localtime(x) for x in timestamps]
    days = order_times_by_day(fixed_time)

    # Make a report for each day
    for day in sorted(days.keys()):
        make_report_for_single_day(day, days, options)


def get_database():
    '''
    Load database from pickled object
    '''
    database = pickle.load(open("timekeep.p", "rb"))
    return database


def note_time(options, database):
    '''
    Register a new time in the database, called whenever a checkin or
    checkout are performed
    '''
    # Prevent erronous check in/out to preserve database
    last_action = database[next(reversed(database))][0]
    if last_action == 'checkin' and options.checkin:
        exit("You are already checked in!")
    elif last_action == 'checkout' and not options.checkin:
        exit("You have already checked out!")

    now = time.time()
    database[now] = []

    if options.checkin:
        database[now].append('checkin')
    else:
        database[now].append('checkout')

    pickle.dump(database, open("timekeep.p", "wb"))

def main():
    '''
    Main execution path when running standalone
    '''
    args = parse_arguments()
    data = get_database()
    if args.report:
        make_report(args, data)
    else:
        note_time(args, data)

if __name__ == "__main__":
    main()
