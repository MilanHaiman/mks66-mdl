import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    clear_screen(screen)
    clear_zbuffer(zbuffer)
    systems = stack

    polygons = coords1
    edges = coords

    print symbols
    for command in commands:
      line = command['op']
      if line == 'sphere':
        #print 'SPHERE\t' + str(command['args'])
        add_sphere(polygons,float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),float(command['args'][3]), step_3d)
        matrix_mult( systems[-1], polygons )
        if command['constants'] == None:
          r = reflect
        else:
          r = command['constants']
        draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, r)
        polygons = []

      elif line == 'torus':
        #print 'TORUS\t' + str(command['args'])
        add_torus(polygons,
                  float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                  float(command['args'][3]), float(command['args'][4]), step_3d)
        matrix_mult( systems[-1], polygons )
        if command['constants'] == None:
          r = reflect
        else:
          r = command['constants']
        draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, r)
        polygons = []

      elif line == 'box':
        #print 'BOX\t' + str(command['args'])
        add_box(polygons,
                float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                float(command['args'][3]), float(command['args'][4]), float(command['args'][5]))
        matrix_mult( systems[-1], polygons )
        if command['constants'] == None:
          r = reflect
        else:
          r = command['constants']
        draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, r)
        polygons = []

      elif line == 'circle':
        #print 'CIRCLE\t' + str(command['args'])
        add_circle(edges,
                   float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                   float(command['args'][3]), step)
        matrix_mult( systems[-1], edges )
        draw_lines(edges, screen, zbuffer, color)
        edges = []

      elif line == 'hermite' or line == 'bezier':
        #print 'curve\t' + line + ": " + str(command['args'])
        add_curve(edges,
                  float(command['args'][0]), float(command['args'][1]),
                  float(command['args'][2]), float(command['args'][3]),
                  float(command['args'][4]), float(command['args'][5]),
                  float(command['args'][6]), float(command['args'][7]),
                  step, line)
        matrix_mult( systems[-1], edges )
        draw_lines(edges, screen, zbuffer, color)
        edges = []

      elif line == 'line':
        #print 'LINE\t' + str(command['args'])

        add_edge( edges,
                  float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                  float(command['args'][3]), float(command['args'][4]), float(command['args'][5]) )
        matrix_mult( systems[-1], edges )
        draw_lines(eges, screen, zbuffer, color)
        edges = []

      elif line == 'scale':
        #print 'SCALE\t' + str(command['args'])
        t = make_scale(float(command['args'][0]), float(command['args'][1]), float(command['args'][2]))
        matrix_mult( systems[-1], t )
        systems[-1] = [ x[:] for x in t]

      elif line == 'move':
        #print 'MOVE\t' + str(command['args'])
        t = make_translate(float(command['args'][0]), float(command['args'][1]), float(command['args'][2]))
        matrix_mult( systems[-1], t )
        systems[-1] = [ x[:] for x in t]

      elif line == 'rotate':
        #print 'ROTATE\t' + str(command['args'])
        theta = float(command['args'][1]) * (math.pi / 180)
        if command['args'][0] == 'x':
          t = make_rotX(theta)
        elif command['args'][0] == 'y':
          t = make_rotY(theta)
        else:
          t = make_rotZ(theta)
        matrix_mult( systems[-1], t )
        systems[-1] = [ x[:] for x in t]

      elif line == 'push':
        systems.append( [x[:] for x in systems[-1]] )

      elif line == 'pop':
        systems.pop()

      elif line == 'display' or line == 'save':
        if line == 'display':
          display(screen)
        else:
          save_extension(screen, command['args'][0]+".png")
      print command
