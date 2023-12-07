'use strict';

const Client = require('azure-iot-device').Client;
const Protocol = require('azure-iot-device-mqtt').Mqtt;
const errors = require('azure-iot-common').errors;
const path = require('path');

const {
    AnonymousCredential,
    BlockBlobClient,
    newPipeline
} = require('@azure/storage-blob');

// make sure you set these environment variables prior to running the sample.
const deviceConnectionString = "HostName=KSW.azure-devices.net;DeviceId=RaspberryKSW;SharedAccessKey=9inK442ZoKt2GkdU2Q339P2ePV4hFMELoAIoTPGwskM==";
const localFilePath = "/home/itsp/iot_project/fileupload/myimage.png";
const storageBlobName = path.basename(localFilePath);

async function uploadToBlob(localFilePath, client) {
    const blobInfo = await client.getBlobSharedAccessSignature(storageBlobName);
    if (!blobInfo) {
        throw new errors.ArgumentError('Invalid upload parameters');
    }

    const pipeline = newPipeline(new AnonymousCredential(), {
        retryOptions: { maxTries: 4 },
        telemetry: { value: 'HighLevelSample V1.0.0' }, // Customized telemetry string
        keepAliveOptions: { enable: false }
    });

    // Construct the blob URL to construct the blob client for file uploads
    const { hostName, containerName, blobName, sasToken } = blobInfo;
    const blobUrl = `https://${hostName}/${containerName}/${blobName}${sasToken}`;

    // Create the BlockBlobClient for file upload to the Blob Storage Blob
    const blobClient = new BlockBlobClient(blobUrl, pipeline);

    // Setup blank status notification arguments to be filled in on success/failure
    let isSuccess;
    let statusCode;
    let statusDescription;

    try {
        const uploadStatus = await blobClient.uploadFile(localFilePath);
        console.log('uploadStreamToBlockBlob success');

        // Save successful status notification arguments
        isSuccess = true;
        statusCode = uploadStatus._response.status;
        statusDescription = uploadStatus._response.bodyAsText;

        // Notify IoT Hub of upload to blob status (success)
        console.log('notifyBlobUploadStatus success');
    }
    catch (err) {
        isSuccess = false;
        statusCode = err.code;
        statusDescription = err.message;

        console.log('notifyBlobUploadStatus failed');
        console.log(err);
    }

    await client.notifyBlobUploadStatus(blobInfo.correlationId, isSuccess, statusCode, statusDescription);
}

// Read file
const FilePath = "/home/itsp/iot_project/img";
var fs = require('fs');

let timer;

timer = setInterval(() => {
    try {
        // upload image file to azure
        fs.readdir(FilePath, function (error, filelist) {
            for (var i = 1; i < filelist.length; i++) {
                console.log(FilePath + "/" + filelist[i]);
            }
        })



        //remove all image file
        fs.readdir(FilePath, function (error, filelist) {
            for (var i = 1; i < filelist.length; i++) {
                fs.unlinkSync(FilePath + "/" + filelist[i]);
                console.log(filelist[i]);
            }
        })

    } catch (error) {
        if (err.code == 'ENOENT') {
            console.log("delete image file fail");
        }
    }
}, 2000);








// Create a client device from the connection string and upload the local file to blob storage.


// console.log(deviceConnectionString);
// const deviceClient = Client.fromConnectionString(deviceConnectionString, Protocol);
// console.log("success connect with azure");
// uploadToBlob(localFilePath, deviceClient)
//     .catch((err) => {
//         console.log(err);
//     })
//     .finally(() => {
//         process.exit();
//     });