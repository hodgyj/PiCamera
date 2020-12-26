import picamera
import pygame
import pygame_gui
import time
import io
import os

from datetime import datetime

def setup_pygame():
    pygame.init()
    # Set the cursor to invisible. We use a transparent cursor for this as set_visible breaks the touch screen
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # (0, 0) means same as display resolution
    return screen

def setup_camera(screen):
    camera = picamera.PiCamera()
    camera.rotation = 90
    return camera

def take_picture(camera, capture_resolution, directory):
    now = datetime.now()
    now_string = now.strftime("%d-%m-%Y %H-%M-%S")
    print("Saving image to: \"./images/{0}.jpg\"".format(now_string))
    camera.resolution = capture_resolution
    camera.capture("./{0}/{1}.jpg".format(directory, now_string))

def set_cam_resolution(camera, resolution, framerate):
    camera.resolution = resolution
    camera.framerate = framerate

screen = setup_pygame()
camera = setup_camera(screen)

cam_viewfinder_resolution = (int(screen.get_width()), int(screen.get_height()))
cam_capture_resolution = (camera.MAX_RESOLUTION.width, camera.MAX_RESOLUTION.height)
cam_video_resolution = (1920, 1080)

cam_viewfinder_framerate = 15
cam_video_framerate = 30

set_cam_resolution(camera, cam_viewfinder_resolution, cam_viewfinder_framerate)

rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)

#pygame-gui
gui_manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()))
clock = pygame.time.Clock()

take_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((720, 200), (80, 80)),
                                             text='Take',
                                             manager=gui_manager)

loop = True
while loop:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loop = False
        elif event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == take_button:
                    take_picture(camera, cam_capture_resolution, './images')
                    # reset_resolution(camera, cam_viewfinder_resolution, cam_viewfinder_framerate)
                    set_cam_resolution(camera, cam_viewfinder_resolution, cam_viewfinder_framerate)
        gui_manager.process_events(event)

    gui_manager.update(time_delta)

    stream = io.BytesIO()
    camera.capture(stream, use_video_port=True, format='rgb')
    stream.seek(0)
    stream.readinto(rgb)
    stream.close()
    img = pygame.image.frombuffer(rgb[0:(camera.resolution[0] * camera.resolution[1] * 3)], camera.resolution, 'RGB')
    img = pygame.transform.scale(img, (screen.get_width(), screen.get_height()))

    if img:
        screen.blit(img, (0, 0))

    gui_manager.draw_ui(screen)
    pygame.display.update()

camera.close()
pygame.display.quit()
