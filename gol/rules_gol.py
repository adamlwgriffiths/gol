import numpy

def count_neighbours( cells, wrap ):
    # we use "numpy.roll" to move the entire board at once
    # ->
    left = numpy.roll( cells, 1, axis = 0 )
    # <-
    right = numpy.roll( cells, -1, axis = 0 )
    
    # \/
    up = numpy.roll( cells, 1, axis = 1 )
    # ^
    down = numpy.roll( cells, -1, axis = 1 )
    
    # up left
    left_up = numpy.roll( left, 1, axis = 1 )
    # up right
    right_up = numpy.roll( right, 1, axis = 1 )
    
    # down left
    left_down = numpy.roll( left, -1, axis = 1 )
    # down right
    right_down = numpy.roll( right, -1, axis = 1 )
    
    # check if wrapping is enabled
    x_wrap = True if wrap != None and wrap[ 0 ] == True else False
    y_wrap = True if wrap != None and wrap[ 1 ] == True else False
 
    # if wrapping is not enabled
    # we need to zero out the wrapped columns
    if x_wrap == False:
        # left
        left[ 0, : ] = 0
        left_up[ 0, : ] = 0
        left_down[ 0, : ] = 0
        
        # right
        right_up[-1, : ] = 0
        right[-1, : ] = 0
        right_down[-1, : ] = 0
    if y_wrap == False:
        # top
        up[ :, 0 ] = 0
        left_up[ :, 0 ] = 0
        right_up[ :, 0 ] = 0
        
        # bottom
        down[ :,-1 ] = 0
        left_down[ :,-1 ] = 0
        right_down[ :,-1 ] = 0
    
    counts = left + right + \
        up + down + \
        left_up + right_up + \
        left_down + right_down
    
    return counts

def apply_rules( cells, counts ):
    # apply conway's rules
    # using numpy.where
    
    new_cells = numpy.array( cells )
    
    # rule 1: < 2 neighbour = dead
    new_cells = numpy.where( counts < 2, [0], new_cells )
    
    # rule 2: 2 - 3 neighbours = alive
    pass
    
    # rule 3: > 3 neighbours = dead
    new_cells = numpy.where( counts > 3, [0], new_cells )
    
    # rule 4: 3 neighbours = alive
    new_cells = numpy.where( counts == 3, [1], new_cells )
    
    return new_cells

def apply( cells, wrap = None ):
    assert cells.ndim == 2
    
    # we roll the cells around in 8 directions and add them up
    # this lets us count ALL cells neighbours in one operation
    counts = count_neighbours( cells, wrap )
    
    # apply conway's rules
    new_cells = apply_rules( cells, counts )
    
    return new_cells


if __name__ == '__main__':
    cells = numpy.random.randint( 2, size = (10,10) )
    print "New cells"
    print cells
    
    for i in range(5):
        cells = apply( cells, wrap = (True, True) )
        print "Generation ",i
        print cells
    pass
