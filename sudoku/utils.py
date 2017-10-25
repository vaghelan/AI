rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

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
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
diagonal_units = diagonal ('ABCDEFGHI', '123456789')
diagonal_set = set()
for m in diagonal_units:
    for i in m:
        diagonal_set.add(i)
diagonal_list = list(diagonal_set) 
print (diagonal_list)

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


# WARNING! We've modified this function to return '123456789' instead of '.' for boxes with no value.
# Look at the explanation above in the text.
def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

