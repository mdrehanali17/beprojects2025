import { View, Text, FlatList, Image } from "react-native";
import React, { useEffect, useState } from "react";
import CaptainHeader from "@/components/captain/CaptainHeader";
import { homeStyles } from "@/styles/homeStyles";
import CustomText from "@/components/shared/CustomText";
import { useCaptainStore } from "@/store/captainStore";
import { captainStyles } from "@/styles/captainStyles";
import CaptainRidesItem from "@/components/captain/CaptainRidesItem";
import { StatusBar } from "expo-status-bar";
import * as Location from "expo-location";
import { useWS } from "@/service/WSProvider";
import { getMyRides } from "@/service/rideService";
import { useIsFocused } from "@react-navigation/native";

const Home = () => {
  const isFocused = useIsFocused();
  const { emit, on, off } = useWS();
  const { onDuty, setLocation } = useCaptainStore();

  const [rideOffers, setRideOffers] = useState<any[]>([]);

  useEffect(() => {
    let locationSubscription: any;

    const startLocationUpdates = async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status === "granted") {
        locationSubscription = await Location.watchPositionAsync(
          {
            accuracy: Location.Accuracy.High,
            timeInterval: 5000,
            distanceInterval: 10,
          },
          (location) => {
            const { latitude, longitude, heading } = location.coords;
            setLocation({
              latitude: latitude,
              longitude: longitude,
              address: "Somewhere",
              heading: heading as number,
            });
            emit("updateLocation", {
              latitude,
              longitude,
              heading,
            });

            console.log(
              `Location updated: Lat ${latitude}, Lon ${longitude}, Heading: ${heading}`
            );
          }
        );
      } else {
        console.log("Location permission denied");
      }
    };

    if (onDuty && isFocused) {
      startLocationUpdates();
    }

    return () => {
      if (locationSubscription) {
        locationSubscription.remove();
      }
    };
  }, [onDuty, isFocused]);

  useEffect(() => {
    if (onDuty && isFocused) {
      on("rideOffer", (rideDetails: any) => {
        setRideOffers((prevOffers) => {
          const existingIds = new Set(prevOffers.map((offer) => offer._id));
          if (!existingIds.has(rideDetails._id)) {
            return [...prevOffers, rideDetails];
          }
          return prevOffers;
        });
      });
    }

    return () => {
      off("rideOffer");
    };
  }, [onDuty, on, off, isFocused]);

  const removeRide = (id: string) => {
    setRideOffers((prevOffers) =>
      prevOffers.filter((offer) => offer._id !== id)
    );
  };

  const renderRides = ({ item }: any) => {
    return (
      <CaptainRidesItem removeIt={() => removeRide(item._id)} item={item} />
    );
  };

  useEffect(() => {
    getMyRides(false);
  }, []);

  return (
    <View style={homeStyles.container}>
      <StatusBar style="light" backgroundColor="black" translucent={false} />
      <CaptainHeader />

      <FlatList
        data={!onDuty ? [] : rideOffers}
        renderItem={renderRides}
        style={{ flex: 1 }}
        contentContainerStyle={{ padding: 10, paddingBottom: 120 }}
        keyExtractor={(item: any) => item._id || Math.random().toString()}
        ListEmptyComponent={
          <View style={captainStyles.emptyContainer}>
            <Image
              source={require("@/assets/icons/ride.jpg")}
              style={captainStyles.emptyImage}
            />
            <CustomText fontSize={12} style={{ textAlign: "center" }}>
              {onDuty
                ? "There are no available rides! Stay Active"
                : "You're currently OFF-DUTY, please go ON DUTY to start earning"}
            </CustomText>
          </View>
        }
      />
    </View>
  );
};

export default Home;
