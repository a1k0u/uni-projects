from pygame import init, display

# display
init()

display_info = display.Info()
width = display_info.current_w
height = display_info.current_h

fps = 600

# color
background_color = (0, 0, 0)
