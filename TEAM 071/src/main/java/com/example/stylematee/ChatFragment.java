package com.example.stylematee;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;


import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.bumptech.glide.Glide;
import com.example.stylematee.utils.FileUtils;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Retrofit;
import retrofit2.Response;
import retrofit2.converter.gson.GsonConverterFactory;

public class ChatFragment extends Fragment {

    private static final int IMAGE_PICK_REQUEST = 100;
    private static final int CAMERA_REQUEST = 101;

    LinearLayout imageContainer;
    TextView resultTextView;
    ProgressBar progressBar;

    List<Uri> selectedImageUris = new ArrayList<>();
    private static final int IMAGE_LIMIT = 10;

    // Firebase Function Base URL
    private static final String BASE_URL = "https://us-central1-stylematee-backend.cloudfunctions.net/";

    public ChatFragment() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_chat, container, false);

        // Initialize UI components
        imageContainer = view.findViewById(R.id.imageContainer);
        resultTextView = view.findViewById(R.id.resultTextView);
        progressBar = view.findViewById(R.id.progressBar);

        imageContainer.setOnClickListener(v -> showImagePickerOptions());
        return view;
    }

    private void showImagePickerOptions() {
        Intent galleryIntent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        galleryIntent.setType("image/*");
        galleryIntent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);

        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

        Intent chooser = Intent.createChooser(galleryIntent, "Select Images");
        chooser.putExtra(Intent.EXTRA_INITIAL_INTENTS, new Intent[]{cameraIntent});
        startActivityForResult(chooser, IMAGE_PICK_REQUEST);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (resultCode == Activity.RESULT_OK) {
            if (requestCode == IMAGE_PICK_REQUEST && data != null) {
                if (data.getClipData() != null) {
                    // Handle multiple images
                    int count = data.getClipData().getItemCount();
                    for (int i = 0; i < count && selectedImageUris.size() < IMAGE_LIMIT; i++) {
                        Uri imageUri = data.getClipData().getItemAt(i).getUri();
                        addImageUri(imageUri);
                    }
                } else if (data.getData() != null) {
                    // Single image from gallery
                    addImageUri(data.getData());
                }
            } else if (requestCode == CAMERA_REQUEST && data.getExtras() != null) {
                Bitmap bitmap = (Bitmap) data.getExtras().get("data");
                Uri cameraImageUri = FileUtils.saveBitmapToFile(getContext(), bitmap);
                if (cameraImageUri != null) {
                    addImageUri(cameraImageUri);
                }
            }
        }

        if (selectedImageUris.size() >= 2) {
            uploadImagesToFirebase();
        } else {
            resultTextView.setText("Please select at least 2 images.");
        }
    }

    private void addImageUri(Uri imageUri) {
        if (selectedImageUris.size() < IMAGE_LIMIT) {
            selectedImageUris.add(imageUri);
            addImageView(imageUri);
        } else {
            Toast.makeText(getContext(), "You can upload up to 10 images only.", Toast.LENGTH_SHORT).show();
        }
    }

    private void addImageView(Uri imageUri) {
        ImageView imageView = new ImageView(getContext());
        Glide.with(this).load(imageUri).into(imageView);
        imageView.setLayoutParams(new ViewGroup.LayoutParams(200, 200));
        imageContainer.addView(imageView);
    }

    private void uploadImagesToFirebase() {
        progressBar.setVisibility(View.VISIBLE);

        new Thread(() -> {
            try {
                List<String> imagePaths = new ArrayList<>();
                for (Uri uri : selectedImageUris) {
                    File file = new File(FileUtils.getPath(getContext(), uri));
                    imagePaths.add(file.getAbsolutePath());
                }
                fetchClothingSuggestions(imagePaths);

            } catch (Exception e) {
                e.printStackTrace();
                getActivity().runOnUiThread(() -> {
                    Toast.makeText(getContext(), "Failed to upload images.", Toast.LENGTH_SHORT).show();
                    progressBar.setVisibility(View.GONE);
                });
            }
        }).start();
    }

    private void fetchClothingSuggestions(List<String> imagePaths) {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        FirebaseFunctionService service = retrofit.create(FirebaseFunctionService.class);

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("imageUrls", imagePaths);

        Call<Map<String, String>> call = service.getClothingSuggestions(requestBody);
        call.enqueue(new Callback<Map<String, String>>() {
            @Override
            public void onResponse(Call<Map<String, String>> call, Response<Map<String, String>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    resultTextView.setText(response.body().get("suggestions"));
                } else {
                    resultTextView.setText("Failed to fetch suggestions.");
                }
                progressBar.setVisibility(View.GONE);
            }

            @Override
            public void onFailure(Call<Map<String, String>> call, Throwable t) {
                resultTextView.setText("Error: " + t.getMessage());
                progressBar.setVisibility(View.GONE);
            }
        });
    }

    interface FirebaseFunctionService {
        @POST("generateClothingSuggestions")
        Call<Map<String, String>> getClothingSuggestions(@Body Map<String, Object> body);
    }
}
