import pygame
import pygame_gui

class PiCamUi:
    screen = None
    guiManager = None
    clock = None
    uiElements = []

    def __init__(self):
        pygame.init()
        # Set the cursor to invisible. We use a transparent cursor for this as set_visible breaks the touch screen
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # (0, 0) means same as display resolution

    def createUi(self):
        self.guiManager = pygame_gui.UIManager((self.screen.get_width(), self.screen.get_height()))
        self.clock = pygame.time.Clock()

        self.createUiElements()

    def createUiElements(self):
        btnTake = {
            "name": "btnTake",
            "element": pygame_gui.elements.UIButton(
                relative_rect = pygame.Rect((720, 200), (80, 80)),
                text = "Take",
                manager = self.guiManager
            )
        }
        self.uiElements.append(btnTake)

        btnExit = {
            "name": "btnExit",
            "element": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((760, 440), (40, 40)),
                text='X',
                manager=self.guiManager
            )
        }
        self.uiElements.append(btnExit)

    def updatePreview(self, rgb, res):
        img = pygame.image.frombuffer(rgb[0:(res[0] * res[1] * 3)], res, 'RGB')
        img = pygame.transform.scale(img, (self.screen.get_width(), self.screen.get_height()))

        if img:
            self.screen.blit(img, (0, 0))

    def update(self):
        self.guiManager.draw_ui(self.screen)
        pygame.display.update()

    def cleanup(self):
        pygame.display.quit()

    def getEvents(self):
        events = []
        time_delta = self.clock.tick(30)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events.append("keyDownEscape")
            elif event.type == pygame.QUIT:
                events.append("pygameQuit")
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    for element in self.uiElements:
                        if event.ui_element == element.get("element"):
                            events.append("{}Pressed".format(element.get("name")))
            self.guiManager.process_events(event)
        self.guiManager.update(time_delta)

        return events

    def getScreenResolution(self):
        return (self.screen.get_width(), self.screen.get_height())
