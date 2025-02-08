package com.example.stylematee;

import com.google.firebase.Timestamp;

public class UserModel {
    private String name;
    private String email;
    private String phoneNumber;
    private String address;
    private String other;

    // Default constructor required for Firestore
    public UserModel() {}

    // Constructor for phoneNumber, username, and additional fields
    public UserModel(String phoneNumber, String username, Timestamp now, String s) {
        this.phoneNumber = phoneNumber;
        this.name = username;
        this.other = s;
        this.email = ""; // Default value for email
        this.address = ""; // Default value for address
    }

    // Getters and Setters
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getOther() {
        return other;
    }

    public void setOther(String other) {
        this.other = other;
    }

    public void setUsername(String username) {
        this.name = username;
    }

    public String getUsername() {
        return name;
    }
}
