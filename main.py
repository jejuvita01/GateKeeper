from camera.cam import runCam
from utils import runJavaScript
import threading
import time


fileUploadNotTread = threading.Thread(target=runJavaScript.runFileUpload)
fileUploadNotTread.daemon = True

if __name__=='__main__':
    fileUploadNotTread.start()
    time.sleep(3)
    runCam()
