from pygame import init, display

# display
init()

display_info = display.Info()
width = display_info.current_w
height = display_info.current_h

fps = 600

# objects
gravity = 0, 1000

ball_parameters = {
    "amount": 30,
    "mass": 1,
    "radius": 7,
    "elasticity": 0.1,
    "friction": 1.0,
}

# color
background_color = (0, 0, 0)
