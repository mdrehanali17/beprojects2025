package com.example.stylematee.model;

public class BannerModel {
    private String name;
    private int imageResId;  // Resource ID for drawable images
    private String linkUrl;  // Link to the website

    // Updated Constructor
    public BannerModel(String name, int imageResId, String linkUrl) {
        this.name = name;
        this.imageResId = imageResId;
        this.linkUrl = linkUrl;
    }

    // Getters
    public String getName() {
        return name;
    }

    public int getImageResId() {
        return imageResId;
    }

    public String getLinkUrl() {
        return linkUrl;
    }
}
