package com.example.stylematee.utils;

import android.content.Context;
import android.graphics.Bitmap;
import android.net.Uri;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;

public class FileUtils {

    /**
     * Get the file path for a given URI
     */
    public static String getPath(Context context, Uri uri) throws Exception {
        InputStream inputStream = context.getContentResolver().openInputStream(uri);
        File tempFile = File.createTempFile("upload", ".jpg", context.getCacheDir());
        FileOutputStream outputStream = new FileOutputStream(tempFile);

        byte[] buffer = new byte[1024];
        int length;
        while ((length = inputStream.read(buffer)) > 0) {
            outputStream.write(buffer, 0, length);
        }
        outputStream.close();
        inputStream.close();
        return tempFile.getAbsolutePath();
    }

    /**
     * Save a Bitmap image to a temporary file and return its Uri
     */
    public static Uri saveBitmapToFile(Context context, Bitmap bitmap) {
        try {
            // Create a temporary file in the cache directory
            File tempFile = File.createTempFile("camera_image", ".jpg", context.getCacheDir());

            // Write the bitmap to the file
            FileOutputStream outputStream = new FileOutputStream(tempFile);
            bitmap.compress(Bitmap.CompressFormat.JPEG, 90, outputStream);
            outputStream.close();

            // Return the file's Uri
            return Uri.fromFile(tempFile);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
