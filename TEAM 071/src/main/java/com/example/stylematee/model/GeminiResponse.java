package com.example.stylematee.model;

public class GeminiResponse {
    private Candidate[] candidates;

    public String getText() {
        return candidates[0].content.parts[0].text;
    }

    private static class Candidate {
        private Content content;
    }

    private static class Content {
        private Part[] parts;
    }

    private static class Part {
        private String text;
    }
}
