"use client";
import { useEffect } from "react";

export default function StagewiseToolbarClient() {
  useEffect(() => {
    if (typeof window !== "undefined" && process.env.NODE_ENV === "development") {
      import("@stagewise/toolbar").then(({ initToolbar }) => {
        const stagewiseConfig = { plugins: [] };
        initToolbar(stagewiseConfig);
      }).catch(() => {});
    }
  }, []);
  return null;
} 