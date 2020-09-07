package com.abhivineet.tracking;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;
//import org.json.simple.JSONObject;

import java.io.BufferedInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.concurrent.ExecutionException;

public class Result extends AppCompatActivity {

    String ret;
    Button back;
    TextView name;
    TextView birthday;
    TextView post;
    ImageView profile;
    Bitmap bm;
    String TAG="RESULT_ACTIVITY";


    public class DownloadImagesTask extends AsyncTask<String, Void, Bitmap> {

        @Override
        protected Bitmap doInBackground(String... urls) {
            return download_Image(urls[0]);
        }

        @Override
        protected void onPostExecute(Bitmap result) {
            profile.setImageBitmap(result);              // how do I pass a reference to mChart here ?
        }

        private Bitmap download_Image(String url) {
            //---------------------------------------------------
            Bitmap bm = null;
            try {
                URL aURL = new URL(url);
                URLConnection conn = aURL.openConnection();
                conn.connect();
                InputStream is = conn.getInputStream();
                BufferedInputStream bis = new BufferedInputStream(is);
                bm = BitmapFactory.decodeStream(bis);
                bis.close();
                is.close();
            } catch (Exception e) {
                Log.e("Hub","Error getting the image from server : " + e.getMessage().toString());
            }
            return bm;
        }
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);

        Intent result = getIntent();
        ret = result.getStringExtra("return");

        back = (Button) findViewById(R.id.back);
        name = (TextView) findViewById(R.id.name);
        birthday = (TextView) findViewById(R.id.birthday);
        profile = (ImageView) findViewById(R.id.profile);
        post = (TextView) findViewById(R.id.post);
        try {
            JSONObject jsonObject = new JSONObject(ret);
            name.setText(jsonObject.getString("name"));
            birthday.setText(jsonObject.getString("birthday"));
            post.setText(jsonObject.getString("post"));
            DownloadImagesTask task = new DownloadImagesTask();
            bm = task.execute("https://graph.facebook.com/" + jsonObject.getString("userId") + "/picture?type=large").get();
        } catch (Exception e) {
            e.printStackTrace();
        }

        back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent camera = new Intent(getApplicationContext(), Camera.class);
                startActivity(camera);
                finish();
            }
        });

    }
}
