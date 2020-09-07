package com.abhivineet.tracking;

import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Environment;
import android.preference.PreferenceManager;
import android.provider.MediaStore;
import android.support.annotation.Nullable;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedOutputStream;
import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Locale;

public class Setup extends AppCompatActivity {

    Button click;
    Button finish;
    String imageFilePath;
    int left = 3;
    private Bitmap mImageBitmap;
    private Uri photoURI;
    ArrayList<String> encodedBitmapStore;
    private static final int REQUEST_CAPTURE_IMAGE = 100;
    String userId;
    String TAG = "SETUP ACTIVITY";

    void parcelPlease(){
        SendImage task = new SendImage();
        JSONObject parcelObject = new JSONObject();
//        Log.e(TAG, "" + encodedBitmapStore.size());
        JSONArray array = new JSONArray(encodedBitmapStore);
        try {
            parcelObject.put("userId", userId);
            parcelObject.put("pictures", array);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        String parcelString = parcelObject.toString();
        task.execute(parcelString);
    }

    private class SendImage extends AsyncTask<String, Void, Void>{

        @Override
        protected Void doInBackground(String... strings) {
            String server = "http://10.59.99.137:5000/face_embed";
            String data = strings[0]; //data to post
            String ret = "";
            OutputStream out = null;
            URL url;
            HttpURLConnection urlConnection = null;
            try {
                url = new URL(server);
                urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setRequestMethod("POST");
                urlConnection.setRequestProperty("Content-Type", "application/string");
                out = new BufferedOutputStream(urlConnection.getOutputStream());

                BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(out, "UTF-8"));
                writer.write(data);
                writer.flush();
                writer.close();
                out.close();

                urlConnection.connect();
                InputStream in = urlConnection.getInputStream();
                InputStreamReader inputStreamReader = new InputStreamReader(in);

                int inputStreamData = inputStreamReader.read();
                while (inputStreamData != -1) {
                    char current = (char) inputStreamData;
                    inputStreamData = inputStreamReader.read();
                    ret += current;
                }
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                if (urlConnection != null) {
                    urlConnection.disconnect();
                }
            }
            Log.i(TAG, data);

            return null;
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup);

        Intent intent = getIntent();
        userId = intent.getStringExtra("id");

        final SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(this);

        click = (Button) findViewById(R.id.click);
        finish = (Button) findViewById(R.id.submit);
        encodedBitmapStore = new ArrayList<String>();
        System.out.println(encodedBitmapStore.size());
        click.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCameraIntent();
            }
        });

        finish.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // mark that the first time has run
                SharedPreferences.Editor editor = prefs.edit();
                editor.putBoolean("firstTime", true);
                editor.commit();
                parcelPlease();
                finish();
            }
        });

    }


    //STARTS THE CAMERA INTENT A PRESET 5 TIMES TO SEND TO THE SERVER FOR TRAINING
    private void openCameraIntent() {
        Intent pictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if(pictureIntent.resolveActivity(getPackageManager()) != null){
            //Create a file to store the image
            File photoFile = null;
            try {
                photoFile = createImageFile();
            } catch (IOException ex) {
                // Error occurred while creating the File
                Log.e("Error", "While creating the file!");
            }
            if (photoFile != null) {
                photoURI = FileProvider.getUriForFile(getApplicationContext(),"com.abhivineet.tracking.provider", photoFile);
                pictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                pictureIntent.putExtra("android.intent.extras.CAMERA_FACING", 1);
                startActivityForResult(pictureIntent, REQUEST_CAPTURE_IMAGE);
            }
        }
    }


    // CREATES IMAGE FILE IN DIRECTORY WITH EXTENSION (NOTE: THIS FILE IS AN EMPTY FILE WHICH MUST BE POPULATED WITH THE DATA)
    private File createImageFile() throws IOException {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(new Date());
        String imageFileName = "IMG_" + timeStamp + "_";
        File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(imageFileName,  ".jpg", storageDir);
        return image;
    }

    //HANDLING THE RESULT OBTAINED FROM THE CAMERA INTENT
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode==REQUEST_CAPTURE_IMAGE){
            try {
                mImageBitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), photoURI);
            } catch (IOException e) {
                Log.e("IO Exception", "File not found for getBitmap");
            }
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            mImageBitmap.compress(Bitmap.CompressFormat.JPEG, 100, baos);
            byte[] imageBytes = baos.toByteArray();
            String encodedImage = Base64.encodeToString(imageBytes, Base64.DEFAULT);
            encodedBitmapStore.add(encodedImage);
            left--;
            if (left>0){
                Toast.makeText(getApplicationContext(), left + "pictures more!", Toast.LENGTH_SHORT).show();
            }
            if (left==0){
                finish.setVisibility(View.VISIBLE);
            }
            try {
                baos.flush();
                baos.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
