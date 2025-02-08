package com.example.stylematee;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.MenuItem;
import android.widget.ImageButton;

import com.example.stylematee.utils.FirebaseUtil;
import com.google.android.gms.tasks.Task;
import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.firebase.messaging.FirebaseMessaging;

import java.util.HashMap;

public class MainActivity extends AppCompatActivity {

    BottomNavigationView bottomNavigationView;
    ImageButton searchButton;

    ChatFragment chatFragment;
    ProfileFragment profileFragment;

    // HashMap to store menu item IDs and their corresponding fragments
    HashMap<Integer, androidx.fragment.app.Fragment> fragmentMap;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize Fragments
        chatFragment = new ChatFragment();
        profileFragment = new ProfileFragment();

        // Initialize Views
        bottomNavigationView = findViewById(R.id.bottom_navigation);
        searchButton = findViewById(R.id.main_search_btn);

        // Handle Search Button Click
        searchButton.setOnClickListener(v -> {
            startActivity(new Intent(MainActivity.this, SearchUserActivity.class));
        });

        // Initialize Fragment Map
        fragmentMap = new HashMap<>();
        fragmentMap.put(R.id.menu_chat, chatFragment);
        fragmentMap.put(R.id.menu_profile, profileFragment);

        // Set Bottom Navigation Item Click Listener
        bottomNavigationView.setOnItemSelectedListener(item -> {
            androidx.fragment.app.Fragment selectedFragment = fragmentMap.get(item.getItemId());
            if (selectedFragment != null) {
                getSupportFragmentManager()
                        .beginTransaction()
                        .replace(R.id.main_frame_layout, selectedFragment)
                        .commit();
                return true;
            }
            return false;
        });

        // Set Default Selected Item
        bottomNavigationView.setSelectedItemId(R.id.menu_chat);

        // Fetch FCM Token
        getFCMToken();
    }

    // Method to Retrieve FCM Token
    private void getFCMToken() {
        FirebaseMessaging.getInstance().getToken().addOnCompleteListener(task -> {
            if (task.isSuccessful()) {
                String token = task.getResult();
                // Update FCM token in Firebase Firestore
                FirebaseUtil.currentUserDetails().update("fcmToken", token);
            } else {
                // Log error or handle failure
                System.out.println("Failed to fetch FCM Token: " + task.getException());
            }
        });
    }
}
