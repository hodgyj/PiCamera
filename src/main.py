import picamui
import picam

def main():
    captureResolution = (1280, 1024)
    captureDirectory = "./images"
    captureExtension = "jpg"

    # Setup UI
    ui = picamui.PiCamUi()
    ui.createUi()

    # Setup camera
    cam = picam.PiCam()
    cam.setPreviewResolution(ui.getScreenResolution())
    captureResolution = cam.getMaxResolution()

    loop = True
    while loop:
        rgb = cam.getPreviewFrame()
        ui.updatePreview(rgb, cam.getPreviewResolution())
        ui.update()

        uiEvents = ui.getEvents()
        for event in uiEvents:
            if event == "keyDownEscape" or event == "pygameQuit" or event == "btnExitPressed":
                loop = False
            elif event == "btnTakePressed":
                cam.capture(captureResolution, captureDirectory, captureExtension)
            else:
                print("Unknown event {}".format(event))
    ui.cleanup()


if __name__ == "__main__":
    main()
