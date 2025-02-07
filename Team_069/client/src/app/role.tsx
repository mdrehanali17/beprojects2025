import { View, Text, Image, TouchableOpacity } from "react-native";
import React from "react";
import { roleStyles } from "@/styles/roleStyles";
import CustomText from "@/components/shared/CustomText";
import { router } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";

export default function Role() {
  const handleCustomerPress = () => {
    router.navigate("/customer/auth");
  };

  const handleCaptainPress = () => {
    router.navigate("/captain/auth");
  };

  return (
    <SafeAreaView style={roleStyles.container}>
      {/* <Image
        source={require("@/assets/images/logo_t.png")}
        style={roleStyles.logo}
      /> */}
      <CustomText fontFamily="Medium" variant="h6" style={roleStyles.header}>
        Choose your user type
      </CustomText>

      <TouchableOpacity style={roleStyles.card} onPress={handleCustomerPress}>
        <Image
          source={require("@/assets/images/customer.png")}
          style={roleStyles.image}
        />
        <View style={roleStyles.cardContent}>
          <CustomText style={roleStyles.title}>Customer</CustomText>
          <CustomText style={roleStyles.description}>
            Are you a customer? Order rides and deliveries easily.
          </CustomText>
        </View>
      </TouchableOpacity>

      <TouchableOpacity style={roleStyles.card} onPress={handleCaptainPress}>
        <Image
          source={require("@/assets/images/role_captain.png")}
          style={roleStyles.image}
        />
        <View style={roleStyles.cardContent}>
          <CustomText style={roleStyles.title}>Captain</CustomText>
          <CustomText style={roleStyles.description}>
            Are you a captain? Join us to drive and deliver.
          </CustomText>
        </View>
      </TouchableOpacity>
    </SafeAreaView>
  );
}
