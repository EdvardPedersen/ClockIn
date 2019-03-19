import time, pickle

def get_database(options):
    # Load database from pickled object
    #with open("timekeep.p", "wb") as f:
    #    pickle.dump({123: ["checkin"]}, f)
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
    
    # Write to database
    merged = {**database, **data}
    print (merged)
    pickle.dump(merged, open("timekeep.p", "wb"))
