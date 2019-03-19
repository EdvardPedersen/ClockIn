import time, pickle

def get_database(options):
    # Load database from pickled object
    database = pickle.load(open("timekeep.p", "rb"))
    return database

def note_time(options, database):
    # Set time and create dict entry
    now = time.time()
    data = {now: []}

    # Check if checkin or check out, append as first element to list
    if options.checkin:
        data[now].append('checkin')
    else:
        data[now].append('checkout')
    
    return data
