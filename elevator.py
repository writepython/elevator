import sys, getopt

USAGE_MESSAGE = """Usage: python elevator.py -i <input_file> -m <mode>
<input_file> is a text file containing multiple sets of commands as an input.
<mode> is the mode the elevator will operate in throughout the application lifecycle. Options are "a" and "b".
"""

def mode_a(command_sets):
    for command_set in command_sets:
        distance_travelled = 0
        output_list = []
        initial_floor, colon, commands_string = command_set.partition(':')
        current_floor = int(initial_floor)
        output_list.append(current_floor)        
        commands = [ [ int(command.split('-')[0]), int(command.split('-')[1]) ] for command in commands_string.split(',') ]
        for start, end in commands:
            if start != current_floor:
                output_list.append(start)
            output_list.append(end)            
            distance_to_start = abs(current_floor - start)
            distance_to_end = abs(start - end)
            distance_travelled = distance_travelled + distance_to_start + distance_to_end
            current_floor = end
        output_list.append("(%d)" % distance_travelled)
        print " ".join( [str(x) for x in output_list] )

def mode_b(command_sets):
    for command_set in command_sets:
        distance_travelled = 0
        output_list = []
        initial_floor, colon, commands_string = command_set.partition(':')
        current_floor = int(initial_floor)
        output_list.append(current_floor)
        # Group the commands into batches based on direction
        batches = []
        current_batch = []
        last_known_direction = 'up'
        for cmd in commands_string.split(','):
            command_split = cmd.split('-')
            start = int(command_split[0])
            end = int(command_split[1])
            if start < end:
                direction = 'up'
            elif end < start:
                direction = 'down'
            command = dict(start=start, end=end, direction=direction)
            if direction == last_known_direction:
                current_batch.append(command)
            else:
                last_known_direction = direction
                if current_batch:
                    batches.append(current_batch)
                current_batch = [ command ]
        batches.append(current_batch)
        # Process each batch
        for batch in batches:
            direction = batch[0].get('direction')
            floors_hit = []
            for command in batch:
                floors_hit.append(command.get('start'))
                floors_hit.append(command.get('end'))
            if direction == 'up': 
                floors_hit = sorted( list(set(floors_hit)) )
            elif direction == 'down':
                floors_hit = sorted( list(set(floors_hit)), reverse=True )
            start = floors_hit.pop(0)
            end = floors_hit.pop(-1)                
            if start != current_floor:
                output_list.append(start)
            for floor in floors_hit:
                output_list.append(floor)
            output_list.append(end)
            distance_to_start = abs(current_floor - start)
            distance_to_end = abs(start - end)
            distance_travelled = distance_travelled + distance_to_start + distance_to_end
            current_floor = end
        output_list.append("(%d)" % distance_travelled)
        print " ".join( [str(x) for x in output_list] )
        
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
        elif mode == 'b':
            mode_b(command_sets)            
    
if __name__ == "__main__":
    main(sys.argv[1:])    
