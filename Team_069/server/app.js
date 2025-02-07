require("dotenv").config();
require("express-async-errors");

const swaggerJSDoc = require("swagger-jsdoc");
const swaggerUI = require("swagger-ui-express");

const EventEmitter = require("events");
EventEmitter.defaultMaxListeners = 100;

const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const connectDB = require("./config/connect");
const notFoundMiddleware = require("./middleware/not-found");
const errorHandlerMiddleware = require("./middleware/error-handler");
const authMiddleware = require("./middleware/authentication");

// Port
const port = 8000;

// Import socket handler
const handleSocketConnection = require("./controllers/sockets");

const app = express();
app.use(express.json());

const server = http.createServer(app);

const io = socketIo(server, { cors: { origin: "*" } });

// Routers
const authRouter = require("./routes/auth");
const rideRouter = require("./routes/ride");

// Swagger
const swaggerOptions = {
  definition: {
    openapi: "3.0.0",
    info: {
      title: "Ride-Share API with Swagger UI",
      version: "1.0.0",
      description: "Ride-Share API with Swagger UI",
    },
    servers: [
      {
        url: `http://localhost:${port}`,
      },
    ],
  },
  apis: ["./routes/*.js"],
};

const swaggerSpec = swaggerJSDoc(swaggerOptions);

app.use("/api-docs", swaggerUI.serve, swaggerUI.setup(swaggerSpec));

// Attach the WebSocket instance to the request object
app.use((req, res, next) => {
  req.io = io;
  return next();
});

// Initialize the WebSocket handling logic
handleSocketConnection(io);

// Routes
app.use("/auth", authRouter);
app.use("/ride", authMiddleware, rideRouter);

// Middleware
app.use(notFoundMiddleware);
app.use(errorHandlerMiddleware);

const start = async () => {
  try {
    await connectDB(process.env.MONGO_URI);

    server.listen(process.env.PORT || 8000, "0.0.0.0", () =>
      // server.listen(process.env.PORT || 3000, () =>
      console.log(
        `HTTP server is running on port http://localhost:${process.env.PORT || 8000
        }`
      )
    );
  } catch (error) {
    console.log(error);
  }
};

start();
