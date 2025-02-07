import { View } from "react-native";
import React, { FC } from "react";
import SwipeButton from "rn-swipe-button";
import Ionicons from "@expo/vector-icons/Ionicons";
import { RFValue } from "react-native-responsive-fontsize";
import { Colors } from "@/utils/Constants";
import { rideStyles } from "@/styles/rideStyles";

const SwipeableButton: FC<{
  color?: string;
  title: string;
  onPress: () => void;
}> = ({ color = Colors.iosColor, title, onPress }) => {
  const CheckoutButton = () => (
    <Ionicons
      name="arrow-forward-sharp"
      style={{ bottom: 2 }}
      size={32}
      color="#fff"
    />
  );

  return (
    <View style={rideStyles.swipeableContainer}>
      <SwipeButton
        containerStyles={rideStyles.swipeButtonContainer}
        height={30}
        shouldResetAfterSuccess={true}
        onSwipeSuccess={onPress}
        railBackgroundColor={color}
        railStyles={rideStyles.railStyles}
        railBorderColor="transparent"
        railFillBackgroundColor="rgba(255,255,255,0.6)"
        railFillBorderColor="rgba(255,255,255,0.6)"
        titleColor="#fff"
        titleFontSize={RFValue(13)}
        titleStyles={rideStyles.titleStyles}
        thumbIconComponent={CheckoutButton}
        thumbIconStyles={rideStyles.thumbIconStyles}
        title={title.toUpperCase()}
        thumbIconBackgroundColor="transparent"
        thumbIconBorderColor="transparent"
        thumbIconHeight={50}
        thumbIconWidth={60}
      />
    </View>
  );
};

export default SwipeableButton;
