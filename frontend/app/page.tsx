'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { isAuthenticated } from '@/lib/auth';

export default function Home() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // If already authenticated, redirect to todos
    if (isAuthenticated()) {
      router.push('/todos');
    }
  }, [router]);

  if (!mounted) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          {/* Hero Section */}
          <div className="mb-12">
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              Welcome to Todo App
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8">
              Organize your tasks, boost your productivity, and achieve your goals
            </p>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-8 mb-12">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">✅</div>
              <h3 className="text-xl font-semibold mb-2">Simple & Clean</h3>
              <p className="text-gray-600">Easy-to-use interface for managing your daily tasks</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="text-xl font-semibold mb-2">Secure</h3>
              <p className="text-gray-600">Your data is protected with JWT authentication</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">📱</div>
              <h3 className="text-xl font-semibold mb-2">Responsive</h3>
              <p className="text-gray-600">Works seamlessly on desktop and mobile devices</p>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button
              onClick={() => router.push('/signup')}
              className="w-full sm:w-auto px-8 py-3 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
            >
              Get Started
            </button>
            <button
              onClick={() => router.push('/login')}
              className="w-full sm:w-auto px-8 py-3 bg-white text-blue-600 text-lg font-semibold rounded-lg border-2 border-blue-600 hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
            >
              Sign In
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}