const express = require("express");
const axios = require("axios");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
const port = 3000;

app.use(cors()); // Enable Cross-Origin Resource Sharing (CORS) for all origins
app.use(bodyParser.json()); // Parse incoming JSON requests

const GEMINI_API_KEY = "AIzaSyCF6J8_14DN58pEe_oRDergvJ3knsM_qWU"; // Replace with your Gemini API key
const GEMINI_API_URL =
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"; // Gemini API endpoint

// Chat endpoint
app.post("/chat", async (req, res) => {
  const userMessage = req.body.prompt; // Get the user's message from the request body

  try {
    console.log(`Requesting Gemini API with prompt: ${userMessage}`);

    // Send request to Gemini API
    const response = await axios.post(
      GEMINI_API_URL,
      {
        contents: [
          {
            parts: [{ text: userMessage }], // Send the user's message in the correct format
          },
        ],
      },
      {
        headers: {
          "Content-Type": "application/json", // Ensure the request body is in JSON format
        },
        params: {
          key: GEMINI_API_KEY, // Provide the API key as a URL parameter
        },
      }
    );

    // Log the response from the Gemini API
    console.log("Gemini API response:", JSON.stringify(response.data, null, 2));

    // Check if the response contains candidates and content
    if (
      response.data &&
      response.data.candidates &&
      Array.isArray(response.data.candidates) &&
      response.data.candidates.length > 0 &&
      response.data.candidates[0].content
    ) {
      // Extract the bot's response text from the content
      const botResponse = response.data.candidates[0].content.parts[0].text;

      // Send the bot's response as a JSON object
      res.json({ response: botResponse });
    } else {
      console.error("Unexpected response structure:", response.data);
      res.status(500).json({
        error: "Unexpected response structure from Gemini API.",
        details: "The response from Gemini API was not in the expected format.",
      });
    }
  } catch (error) {
    // Log and send error details if there is an error during the request
    console.error("Error interacting with Gemini API:", error);

    if (error.response) {
      // You can log the error response from the API
      console.error("Error response:", error.response.data);
    }

    res.status(500).json({
      error: "Failed to get response from chatbot.",
      details: error.message,
    });
  }
});

// Start the server on port 3000
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
