package com.example.stylematee;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

import androidx.appcompat.app.AppCompatActivity;

public class SplashActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        // Simulate loading with a delay
        new Handler().postDelayed(() -> {
            // Redirect to LoginPhoneNumberActivity instead of MainActivity
            Intent intent = new Intent(SplashActivity.this, LoginPhoneNumberActivity.class);
            startActivity(intent);
            finish(); // Close splash screen
        }, 3000); // 3 seconds
    }
}
