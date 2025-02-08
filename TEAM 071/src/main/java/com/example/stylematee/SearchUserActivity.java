package com.example.stylematee;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.widget.EditText;
import android.widget.ImageButton;

import com.example.stylematee.adapter.BannerAdapter;
import com.example.stylematee.model.BannerModel;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class SearchUserActivity extends AppCompatActivity {

    EditText searchInput;
    ImageButton backButton;
    RecyclerView bannerRecyclerView;

    BannerAdapter bannerAdapter;
    List<BannerModel> bannerList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search_user);

        // Initialize UI components
        searchInput = findViewById(R.id.search_input);
        backButton = findViewById(R.id.back_button);
        bannerRecyclerView = findViewById(R.id.banner_recycler_view);

        // Back button listener
        backButton.setOnClickListener(v -> onBackPressed());

        // Initialize Banner RecyclerView
        setupBannerRecyclerView();

        // Add Text Change Listener for Search Input
        searchInput.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                filterBanners(s.toString());
            }

            @Override
            public void afterTextChanged(Editable s) {
            }
        });
    }

    void setupBannerRecyclerView() {
        List<BannerModel> bannerList = new ArrayList<>();
        bannerList.add(new BannerModel("Amazon", R.drawable.amazon_banner, "https://www.amazon.in"));
        bannerList.add(new BannerModel("Flipkart", R.drawable.flipkart_banner, "https://www.flipkart.com"));
        bannerList.add(new BannerModel("Myntra", R.drawable.myntra_banner, "https://www.myntra.com"));
        bannerList.add(new BannerModel("Ajio", R.drawable.ajio_banner, "https://www.ajio.com"));
        bannerList.add(new BannerModel("Nykaa Fashion", R.drawable.nykaa_banner, "https://www.nykaafashion.com"));

        bannerAdapter = new BannerAdapter(this, bannerList);
        bannerRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        bannerRecyclerView.setAdapter(bannerAdapter);
    }


    private void filterBanners(String searchTerm) {
        if (searchTerm.isEmpty()) {
            // Reset to original list
            setupBannerRecyclerView();
            return;
        }

        // Sort the banners based on whether their name contains the search term
        Collections.sort(bannerList, new Comparator<BannerModel>() {
            @Override
            public int compare(BannerModel o1, BannerModel o2) {
                boolean o1Contains = o1.getName().toLowerCase().contains(searchTerm.toLowerCase());
                boolean o2Contains = o2.getName().toLowerCase().contains(searchTerm.toLowerCase());

                if (o1Contains && !o2Contains) {
                    return -1; // Move o1 up
                } else if (!o1Contains && o2Contains) {
                    return 1; // Move o2 up
                } else {
                    return o1.getName().compareTo(o2.getName()); // Alphabetical order if equal
                }
            }
        });

        // Notify the adapter about changes
        bannerAdapter.notifyDataSetChanged();
    }
}
