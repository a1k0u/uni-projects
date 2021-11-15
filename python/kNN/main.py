import pygame
import pygame.gfxdraw
import pygame_widgets

import widgets
import config as c
import app_math as m


class Application:
    def __init__(self):
        self.application = True
        self.classify_reset_flag = True

        self.points = []
        self.classify_blocks = []

        self.menu_rect = pygame.Rect(0, 0, c.width, c.menu_height)

        self.mouse = (0, 0)
        self.user_color_index = 0

        self.parameters = c.parameters
        self.colors = c.point_colors[: self.parameters["colors"]]

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((c.width, c.height), pygame.FULLSCREEN)
        pygame.display.set_caption(c.CAPTION)
        pygame.mouse.set_visible(False)

        self.sliders_widget = widgets.create_slider_widgets(self.screen)
        self.text_widget = widgets.create_text_widgets(self.screen)
        self.toggle_widget = widgets.create_toggle_widget(self.screen)
        self.text_mode = widgets.create_text_mode_widget(self.screen)
        self.button_widget = widgets.create_color_buttons(len(self.colors))

    def loop(self):
        while self.application:
            self.update()
            self.draw()
            self.handlers()

            self.draw_cursor()

            self.clock.tick(c.FPS)
            pygame.display.update()

    def handlers(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.application = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_rect.collidepoint(self.mouse):
                    for i, button in enumerate(self.button_widget):
                        if button.collidepoint(event.pos):
                            self.user_color_index = i
                else:
                    self.points.append(
                        [
                            *event.pos,
                            self.colors[self.user_color_index]
                            if self.toggle_widget.getValue()
                            else m.find_common_color(
                                self.points,
                                m.find_nearest(
                                    self.points,
                                    self.parameters["kNN"],
                                    *event.pos,
                                ),
                            ),
                        ]
                    )
                    self.classify_reset_flag = True
        pygame_widgets.update(events)

    def update(self):
        self.mouse = m.get_pos()
        self.set_parameters()

    def set_parameters(self):
        for i, key in enumerate(self.parameters):
            if self.parameters[key] != self.sliders_widget[i].getValue():
                self.parameters[key] = self.sliders_widget[i].getValue()

                self.colors = c.point_colors[: self.parameters["colors"]]
                self.user_color_index = min(self.user_color_index, len(self.colors) - 1)

                self.classify_reset_flag = True
                self.button_widget = widgets.create_color_buttons(len(self.colors))

                self.points = m.generate_points(
                    self.menu_rect.height, self.colors, self.parameters["points"]
                )

    def draw(self):
        self.draw_background()

        if self.toggle_widget.getValue():
            if self.classify_reset_flag:
                self.classify_blocks = m.classify_area(
                    self.points, self.parameters["kNN"]
                )
                self.classify_reset_flag = False
            self.draw_classify_area()
        elif not self.menu_rect.collidepoint(self.mouse):
            self.draw_lines()

        self.draw_points()
        self.draw_menu_bar()

        self.output_info()

    def draw_background(self):
        self.screen.fill(c.black)

    def draw_classify_area(self):
        for pos_x, pos_y, color in self.classify_blocks:
            pygame.gfxdraw.box(
                self.screen,
                [
                    pos_x,
                    pos_y,
                    c.width_block,
                    c.width_block,
                ],
                color,
            )

    def draw_lines(self):
        nearest_points = m.find_nearest(
            self.points, self.parameters["kNN"], *self.mouse
        )
        for index in nearest_points:
            pos = (self.points[index][0], self.points[index][1])
            pygame.gfxdraw.line(
                self.screen,
                *self.mouse,
                *pos,
                c.white_alpha_64,
            )
            self.draw_gfx_circle(*pos, c.line_radius, c.white_alpha_128)

    def draw_gfx_circle(self, pos_x: int, pos_y: int, radius: int, color: tuple):
        pygame.gfxdraw.aacircle(self.screen, pos_x, pos_y, radius, color)
        pygame.gfxdraw.filled_circle(self.screen, pos_x, pos_y, radius, color)

    def draw_points(self):
        for pos_x, pos_y, color in self.points:
            if self.toggle_widget.getValue():
                changed_color = m.change_color(color, lambda a: a, c.MAKE_DARKER)

                self.draw_gfx_circle(
                    pos_x, pos_y, c.point_outline_radius, c.outline_color
                )
                self.draw_gfx_circle(pos_x, pos_y, c.point_radius, changed_color)
                self.draw_gfx_circle(pos_x - 1, pos_y - 1, c.point_radius - 1, color)
            else:
                pygame.gfxdraw.circle(self.screen, pos_x, pos_y, c.point_radius, color)

    def draw_menu_bar(self):
        pygame.gfxdraw.box(self.screen, self.menu_rect, c.black)
        if self.toggle_widget.getValue():
            self.draw_color_buttons()

    def draw_color_buttons(self):
        for i, button in enumerate(self.button_widget):
            pos_x, pos_y, *width = button
            radius = width[0] // 2
            pos_x += radius
            pos_y += radius

            self.draw_gfx_circle(pos_x, pos_y, radius, self.colors[i])
            if i == self.user_color_index:
                self.draw_gfx_circle(
                    pos_x,
                    pos_y,
                    radius + c.pressed_button_radius,
                    c.white,
                )
                self.draw_gfx_circle(
                    pos_x,
                    pos_y,
                    radius,
                    m.change_color(self.colors[i], lambda a: a, c.MAKE_DARKER_64),
                )

    def draw_cursor(self):
        self.draw_gfx_circle(*self.mouse, c.cursor_outline_radius, c.black)
        self.draw_gfx_circle(*self.mouse, c.cursor_radius, c.white)

    def output_info(self):
        for i, key in enumerate(self.parameters):
            self.text_widget[i].setText(
                f"{c.SLIDERS_TEXT} {key}: {self.parameters[key]}"
            )
        self.text_widget[-1].setText(
            c.EDIT_MODE_TEXT if self.toggle_widget.getValue() else c.SPIDER_MODE_TEXT
        )
        self.text_mode.setText(
            c.BUTTONS_TEXT if self.toggle_widget.getValue() else c.NON_BUTTONS_TEXT
        )


if __name__ == "__main__":
    app = Application()
    app.loop()
    pygame.quit()
