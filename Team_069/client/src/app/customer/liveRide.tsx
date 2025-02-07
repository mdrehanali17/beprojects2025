import { View, Platform, ActivityIndicator, Alert } from "react-native";
import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { rideStyles } from "@/styles/rideStyles";
import LiveTrackingMap from "@/components/customer/LiveTrackingMap";
import { useRoute } from "@react-navigation/native";
import { screenHeight } from "@/utils/Constants";
import BottomSheet, { BottomSheetScrollView } from "@gorhom/bottom-sheet";
import { StatusBar } from "expo-status-bar";
import SearchingRideSheet from "@/components/customer/SearchingRideSheet";
import LiveTrackingSheet from "@/components/customer/LiveTrackingSheet";
import SwipeableButton from "@/components/customer/SwipeableButton";
import { resetAndNavigate } from "@/utils/Helpers";
import { useWS } from "@/service/WSProvider";

const androidHeights = [screenHeight * 0.12, screenHeight * 0.42];
const iosHeights = [screenHeight * 0.2, screenHeight * 0.5];

const LiveRide = () => {
  const { emit, on, off } = useWS();
  const [rideData, setRideData] = useState<any>(null);
  const [captainCoords, setCaptainCoords] = useState<any>(null);
  const route = useRoute() as any;
  const params = route?.params || {};
  const id = params.id;
  const bottomSheetRef = useRef(null);
  const snapPoints = useMemo(
    () => (Platform.OS === "ios" ? iosHeights : androidHeights),
    []
  );
  const [mapHeight, setMapHeight] = useState(snapPoints[0]);
  const handleSheetChanges = useCallback((index: number) => {
    let height = screenHeight * 0.8;
    if (index == 1) {
      height = screenHeight * 0.5;
    }
    setMapHeight(height);
  }, []);

  useEffect(() => {
    if (id) {
      emit("subscribeRide", id);

      on("rideData", (data) => {
        setRideData(data);
        if (data.status === "SEARCHING_FOR_CAPTAIN") {
          emit("searchCaptain", id);
        }
      });

      on("rideUpdate", (data) => {
        setRideData(data);
      });

      on("rideCanceled", (error) => {
        console.log("Ride error:", error);
        resetAndNavigate("/customer/home");
        Alert.alert("Ride Canceled");
      });

      on("error", (error) => {
        console.log("Ride error:", error);
        resetAndNavigate("/customer/home");
        Alert.alert("Oh Dang! No Riders Found");
      });
    }

    return () => {
      off("rideData");
      off("rideUpdate");
      off("rideCanceled");
      off("error");
    };
  }, [id, emit, on, off]);

  useEffect(() => {
    if (rideData?.captain?._id) {
      emit("subscribeToCaptainLocation", rideData?.captain?._id);
      on("captainLocationUpdate", (data) => {
        console.log("Captain location updated:", data);
        setCaptainCoords(data.coords);
      });
    }
    return () => {
      off("captainLocationUpdate");
    };
  }, [rideData]);

  return (
    <View style={rideStyles.container}>
      <StatusBar style="light" backgroundColor="black" translucent={false} />
      {rideData && (
        <LiveTrackingMap
          status={rideData?.status}
          height={mapHeight}
          drop={{
            latitude: parseFloat(rideData?.drop?.latitude),
            longitude: parseFloat(rideData?.drop?.longitude),
          }}
          pickup={{
            latitude: parseFloat(rideData?.pickup?.latitude),
            longitude: parseFloat(rideData?.pickup?.longitude),
          }}
          captain={
            captainCoords
              ? {
                  latitude: captainCoords.latitude,
                  longitude: captainCoords.longitude,
                  heading: captainCoords.heading,
                }
              : {}
          }
        />
      )}
      {rideData ? (
        <BottomSheet
          ref={bottomSheetRef}
          index={1}
          handleIndicatorStyle={{
            backgroundColor: "#ccc",
          }}
          enableOverDrag={false}
          enableDynamicSizing
          style={{ zIndex: 4 }}
          snapPoints={snapPoints}
          onChange={handleSheetChanges}
        >
          <BottomSheetScrollView contentContainerStyle={rideStyles.container}>
            {rideData?.status === "SEARCHING_FOR_CAPTAIN" ? (
              <SearchingRideSheet item={rideData} />
            ) : (
              <LiveTrackingSheet item={rideData} />
            )}
          </BottomSheetScrollView>
        </BottomSheet>
      ) : (
        <ActivityIndicator color="black" size="large" />
      )}

      {rideData?.status === "ARRIVED" && (
        <SwipeableButton
          title="Complete Ride"
          onPress={() => {}}
          color="#228B22"
        />
      )}
    </View>
  );
};

export default LiveRide;
