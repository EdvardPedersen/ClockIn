import time, pickle
from collections import OrderedDict

def get_database(options):
    # Load database from pickled object
    database = pickle.load(open("timekeep.p", "rb"))
    return database

def note_time(options, database):
    # Funny logic to check if your are screwing up
    if database[next(reversed(database))][0] == 'checkin' and options.checkin:
        exit("You are already checked in!")
    if database[next(reversed(database))][0] == 'checkout' and not options.checkin:
        exit("You have already checked out!")

    now = time.time()
    database[now] = []

    # Check if checkin or check out, append as first element to list
    if options.checkin:
        database[now].append('checkin')
    else:
        database[now].append('checkout')
    
    # Write to database
    pickle.dump(database, open("timekeep.p", "wb"))
