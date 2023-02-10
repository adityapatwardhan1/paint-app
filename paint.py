import pygame
import sys
import collections


class PaintApp:
    """Class representing the paint app.
    Supports draw, erase, fill, replace and clear operations.
    Supports 4 thicknesses of paintbrushes in 8 colors.
    """

    WINDOW_WIDTH = 450
    WINDOW_HEIGHT = 580

    def __init__(self):
        """Initializes app with window, paintbrush, and panel for color, brush thickness and tools
        (draw, erase, fill, replace and clear).
        :param self: The calling object/object being initialized
        :type self: PaintApp
        """
        pygame.init()
        self.background_color = (255, 255, 255)  # Screen has a white background
        self.current_tool = "Draw"  # current_tool can be Draw, Erase, Fill, Replace or Clear
        self.pb = PaintBrush()
        self.win = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))  # Draws window
        pygame.display.set_caption("Paint")
        self.win.fill(self.background_color)
        self.panel = Panel()  # Displays paintbrush thickness, paintbrush color and current_tool
        self.color_dict = self.panel.get_color_buttons()
        self.display_panel()
        pygame.display.update()

    def display_panel(self):
        """Displays the panel for color, brush thickness and tools (draw, erase, fill, replace and clear).
        :param self: The calling object
        :type self: PaintApp
        """
        self.panel.display(self.win)

    def det_brush_color(self, pos, color):
        """Determines the color of the paintbrush.
        :param self: The calling object
        :type self: PaintApp
        :param pos: The position of the cursor if the mouse is pressed, else None
        :type pos: tuple
        :param color: The color of the brush when the method was called
        :type color: tuple
        :returns: Current color of the brush
        :rtype: tuple
        """
        # Nothing has changed so the color hasn't changed
        if pos is None:
            return color
        # The cursor isn't hovering over the panel so the color hasn't changed
        if 0 <= pos[1] < self.WINDOW_WIDTH:
            return color
        color_buttons = self.panel.get_color_buttons()
        for x in color_buttons:
            # If the user is hovering over a color
            if color_buttons[x][1].collidepoint(pos[0], pos[1]):
                return color_buttons[x][0]
        return color

    def det_brush_th(self, pos, th):
        """
        Determines the thickness of the paintbrush.
        :param self: The calling object
        :type self: PaintApp
        :param pos: The position of the cursor if the mouse is pressed, else None
        :type pos: tuple
        :param th: The thickness of the brush when the method was called
        :type th: int
        :returns: Current thickness of the brush
        :rtype: int
        """
        # Nothing has changed so the thickness hasn't changed
        if pos is None:
            return th
        # The cursor isn't hovering over the panel so the thickness hasn't changed
        if 0 <= pos[1] < self.WINDOW_WIDTH:
            return th
        brush_buttons = self.panel.get_brush_buttons()
        for x in brush_buttons:
            # If the user is hovering over a button for thickness
            if brush_buttons[x][1].collidepoint(pos):
                return x
        return th

    def set_current_tool(self, current_tool):
        """
        Sets the tool the user is using.
        :param self: The calling object
        :type self: PaintApp
        :param current_tool: The current_tool when the method is called
        :type current_tool: str
        """
        self.current_tool = current_tool

    def get_current_tool(self, pos, current_tool):
        """
        Determines the tool the user is using.
        :param self: The calling object
        :type self: PaintApp
        :param pos: The position of the cursor if the mouse is pressed, else None
        :type pos: tuple
        :param current_tool: The current_tool when the method is called
        :type current_tool: str
        :returns: The current tool the user is using.
        :rtype: str
        """
        # Nothing has changed so the current_tool hasn't changed
        if pos is None:
            return current_tool
        # The cursor isn't hovering over the panel so the current_tool hasn't changed
        if 0 <= pos[1] < self.WINDOW_WIDTH:
            return current_tool
        tool_buttons = self.panel.get_tool_buttons()
        for x in tool_buttons:
            # If the user is pressing on a button for a new current_tool
            if tool_buttons[x][1].collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                return x
        return current_tool

    def get_click(self, pos):
        """
        Determines the position of the cursor.
        :param self: The calling object
        :type self: PaintApp
        :param pos: The position of the cursor when the method was called
        :type pos: tuple
        :returns: The position of the cursor.
        :rtype: tuple
        """
        pygame.event.pump()
        if pygame.mouse.get_pressed()[0]:
            return pygame.mouse.get_pos()
        return pos

    def user_wants_to_paint(self):
        """
        :param self: The calling object
        :type self: PaintApp
        :returns: Whether the user wants to paint.
        :rtype: bool
        """
        pygame.event.pump()
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.QUIT:
                return False
        return True

    def fill(self, start_pos, tar, repl):
        """
        Fills a region of the painting with the color tar.
        :param self: The calling object
        :type self: PaintApp
        :param start_pos: The starting position from which to fill the contiguous region.
        :type start_pos: tuple
        :param tar: The color of the region the user wants to fill.
        :type tar: tuple
        :param repl: The color the user wants to fill the region with/replace the current color with.
        :type repl: tuple
        """
        # Directions to search for pixels of color tar (target)
        dx = [-1, 0, 1, -1, 1, -1, 0, 1]
        dy = [-1, -1, -1, 0, 0, 1, 1, 1]
        # No pixels have been visited yet; visited pixels shouldn't be revisited
        visited = [[False for _ in range(self.WINDOW_WIDTH + 1)] for _ in range(self.WINDOW_WIDTH + 1)]
        pygame.event.pump()

        if 0 <= start_pos[0] < self.WINDOW_WIDTH and 0 <= start_pos[1] < self.WINDOW_WIDTH:
            # Target color is already the color to replace so do nothing
            if tar == repl:
                return
            # BFS algorithm
            bfs_queue = collections.deque()  # Queue storing pixels to visit
            bfs_queue.append((start_pos[0], start_pos[1]))
            while len(bfs_queue) > 0:
                top_point = bfs_queue.popleft()
                pygame.draw.rect(self.win, repl, (top_point[0], top_point[1], 1, 1))  # Change color of the pixel
                # Traverse neighboring pixels
                for i in range(8):
                    new_x = top_point[0] + dx[i]
                    new_y = top_point[1] + dy[i]
                    # Add neighboring pixel to the queue if it isn't in the queue and needs to be colored
                    if 0 <= new_x < self.WINDOW_WIDTH and 0 <= new_y < self.WINDOW_WIDTH and self.win.get_at(
                            (new_x, new_y)) == tar and not \
                            visited[new_x][new_y]:
                        bfs_queue.append((new_x, new_y))
                        visited[new_x][new_y] = True

            pygame.display.update()  # Update the screen once the region has been filled

    def draw(self, prev_pos, cur_pos):
        """
        Draws on the screen.
        :param self: The calling object
        :type self: PaintApp
        :param prev_pos: The position of the cursor before the method was called.
        :type prev_pos: tuple
        :param cur_pos: The position of the cursor when the method is called.
        :type cur_pos: tuple
        :return: The position of the cursor when the method is called.
        :rtype: tuple
        """
        return self.pb.draw(self.win, prev_pos, cur_pos, self.background_color)

    def replace(self, targetColor: tuple, replaceWith: tuple):
        """
        Changes all pixels of one color to another color.
        :param self: The calling object
        :type self: PaintApp
        :param targetColor: The color to replace.
        :type targetColor: tuple
        :param replaceWith: The color to replace targetColor with.
        :type replaceWith: tuple
        """
        # Loop through all pixels
        for i in range(1, self.WINDOW_WIDTH):
            for j in range(1, self.WINDOW_WIDTH):
                # Replace pixel of targetColor
                if self.win.get_at((i, j)) == targetColor:
                    pygame.draw.rect(self.win, replaceWith, (i, j, 1, 1))
        pygame.display.update()

    def run(self):
        """
        Handles the runtime for the app.
        :param self: The calling object
        :type self: PaintApp
        """
        # Set initial conditions for the app to run.
        prev_pos = pygame.mouse.get_pos()
        pygame.event.pump()
        cur_pos = self.get_click(prev_pos)
        self.current_tool = self.get_current_tool(cur_pos, "Draw")
        self.pb.set_thickness(self.det_brush_th(cur_pos, self.pb.thickness))
        self.pb.set_color(self.det_brush_color(cur_pos, self.pb.color))
        # Game loop.
        while self.user_wants_to_paint():
            # Determine the current state of the app - paintbrush color and thickness and the current tool.
            cur_pos = self.get_click(prev_pos)
            self.pb.set_thickness(self.det_brush_th(cur_pos, self.pb.thickness))
            self.pb.set_color(self.det_brush_color(cur_pos, self.pb.color))
            self.pb.is_painting = True
            self.panel.set_to_indicate_as_current_color(self.pb.color)
            self.panel.set_to_indicate_as_current_brush_thickness(self.pb.thickness)
            self.current_tool = self.get_current_tool(cur_pos, self.current_tool)
            # Do something based on the current tool.
            if self.current_tool == "Draw":
                self.panel.set_to_indicate_as_current_tool("Draw")
                self.display_panel()
                prev_pos = self.draw(prev_pos, cur_pos)  # Changes the stored position of the cursor.
            if self.current_tool == "Erase":
                self.panel.set_to_indicate_as_current_tool("Erase")
                self.display_panel()
                self.pb.is_painting = False  # The paintbrush isn't painting as the eraser is being used.
                prev_pos = self.draw(prev_pos, cur_pos)
            if self.current_tool == "Clear":
                self.panel.set_to_indicate_as_current_tool("Clear")
                self.display_panel()
                self.win.fill(self.background_color)  # Resets the painting window.
                self.display_panel()
                pygame.display.update()
            if self.current_tool == "Replace":
                self.panel.set_to_indicate_as_current_tool("Replace")
                self.display_panel()
                while self.user_wants_to_paint():
                    # User is clicking to replace a color
                    if pygame.mouse.get_pressed()[0]:
                        cur_pos = pygame.mouse.get_pos()
                        color_to_replace = self.win.get_at(cur_pos)[:3]  # Trim RGBA to RGB value.
                        self.replace(color_to_replace, self.pb.color)
                        break
            if self.current_tool == "Fill":
                self.panel.set_to_indicate_as_current_tool("Fill")
                self.display_panel()
                while self.user_wants_to_paint():
                    # User is clicking to fill a region
                    if pygame.mouse.get_pressed()[0]:
                        cur_pos = pygame.mouse.get_pos()
                        target_color = self.win.get_at(cur_pos)[:3]  # Trim RGBA to RGB value.
                        self.fill(cur_pos, target_color, self.pb.color)
                        break

        pygame.quit()
        sys.exit(0)


