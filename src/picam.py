import picamera
import io

from datetime import datetime

class PiCam:
    camera = None
    resPreview = (640, 480)

    def __init__(self):
        self.camera = picamera.PiCamera()

    def setCamResolution(self, res):
        self.camera.resolution = res

    def setPreviewResolution(self, res):
        self.resPreview = res
        self.setCamResolution(self.resPreview)

    def getPreviewResolution(self):
        return self.resPreview

    def getMaxResolution(self):
        return (self.camera.MAX_RESOLUTION.width, self.camera.MAX_RESOLUTION.height)

    def capture(self, res, directory, extension):
        now = datetime.now()
        strNow = now.strftime("%d-%m-%Y %H-%M-%S")
        self.setCamResolution(res)
        self.camera.capture("./{0}/{1}.{2}".format(directory, strNow, extension))
        self.setCamResolution(self.resPreview)

    def getPreviewFrame(self):
        rgb = bytearray(self.getPreviewResolution()[0] * self.getPreviewResolution()[1] * 3)
        stream = io.BytesIO()
        self.camera.capture(stream, use_video_port=True, format="rgb")
        stream.seek(0)
        stream.readinto(rgb)
        stream.close()

        return rgb

    def cleanup(self):
        self.camera.close()
