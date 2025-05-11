/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    turbo: false, // Disable Turbopack, use Webpack
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
};

module.exports = nextConfig; 