class PaintBrush:
    """Class representing a paintbrush.
    Supports painting in many colors with many thicknesses."""

    def __init__(self):
        """Initializes a paintbrush with default values for color and thickness.
        :param self: The calling object/object being initialized
        :type self: PaintBrush
        """
        self.color = (0, 0, 0)  # By default, the brush is black
        self.thickness = 10  # Number of pixels wide that each brushstroke is
        self.is_painting = True

    def set_color(self, col):
        """Manipulates the color of the paintbrush.
        :param self: The calling object
        :type self: PaintBrush
        :param col: The color for the paintbrush.
        :type col: tuple
        """
        self.color = col

    def set_thickness(self, thickness):
        """Manipulates the thickness of the paintbrush.
        :param self: The calling object
        :type self: PaintBrush
        :param thickness: The thickness (in pixels) of the paintbrush's stroke.
        :type thickness: int
        """
        self.thickness = thickness

    def draw(self, win, prev_pos, cur_pos, background_color):
        """Draws on the given window.
        :param self: The calling object
        :type self: PaintBrush
        :param win: The Pygame window to draw on.
        :type win: pygame.Surface
        :param prev_pos: The previous position of the cursor.
        :type prev_pos: tuple
        :param cur_pos: The current position of the cursor.
        :type cur_pos: tuple
        :param background_color: The color of the window.
        :type background_color: tuple
        :returns: The position of the cursor if the mouse is pressed, else None.
        :rtype: tuple
        """
        pygame.event.pump()
        if pygame.mouse.get_pressed()[0]:
            # Check if the cursor has moved
            if prev_pos is None:
                prev_pos = pygame.mouse.get_pos()
                cur_pos = prev_pos
            # If the cursor is on the screen, draw a line from its previous to its current position
            # To make a continuous stroke
            if 0 <= cur_pos[1] < win.get_width():
                if self.is_painting:
                    pygame.draw.line(win, self.color, (prev_pos[0], prev_pos[1]),
                                     (cur_pos[0], cur_pos[1]), self.thickness)
                else:
                    pygame.draw.line(win, background_color, (prev_pos[0], prev_pos[1]),
                                     (cur_pos[0], cur_pos[1]), self.thickness)
                pygame.display.update()
                return cur_pos
        else:
            return None


