import os

def runFileUploadNotification():
    os.chdir("./fileuploadnotification/")
    os.system("node ./FileUploadNotification.js")

def runFileUpload():
    os.chdir("./fileupload/")
    os.system("node ./FileUpload.js")