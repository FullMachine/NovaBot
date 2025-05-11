'use client';

import React from "react";
import { useTheme } from "./ThemeProvider";

export default function ThemeSwitcher({ className = "" }) {
  const { dark, toggleTheme } = useTheme();

  return (
    <button
      className={`rounded-full p-2 bg-gray-200 dark:bg-gray-700 text-xl mt-4 ${className}`}
      onClick={toggleTheme}
      title="Toggle dark/light mode"
    >
      🌙<span className="sr-only">Toggle dark/light mode</span>
    </button>
  );
} 