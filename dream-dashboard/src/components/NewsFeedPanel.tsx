'use client';

import React from "react";
import { Card } from "./ui/card";

interface NewsItem {
  source: string;
  text: string;
}

interface PlayerType {
  name: string;
  team: string;
  position: string;
  photo: string;
  [key: string]: any;
}

const news = [
  {
    source: "@wojespn",
    text: "Breaking: Luka Dončić drops 40 in playoff win!",
  },
  {
    source: "@ESPNStatsInfo",
    text: "Patrick Mahomes now leads the NFL in passing TDs for the 3rd straight year.",
  },
  {
    source: "@ShamsCharania",
    text: "Jayson Tatum expected to return for Game 2, per sources.",
  },
  {
    source: "@OptaJoe",
    text: "Erling Haaland has scored 10+ goals in 3 consecutive UCL campaigns.",
  },
];

export default function NewsFeedPanel({ player, news = [] }: { player?: PlayerType; news?: NewsItem[] }) {
  return (
    <Card className="bg-white text-black dark:bg-gray-900 dark:text-white p-6 border-l-4 border-purple-700 dark:border-purple-500 flex flex-col gap-2 h-full">
      <h3 className="text-xl font-bold text-purple-700 dark:text-purple-400 mb-2">News & Social Feed</h3>
      <ul className="text-base space-y-3">
        {news.length > 0 ? news.map((item, i) => (
          <li key={i}>
            <span className="block text-purple-700 dark:text-purple-300 font-semibold text-base">{item.source}</span>
            <span className="block text-gray-700 dark:text-gray-300 text-base">{item.text}</span>
          </li>
        )) : <li className="text-gray-400">No news available for this sport yet.</li>}
      </ul>
    </Card>
  );
} 