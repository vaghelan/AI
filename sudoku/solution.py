
# coding: utf-8

# In[671]:


# config parameters

import sys

DIAGONAL_ENABLED = True
DEBUG = False


rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s + t for s in a for t in b]


def diagonal(a, b):
    index = 0
    d_set = []
    d = []
    for s in a:
       d.append( s + b[index] )
       index = index + 1
    d_set.append(d)
    
    index = 0
    d = []
    for s in a[::-1]:
       d.append( s + b[index] )
       index = index + 1
    d_set.append(d)
    
    return d_set

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

diagonal_units = diagonal ('ABCDEFGHI', '123456789')
#print (diagonal_units)
diagonal_set = set()
for m in diagonal_units:
    for i in m:
        diagonal_set.add(i)
diagonal_list = list(diagonal_set) 
#print ("Diagonal list")
#print (diagonal_list)
#print ("Diagonal list \n")

#print ("Diagonal units")
#print (diagonal_units)
#print ("Diagonal units \n")

unitlist = row_units + column_units + square_units

if DIAGONAL_ENABLED:
    unitlist = unitlist + diagonal_units
    #print (unitlist) 
    
    
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

#e = 'I5'
#print (units[e])
#print (len(units[e]))


# In[672]:

#print (units)
for a_box in boxes:
        for a_peer in peers[a_box]:
            if a_box == a_peer:
               print ("Fatal error - Diagonal units are not set properly {} {} ".format(a_box, a_peer))
               sys.exit(1)


# In[673]:

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins_backend_v2(values, num):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    
    for unit in unitlist:
        # find all boxes which has two digits
        box_dict = {}
        #del_keys = []
        for a_box in unit:
            key = values[a_box]
            if len(key) == num:
                if key not in box_dict:
                    box_dict[key] = [a_box]
                else:
                    box_dict[key].append(a_box)
        
        #print ("box dict = {}".format(box_dict))
        
        box_positions = set()
        naked_twins = set()
        
        for k, v in box_dict.items():
            if len(v) != num:
                continue
            for ve in v:   
                box_positions.add(ve)
            for d in k:     
                naked_twins.add(d)
        
        if len(box_positions) == 0:
            #print ("No naked twins....\n")
            continue
        
        box_positions = set(unit) - box_positions     
        
        for a_box in box_positions:
            for d in naked_twins:
                values[a_box] = values[a_box].replace(d, '')

    return values 

def naked_twins_backend_v1(values, num):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        # find all boxes which has two digits
        two_digit_boxes = [box for box in unit if len(values[box]) == num]
        box_dict = {}
        for a_box in two_digit_boxes:
            if values[a_box] not in box_dict:
               box_dict[values[a_box]] = [ a_box ]
            else:
               box_dict[values[a_box]].append(a_box)
            
        for key in  box_dict:
            if len(box_dict[key]) == num :
               digits = list(key)
               for a_box in unit:
                    if a_box not in box_dict[key]:
                        for d in digits:
                            values[a_box] = values[a_box].replace(d, '')
                            

    return values 


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.
    

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    result = {}
    flattened_row_units = [val for sublist in row_units for val in sublist]
    index = 0
    for i in grid:
        if i == ".":
            result[flattened_row_units[index]] = '123456789'
        else:
            result[flattened_row_units[index]] = i
        index = index + 1    
    return result

