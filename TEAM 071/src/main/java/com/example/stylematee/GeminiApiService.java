package com.example.stylematee;

import com.example.stylematee.model.GeminiRequest;
import com.example.stylematee.model.GeminiResponse;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;
import retrofit2.http.Query;

public interface GeminiApiService {
    @POST("v1beta/models/gemini-1.5-flash-latest:generateContent")
    Call<GeminiResponse> getColorCombinations(@Query("key") String apiKey, @Body GeminiRequest request);
}
