import edvard
import espen

if __name__ == "__main__":
    options = edvard.parse_arguments()
    database = espen.get_database(options)
    if options.type == "report":
        edvard.make_report(options, database)
    else:
        espen.note_time(options, database)

'''
parse_arguments - edvard
get_database - espen
make_report - edvard
note_time - espen


'''
