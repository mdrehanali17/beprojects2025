import { Text, View } from "react-native";
import React, { useCallback, useMemo, useRef, useState } from "react";
import { homeStyles } from "@/styles/homeStyles";
import { StatusBar } from "expo-status-bar";
import LocationBar from "@/components/customer/LocationBar";
import { useUserStore } from "@/store/userStore";
import { useWS } from "@/service/WSProvider";
import { screenHeight } from "@/utils/Constants";
import DraggableMap from "@/components/customer/DraggableMap";
import BottomSheet, { BottomSheetScrollView } from "@gorhom/bottom-sheet";
import SheetContent from "@/components/customer/SheetContent";
import { commonStyles } from "@/styles/commonStyles";
import { SafeAreaView } from "react-native-safe-area-context";

const androidHeights = [screenHeight * 0.12, screenHeight * 0.42];

export default function Home() {
  const { location } = useUserStore();
  const { disconnect } = useWS();

  const bottomSheetRef = useRef(null);
  const snapPoints = useMemo(() => androidHeights, []);

  const [mapHeight, setMapHeight] = useState(snapPoints[0]);

  const handleSheetChanges = useCallback((index: number) => {
    let height = screenHeight * 0.8;
    if (index == 1) {
      height = screenHeight * 0.5;
    }
    setMapHeight(height);
  }, []);

  return (
    <SafeAreaView style={homeStyles.container}>
      <StatusBar style="light" backgroundColor="black" translucent={false} />
      <LocationBar />
      <DraggableMap height={mapHeight} />

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
        <BottomSheetScrollView
          contentContainerStyle={homeStyles.scrollContainer}
        >
          <SheetContent />
        </BottomSheetScrollView>
      </BottomSheet>
    </SafeAreaView>
  );
}
