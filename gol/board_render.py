from pyglet.gl import *
import numpy


class BoardRenderer( object ):
    
    def __init__( self, board ):
        super( BoardRenderer, self ).__init__()
        
        self.board = board
        self.grid = self._create_grid( self.board )
        self.cell = self._create_cell()

    def render( self ):
        # draw the grid
        glLineWidth( 1.0 )
        glColor3f( 1.0, 1.0, 1.0 )
        glDisable( GL_LIGHTING )
        
        glCallList( self.grid )
        
        # draw any cells
        glColor3f( 1.0, 0.0, 0.0 )
        
        indices = numpy.where( self.board == 1 )
        indices = numpy.dstack( (indices[ 0 ], indices[ 1 ]) )[ 0 ]
        
        for cell in indices:
            glLoadIdentity()
            pos = numpy.array( [ float(cell[ 0 ]), float(cell[ 1 ]) ], dtype = numpy.float )

            pos *= [ 2.0 / self.board.shape[ 0 ], 2.0 / self.board.shape[ 1 ] ]
            pos += [-1.0,-1.0 ]
            
            glTranslatef( pos[ 0 ], pos[ 1 ], 0.0 )            

            glCallList( self.cell )

    def _create_cell( self ):
        display_list = glGenLists( 1 )
        glNewList( display_list, GL_COMPILE )
        
        self._draw_cell()
        
        glEndList()
        
        return display_list

    def _draw_cell( self ):
        glBegin( GL_QUADS )
        
        x_size, y_size = 2.0 / self.board.shape[ 0 ], 2.0 / self.board.shape[ 1 ]
        
        glVertex2f( 0.0, 0.0 )
        glVertex2f( x_size, 0.0 )
        glVertex2f( x_size, y_size )
        glVertex2f( 0.0, y_size )
        
        glEnd()

    def _create_grid( self, board ):
        display_list = glGenLists( 1 )
        glNewList( display_list, GL_COMPILE )
        
        self._draw_grid( board )
        
        glEndList()
        
        return display_list

    def _draw_grid( self, board ):        
        x_positions = numpy.array( [ x for x in range( board.shape[ 0 ] + 1 ) ], dtype = numpy.float )
        y_positions = numpy.array( [ y for y in range( board.shape[ 1 ] + 1 ) ], dtype = numpy.float )
        
        min_x, max_x = float(x_positions.min()), float(x_positions.max())
        min_y, max_y = float(y_positions.min()), float(y_positions.max())
        
        # we need to now splice these int x,y,z vertices
        # we need 2 vertices per line
        x_lines = numpy.dstack(
            (
                numpy.repeat( x_positions, 2 ),
                [ min_y, max_y ] * len(x_positions),
                [ 0.0, 0.0 ] * len(x_positions)
                )
            )
        y_lines= numpy.dstack(
            (
                [ min_x, max_x ] * len(y_positions),
                numpy.repeat( y_positions, 2 ),
                [ 0.0, 0.0 ] * len(y_positions)
                )
            )
        # join our two arrays together
        vertices = numpy.concatenate( (x_lines, y_lines) )

        # move the vertices so they are between -1.0 - 1.0
        vertices *= [ 2.0 / board.shape[ 0 ], 2.0 / board.shape[ 1 ], 1.0 ]
        vertices += [-1.0,-1.0,-10.0 ]
        
        vertices.shape = (-1,3)
        
        # render the vertices
        glBegin( GL_LINES )
        
        for vertex in vertices:
            #glVertex3f( vertex[ 0 ],vertex[ 1 ],vertex[ 2 ])
            glVertex2f( vertex[ 0 ],vertex[ 1 ])
        
        glEnd()


if __name__ == '__main__':
    import rules_gol
    
    # Direct OpenGL commands to this window.
    window = pyglet.window.Window()
    
    glEnableClientState(GL_VERTEX_ARRAY)
    
    size = (50,50)
    board = numpy.random.randint( 2, size = size )
    renderer = BoardRenderer( board )
    
    @window.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        global renderer
        renderer.render()
    
    @window.event
    def on_key_press(symbol, modifiers):
        global renderer
        global size
        if symbol == pyglet.window.key.SPACE:
            renderer.board = numpy.random.randint( 2, size = size )
    
    def update( delta ):
        global renderer
        renderer.board = rules_gol.apply( renderer.board, wrap = (True, True) )
    
    # update our board at 1Hz
    pyglet.clock.schedule_interval(
        update,
        1.0 / 30.0
        )
    
    pyglet.app.run()
