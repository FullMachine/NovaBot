import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function _SampleBarChart({ data = [] }: { data?: { name: string; value: number }[] }) {
  if (!data || data.length === 0) return null;
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data}>
        <XAxis dataKey="name" stroke="#7e22ce" tick={{ fill: '#7e22ce' }} tickLine={{ stroke: '#7e22ce' }} />
        <YAxis stroke="#7e22ce" tick={{ fill: '#7e22ce' }} tickLine={{ stroke: '#7e22ce' }} />
        <Tooltip contentStyle={{ backgroundColor: '#ede9fe', color: '#7e22ce' }} />
        <Bar dataKey="value" fill="#7e22ce" radius={[6, 6, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
} 