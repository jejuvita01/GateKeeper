import random
import time
from azure.iot.device import IoTHubDeviceClient, Message


CONNECTION_STRING = "HostName=KSW.azure-devices.net;DeviceId=RaspberryKSW;SharedAccessKey=9inK442ZoKt2GkdU2Q339P2ePV4hFMELoAIoTPGwskM="
MSG_SND ='{{"clock" : "{clock}", "camera" : "{camera}"}}'

while True:
    clock = 7501
    camera = 8788
    def iothub_client_init():
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        return client
    
    def iothub_client_run():
        try:
            client = iothub_client_init()
            print("Sending data to IoT Hub, press Ctrl-C to exit")
            while True:
                msg_txt_formatted = MSG_SND.format(clock = clock,camera = camera)
                message = Message(msg_txt_formatted)
                print("Sending message : {}".format(message))
                tmp = client.send_message(message)
                print("\n{}\n".format(tmp))
                
                print("Message successfully sent")
                time.sleep(3)
                
        except KeyboardInterrupt:
            print("IoTHubClient stopped")
            
            
    if __name__ == '__main__':
        print("Press Ctrl-C to exit")
        iothub_client_run()
    