const { Storage } = require('@google-cloud/storage');
const fs = require('fs');
const path = require('path');

// Create a storage client
const storage = new Storage();

async function downloadPublicFile(bucketName, srcFileName, destFileName) {
    const options = {
        destination: destFileName,
    };

    // Download public file.
    await storage.bucket(bucketName).file(srcFileName).download(options);

    console.log(
        `Downloaded public file ${srcFileName} from bucket name ${bucketName} to ${destFileName}`
    );
}

/**
 * Downloads all files from a public Google Cloud Storage bucket.
 * @param {string} bucketName - The name of the bucket.
 * @param {string} folder - The folder (prefix) in the bucket.
 * @param {string} destination - The local directory to save the files.
 */
async function downloadAllFilesFromBucket(bucketName, folder, destination) {
    try {
        // Ensure the destination directory exists
        if (!fs.existsSync(destination)) {
            fs.mkdirSync(destination, { recursive: true });
        }

        // Get the list of files in the bucket
        const [files] = await storage.bucket(bucketName).getFiles({ prefix: folder });

        // Download each file
        for (const file of files) {
            const destFileName = path.join(destination, file.name.replace(folder, ''));
            console.log(`Downloading ${file.name} to ${destFileName}...`);
            await file.download({ destination: destFileName });
            console.log(`Downloaded ${file.name}`);
        }

        console.log('All files downloaded successfully.');
    } catch (error) {
        console.error('Error downloading files:', error);
    }
}

downloadAllFilesFromBucket('quickdraw_dataset', 'full/numpy_bitmap', 'data/numpy_bitmap');
//downloadPublicFile('quickdraw_dataset', 'full/binary/angel.bin', './data/testangel.bin');
