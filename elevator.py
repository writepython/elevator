import os, sys, getopt, traceback

USAGE_MESSAGE = """Usage: elevator.py -i <input_file> -m <mode>
<input_file> is a text file containing multiple sets of commands as an input.
<mode> is the mode the elevator will operate in throughout the application lifecycle. Options are "a" and "b".
"""

def mode_a(command_sets):
    distance_travelled = 0
    for command_set in command_sets:
        initial_floor, colon, commands = command_set.partition(':')
        commands = [ [ int(command.split('-')[0]), int(command.split('-')[1]) ] for command in commands.split(',') ]
            
def main(argv):
    input_file = None
    mode = None
    command_sets = []
    try:
        opts, args = getopt.getopt(argv, "i:m:" )
    except getopt.GetoptError:
        print USAGE_MESSAGE
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            input_file = arg
        if opt == "-m":
            if arg in ('a', 'A'):
                mode = 'a'
            elif arg in ('b', 'B'):
                mode = 'b'
    if not input_file or not mode:
        print USAGE_MESSAGE
        sys.exit(2)
    with open(input_file) as f:
        command_sets = [ line.strip() for line in f.readlines() if line.strip() ]
    if not command_sets:
        print "No command sets to run."
    else:
        print "Found %d set(s) of commands." % len(command_sets)
        print "Operating in mode: %s" % mode
        if mode == 'a':
            mode_a(command_sets)
    
if __name__ == "__main__":
    main(sys.argv[1:])    
