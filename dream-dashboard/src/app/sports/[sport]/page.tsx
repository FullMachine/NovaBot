import { notFound } from 'next/navigation';

const validSports = [
  'nba', 'nfl', 'mlb', 'soccer', 'tennis', 'esports', 'hockey', 'golf'
];

export default function SportPage({ params }: any) {
  const { sport } = params;
  if (!validSports.includes(sport.toLowerCase())) {
    notFound();
  }
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-4xl font-bold mb-4 capitalize">{sport} Dashboard</h1>
      <p className="text-lg text-gray-500">This is the {sport.toUpperCase()} page. More features coming soon!</p>
    </div>
  );
} 