class Panel:
    """Class that represents the selection panel for color, brush thickness and painting tools."""
    
    COLOR_STRIP_WIDTH = 112  # The width of the strip of colors to select from
    COLOR_STRIP_HEIGHT = 16  # The height of the strip of colors to select from
    COLOR_STRIP_X = 64  # x-coordinate of the top-left corner of the color selection strip
    COLOR_STRIP_Y = 496  # y-coordinate of the top-left corner of the color selection strip

    def __init__(self):
        """Initializes the Panel with buttons to select color, brush thickness and painting tools.
        :param self: The calling object/object being initialized
        :type self: Panel
        """
        blue = (0, 255, 255)
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        # Create rectangles/buttons for all the possible tools
        self.fill = self.font.render(" F ", True, (0, 0, 0), blue)
        self.F = self.fill.get_rect()
        self.draw = self.font.render(" D ", True, (0, 0, 0), blue)
        self.D = self.draw.get_rect()
        self.er = self.font.render(" E ", True, (0, 0, 0), blue)
        self.E = self.er.get_rect()
        self.replace = self.font.render(" R ", True, (0, 0, 0), blue)
        self.R = self.replace.get_rect()
        self.clear = self.font.render(" C ", True, (0, 0, 0), blue)
        self.C = self.clear.get_rect()
        # Create rectangles/buttons for all the possible brush thicknesses
        self.brush1 = self.font.render(" 1 ", True, (0, 0, 0), blue)
        self.B1 = self.brush1.get_rect()
        self.brush2 = self.font.render(" 2 ", True, (0, 0, 0), blue)
        self.B2 = self.brush2.get_rect()
        self.brush3 = self.font.render(" 3 ", True, (0, 0, 0), blue)
        self.B3 = self.brush3.get_rect()
        self.brush4 = self.font.render(" 4 ", True, (0, 0, 0), blue)
        self.B4 = self.brush4.get_rect()
        # Create rectangles/buttons for each brush color to form a strip
        self.red = pygame.rect.RectType((64, 496, 16, 16))
        self.blue = pygame.rect.RectType((80, 496, 16, 16))
        self.yellow = pygame.rect.RectType((96, 496, 16, 16))
        self.mag = pygame.rect.RectType((112, 496, 16, 16))
        self.green = pygame.rect.RectType((128, 496, 16, 16))
        self.turq = pygame.rect.RectType((144, 496, 16, 16))
        self.black = pygame.rect.RectType((161, 497, 14, 14))  # The selected color (black by default) appears smaller

    def get_tool_buttons(self):
        """
        :param self: The calling object
        :type self: Panel
        :returns: The tool buttons with text and a rectangle on which the text is placed.
        :rtype: dict
        """
        return {"Fill": [self.fill, self.F], "Draw": [self.draw, self.D], "Erase": [self.er, self.E],
                "Replace": [self.replace, self.R], "Clear": [self.clear, self.C]}

    def get_brush_buttons(self):
        """
        :param self: The calling object
        :type self: Panel
        :returns: The brush buttons with text and a rectangle on which the text is placed.
        :rtype: dict
        """
        return {10: [self.brush1, self.B1], 20: [self.brush2, self.B2], 30: [self.brush3, self.B3],
                40: [self.brush4, self.B4]}

    def get_color_buttons(self):
        """
        :param self: The calling object
        :type self: Panel
        :returns: The color buttons with text and a rectangle on which the text is placed.
        :rtype: dict
        """
        return {"red": [(255, 0, 0), self.red], "blue": [(0, 0, 255), self.blue],
                "yellow": [(255, 255, 0), self.yellow],
                "green": [(0, 255, 0), self.green], "turq": [(0, 255, 255), self.turq],
                "magenta": [(255, 0, 255), self.mag], "black": [(0, 0, 0), self.black]}

    def set_to_indicate_as_current_tool(self, tool):
        """
        Indicates the current tool being used with a red button, and the other tools with a blue button.
        :param self: The calling object
        :type self: Panel
        :param tool: The current tool to be used
        :type tool: str
        """
        blue = (0, 255, 255)
        # Reset each button to its unselected state
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.fill = self.font.render(" F ", True, (0, 0, 0), blue)
        self.F = self.fill.get_rect()
        self.draw = self.font.render(" D ", True, (0, 0, 0), blue)
        self.D = self.draw.get_rect()
        self.er = self.font.render(" E ", True, (0, 0, 0), blue)
        self.E = self.er.get_rect()
        self.replace = self.font.render(" R ", True, (0, 0, 0), blue)
        self.R = self.replace.get_rect()
        self.clear = self.font.render(" C ", True, (0, 0, 0), blue)
        self.C = self.clear.get_rect()

        red = (255, 0, 0)
        # Make the selected button red to indicate the current tool
        if tool == "Fill":
            self.fill = self.font.render(" F ", True, (0, 0, 0), red)
            self.F = self.fill.get_rect()
        elif tool == "Draw":
            self.draw = self.font.render(" D ", True, (0, 0, 0), red)
            self.D = self.draw.get_rect()
        elif tool == "Erase":
            self.er = self.font.render(" E ", True, (0, 0, 0), red)
            self.E = self.er.get_rect()
        elif tool == "Replace":
            self.replace = self.font.render(" R ", True, (0, 0, 0), red)
            self.R = self.replace.get_rect()
        else:
            self.clear = self.font.render(" C ", True, (0, 0, 0), red)
            self.C = self.clear.get_rect()

    def set_to_indicate_as_current_brush_thickness(self, thickness):
        """
        Indicates the current brush thickness being used with a red button, and the other tools with a blue button.
        :param self: The calling object
        :type self: Panel
        :param thickness: The current brush thickness to be used
        :type thickness: int
        """
        blue = (0, 255, 255)
        # Reset each button to its unselected state
        self.brush1 = self.font.render(" 1 ", True, (0, 0, 0), blue)
        self.B1 = self.brush1.get_rect()
        self.brush2 = self.font.render(" 2 ", True, (0, 0, 0), blue)
        self.B2 = self.brush2.get_rect()
        self.brush3 = self.font.render(" 3 ", True, (0, 0, 0), blue)
        self.B3 = self.brush3.get_rect()
        self.brush4 = self.font.render(" 4 ", True, (0, 0, 0), blue)
        self.B4 = self.brush4.get_rect()

        red = (255, 0, 0)
        # Make the selected button red to indicate the current brush thickness
        if thickness == 10:
            self.brush1 = self.font.render(" 1 ", True, (0, 0, 0), red)
            self.B1 = self.brush1.get_rect()
        elif thickness == 20:
            self.brush2 = self.font.render(" 2 ", True, (0, 0, 0), red)
            self.B2 = self.brush2.get_rect()
        elif thickness == 30:
            self.brush3 = self.font.render(" 3 ", True, (0, 0, 0), red)
            self.B3 = self.brush3.get_rect()
        else:
            self.brush4 = self.font.render(" 4 ", True, (0, 0, 0), red)
            self.B4 = self.brush4.get_rect()

    def set_to_indicate_as_current_color(self, color):
        """
        Indicates the current color being used with a smaller button than those for the other colors.
        :param self: The calling object
        :type self: Panel
        :param color: The current color to be used
        :type color: tuple
        """
        # Reset all colors to default size
        self.red = pygame.rect.RectType((64, 496, 16, 16))
        self.blue = pygame.rect.RectType((80, 496, 16, 16))
        self.yellow = pygame.rect.RectType((96, 496, 16, 16))
        self.mag = pygame.rect.RectType((112, 496, 16, 16))
        self.green = pygame.rect.RectType((128, 496, 16, 16))
        self.turq = pygame.rect.RectType((144, 496, 16, 16))
        self.black = pygame.rect.RectType((160, 496, 16, 16))
        # Show current color with a smaller rectangle
        if color == (255, 0, 0):
            self.red = pygame.rect.RectType((65, 497, 14, 14))
        elif color == (0, 0, 255):
            self.blue = pygame.rect.RectType((81, 497, 14, 14))
        elif color == (255, 255, 0):
            self.yellow = pygame.rect.RectType((97, 497, 14, 14))
        elif color == (255, 0, 255):
            self.mag = pygame.rect.RectType((113, 497, 14, 14))
        elif color == (0, 255, 0):
            self.green = pygame.rect.RectType((129, 497, 14, 14))
        elif color == (0, 255, 255):
            self.turq = pygame.rect.RectType((145, 497, 14, 14))
        else:
            self.black = pygame.rect.RectType((161, 497, 14, 14))

    def display(self, win):
        """
        Displays the Panel on the window win with the buttons.
        :param self: The calling object
        :type self: Panel
        :param win: The window to display the Panel on
        :type win: pygame.Surface
        """
        tool_dict = self.get_tool_buttons()
        brush_dict = self.get_brush_buttons()
        color_dict = self.get_color_buttons()

        # Display the buttons for each tool
        x_coord = 320
        for x in tool_dict:
            tool_dict[x][1].center = (x_coord, 544)  # Place center of the rectangle displaying a possible tool
            win.blit(tool_dict[x][0], tool_dict[x][1])
            x_coord += 24  # Spacing between rectangles displaying the tools

        # Display buttons for brush thicknesses
        x_coord = 332
        for x in brush_dict:
            brush_dict[x][1].center = (x_coord, 512)  # Place center of the rectangle displaying a brush thickness
            win.blit(brush_dict[x][0], brush_dict[x][1])
            x_coord += 24  # Spacing between two rectangles

        # Create an empty strip to display the color buttons
        pygame.draw.rect(win, (255, 255, 255),
                         pygame.rect.RectType(self.COLOR_STRIP_X, self.COLOR_STRIP_Y, self.COLOR_STRIP_WIDTH,
                                              self.COLOR_STRIP_HEIGHT))  # Empty rectangle before displaying the colors
        # Display brush colors
        for x in color_dict:
            pygame.draw.rect(win, color_dict[x][0], color_dict[x][1])

        pygame.display.update()


if __name__ == '__main__':
    # Run the app.
    app = PaintApp()
    app.run()
