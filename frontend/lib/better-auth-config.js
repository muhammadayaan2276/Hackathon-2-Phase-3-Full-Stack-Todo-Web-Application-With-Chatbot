import { betterAuth } from "better-auth";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "your-super-secret-key-here",
  // Configure JWT plugin
  plugins: [
    // JWT plugin configuration
  ],
  // Additional configuration
});