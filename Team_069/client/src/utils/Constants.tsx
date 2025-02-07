import { Dimensions } from "react-native";

export const screenHeight = Dimensions.get("screen").height;
export const screenWidth = Dimensions.get("screen").width;

export enum Colors {
  primary = "#000000", // Uber's primary dark color (black)
  background = "#FFFFFF", // Background (white)
  text = "#000000", // Text (black)
  theme = "#EB001B", // Accent color (red for actions)
  secondary = "#F2F2F2", // Light gray for secondary elements
  tertiary = "#CCCCCC", // Medium gray for tertiary elements
  secondary_light = "#EDEDED", // Very light gray for backgrounds or borders
  iosColor = "#000000", // Dark color for iOS-specific elements
}
