const express = require("express");
const {
  createRide,
  updateRideStatus,
  acceptRide,
  getMyRides,
} = require("../controllers/ride");

const router = express.Router();

router.use((req, res, next) => {
  req.io = req.app.get("io");
  next();
});

/**
 * @swagger
 * /create:
 *   post:
 *     summary: Create a new ride
 *     tags:
 *       - Rides
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               vehicle:
 *                 type: string
 *                 enum: [bike, auto, cabEconomy, cabPremium]
 *                 description: Vehicle type
 *               pickup:
 *                 type: object
 *                 properties:
 *                   address:
 *                     type: string
 *                   latitude:
 *                     type: number
 *                   longitude:
 *                     type: number
 *                 description: Pickup location details
 *               drop:
 *                 type: object
 *                 properties:
 *                   address:
 *                     type: string
 *                   latitude:
 *                     type: number
 *                   longitude:
 *                     type: number
 *                 description: Drop location details
 *     responses:
 *       201:
 *         description: Ride created successfully
 *       400:
 *         description: Missing or incomplete ride details
 */
router.post("/create", createRide);

/**
 * @swagger
 * /accept/{rideId}:
 *   patch:
 *     summary: Accept a ride request
 *     tags:
 *       - Rides
 *     parameters:
 *       - in: path
 *         name: rideId
 *         required: true
 *         schema:
 *           type: string
 *         description: ID of the ride to accept
 *     responses:
 *       200:
 *         description: Ride accepted successfully
 *       400:
 *         description: Ride is no longer available or invalid ride ID
 *       404:
 *         description: Ride not found
 */
router.patch("/accept/:rideId", acceptRide);

/**
 * @swagger
 * /update/{rideId}:
 *   patch:
 *     summary: Update the status of a ride
 *     tags:
 *       - Rides
 *     parameters:
 *       - in: path
 *         name: rideId
 *         required: true
 *         schema:
 *           type: string
 *         description: ID of the ride to update
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               status:
 *                 type: string
 *                 enum: [START, ARRIVED, COMPLETED]
 *                 description: New status of the ride
 *     responses:
 *       200:
 *         description: Ride status updated successfully
 *       400:
 *         description: Invalid ride status or missing ride ID
 *       404:
 *         description: Ride not found
 */
router.patch("/update/:rideId", updateRideStatus);

/**
 * @swagger
 * /rides:
 *   get:
 *     summary: Get rides associated with the user
 *     tags:
 *       - Rides
 *     parameters:
 *       - in: query
 *         name: status
 *         schema:
 *           type: string
 *         description: Filter rides by status
 *     responses:
 *       200:
 *         description: List of rides retrieved successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 message:
 *                   type: string
 *                 count:
 *                   type: integer
 *                 rides:
 *                   type: array
 *                   items:
 *                     type: object
 *       400:
 *         description: Failed to retrieve rides
 */
router.get("/rides", getMyRides);

module.exports = router;
