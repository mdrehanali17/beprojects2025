const express = require("express");
const router = express.Router();
const { refreshToken, auth } = require("../controllers/auth");

/**
 * @swagger
 * /refresh-token:
 *   post:
 *     summary: Refresh access and refresh tokens
 *     tags:
 *       - Authentication
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               refresh_token:
 *                 type: string
 *                 description: Refresh token for generating new tokens
 *     responses:
 *       200:
 *         description: New access and refresh tokens
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 access_token:
 *                   type: string
 *                 refresh_token:
 *                   type: string
 *       400:
 *         description: Bad request, refresh token missing or invalid
 *       401:
 *         description: Authentication failed
 */
router.post("/refresh-token", refreshToken);

/**
 * @swagger
 * /signin:
 *   post:
 *     summary: Sign in or register a user
 *     tags:
 *       - Authentication
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               phone:
 *                 type: string
 *                 description: Phone number of the user
 *               role:
 *                 type: string
 *                 enum: [customer, captain]
 *                 description: Role of the user (customer or captain)
 *     responses:
 *       200:
 *         description: User logged in successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 message:
 *                   type: string
 *                 user:
 *                   type: object
 *                 access_token:
 *                   type: string
 *                 refresh_token:
 *                   type: string
 *       201:
 *         description: New user created successfully
 *       400:
 *         description: Missing or invalid phone number/role
 */
router.post("/signin", auth);

module.exports = router;
