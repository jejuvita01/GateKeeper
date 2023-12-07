'use strict';

const Client = require('azure-iothub').Client;

const connectionString = "HostName=KSW.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=YPGM8PhuUDtWAMrKuzy95zNMRTtiiNiuiAIoTNcQ3bs=";

const serviceClient = Client.fromConnectionString(connectionString);

serviceClient.open(function (err) {
    if (err) {
        console.error('Could not connect: ' + err.message);
    } else {
        console.log('Service client connected');
        serviceClient.getFileNotificationReceiver(function receiveFileUploadNotification(err, receiver) {
            if (err) {
                console.error('error getting the file notification receiver: ' + err.toString());
            } else {
                receiver.on('message', function (msg) {
                    console.log('File upload from device:')
                    console.log(msg.getData().toString('utf-8'));
                    receiver.complete(msg, function (err) {
                        if (err) {
                            console.error('Could not finish the upload: ' + err.message);
                        } else {
                            console.log('Upload complete');
                        }
                    });
                });
            }
        });
    }
});