def eliminate_v1(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    
    for a_box in values:
        if len(values[a_box]) == 1:
            continue
        my_peers = peers[a_box]
        for a_peer in my_peers:
            #if a_box == a_peer:
            #    continue
            if len(values[a_peer]) == 1:
                values[a_box] = values[a_box].replace(values[a_peer], '')
    return values

def eliminate_default(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def eliminate(values):
    return eliminate_v1(values)

def only_choice_v1(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for a_box in units:
        # for row_unit, col unit and square_unit
        for a_neighbor_set in units[a_box]: 
            temp = {}
            # for each member in row_unit, col unit and square_unit
            for a_neighbor in a_neighbor_set:
                for v in values[a_neighbor]:
                    if v not in temp: 
                        temp[v] = [ a_neighbor ]
                    else:
                        temp[v].append(a_neighbor)
            for v in temp:
                if len(temp[v]) == 1:
                    values[temp[v][0]] = v
    
    return values

def only_choice_v2(values):
    
    for unit in unitlist: # [ A1, A2]
        d = {}
        for item in unit:  # [ A1 ]
            for box_value in values[item]: # "1234"
                for digit in box_value:
                    if digit not in d:
                        d[digit] = [ item ]
                    else:
                        d[digit].append(item)
        for s in d:
            if len(d[s]) == 1:
                a_box = d[s][0]
                if len(values[a_box]) > 1:
                    values[a_box] = s
                    my_peers = peers[a_box]
                    for a_peer in my_peers:
                        values[a_peer] = values[a_peer].replace(s, '')
    return values

def only_choice_default(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
        

def only_choice(values):
    return only_choice_v2(values)

def find_zero_length_box(values):
    return len([ box for box in values.keys() if len(values[box]) == 0 ] ) != 0

def reduce_puzzle(values):

    iter_num = 1
    orig_values = None

    while True:
        if DEBUG:
            print ("Iteration number {}".format(iter_num))
        orig_values = values.copy()

        if DEBUG:
            display(values)

        if DEBUG:
            temp_values = values.copy()
        
        values = eliminate(values)

        if DEBUG:
            if find_zero_length_box(values):
                print ("\n Fatal error...zero length values after eliminate \n")
                display(values)
                return (-1, values)

            if temp_values != values:
                print ("\n After eliminate values \n")
                display(values)
                temp_values = values.copy()

        values = only_choice(values)

        if DEBUG:
            if find_zero_length_box(values):
                print ("\n Fatal error...zero length values after only choice \n")
                display(values)
                return (-1, values)

            if temp_values != values:
                print ("\n After only choice values \n")
                display(values)
                temp_values = values.copy()

        values = naked_twins_backend_v2(values, 2)

        if DEBUG:
            if find_zero_length_box(values):
                print ("\n Fatal error...zero length values after naked twins \n")
                display(values)
                return (-1, values)

            if temp_values != values:
                print ("\n After naked twins \n")
                display(values)
                temp_values = values.copy()


        values = naked_twins_backend_v2(values, 3)

        if DEBUG:
            if find_zero_length_box(values):
                print ("\n Fatal error...zero length values  after naked triplets\n")
                display(values)
                return (-1, values)

            if temp_values != values:
                print ("\n After naked triplets \n")
                display(values)
                temp_values = values.copy()

        after_num_solved_values = len([ box for box in values.keys() if len(values[box]) == 1 ] )
        if after_num_solved_values == len(boxes):
            print ("Solution is Reached!!!")
            return (0, values )
            
        if values == orig_values:
            print ("Not making any progress")
            break

        if DEBUG:
            print ("##############\n")
        
        iter_num = iter_num + 1

    
    print ("Solution is NOT reached ....!!!")
     # Sanity check, return False if there is a box with zero available values:
    if len([box for box in values.keys() if len(values[box]) == 0]):
        print ("Reason: Fatal Error - Found 0 len boxes ....!!!")
        return (-1, values)

    print ("Reason: Could not reduce further!!!")
    return (-2, values)
    

def naked_twins(values):

    iter_num = 1
    while True:

        if DEBUG:
            print ("Iteration number {}".format(iter_num))
        orig_values = values.copy()

        values = naked_twins_backend_v2(values, 2)

        if DEBUG:
            if find_zero_length_box(values):
                print ("\n Fatal error...zero length values  after naked twins\n")
                display(values)
                return (-1, values)

            if orig_values != values:
                print ("\n After naked twins \n")
                display(values)
        
        after_num_solved_values = len([ box for box in values.keys() if len(values[box]) == 1 ] )
        if after_num_solved_values == len(boxes):
             print ("Solution is Reached!!!")
             break

        if values == orig_values:
            if DEBUG:
                print ("Not making any progress for Naked Twins \n")
            break

        iter_num = iter_num + 1

    if DEBUG:

        if after_num_solved_values == len(boxes):
            print ("Naked Twins Solution is Reached!!!")
        else:
            print ("Naked Twins Solution is NOT reached ....!!!")
      
        
    return values    

def search(values):
    
    # try to reduce the grid
    (result, values) = reduce_puzzle(values)
    
    # Search has failed ..this can happen when we try to search with DFS and recursively called search
    # this means we have selected wrong value for search
    # OR some bug in the code
    if result == -1 :
        return (result, values) 
    
    if result == 0: # We have cracked it!!
        return (result, values) 
    
    #find boxes with length
    min_len = 0
    boxes_dict_with_length = {}
    for box in values.keys():
        key = len(values[box])
        if key > 1:
             if min_len == 0 or min_len > key:
                min_len = key
             if key not in boxes_dict_with_length:
                boxes_dict_with_length[key] = [ box ]
             else:
                boxes_dict_with_length[key].append(box)
     
    min_length_box_num = boxes_dict_with_length[min_len][0]

    for value in values[min_length_box_num]:
        new_sudoku = values.copy()
        #print ("Current state of sudoku \n")
        display(values)
        if DEBUG:
            print ("Trying DFS path with {} single value {} on box = {}".format(value, values[min_length_box_num], min_length_box_num))
        new_sudoku[min_length_box_num] = value
        (result, new_values) = search(new_sudoku)
        if result != 0:
            continue # try next node in DFS
        return (0, new_values) 
    


# In[674]:

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #print ("\n######Before Grid values Call#############\n" )
    values = grid_values(grid)
    #print ("\n######After Grid values Call#############\n" )

    print ("\n#########Sudoku Problem########\n" )

    display(values)

    print ("\n#########Sudoku Problem########\n")
    
    (result, values) = search(values)
    if result == -2: # search also failed to reduce
        print ("FATAL Error : Search failed to reduce")
        return values
    if result == -1: # search also failed to reduce
        print ("FATAL Error : Search failed to reduce and ended up with 0 len boxes")  
        return values
    
    print ("\nHurray !!! Cracked Sudoku !!!\n")
    if __name__ != '__main__':
        display(values)
    
    return values
    
    # In[676]:

if __name__ == '__main__':
    #diag_sudoku_grid = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
    
    #diag_sudoku_grid = '1.4.9..68956.18.34..84.695151.....868..6...1264..8..97781923645495.6.823.6.854179'
    #hard sudoku
    #diag_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    #diag_sudoku_grid = '381..6....7...9.....9......1..5..79.9.4.8.2.1.67..1..5......9.....2...8....9..416'
    #diag_sudoku_grid = '...........4..32.6.9258....6.....9149.......8827.....5....5287.7.94..5...........'
    
    # diagonal grid
    #diagonal_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    # bad example where I spent lot of time debugging....
    #diagonal_grid  = '.5.......6.3..24...7.1....38.4.....7.........3.....2.97....1.2...96..7.1.......4.'
    
    #if DIAGONAL_ENABLED :
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    solution = solve(diag_sudoku_grid)
    display(solution)
    

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')


