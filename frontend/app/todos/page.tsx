'use client';

import { useState, useEffect } from 'react';
import TodoList from '@/components/TodoList';
import AddTaskModal from '@/components/AddTaskModal';
import { isAuthenticated, removeAuthToken } from '@/lib/auth';
import { useRouter } from 'next/navigation';

export default function TodosPage() {
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);
  const [mounted, setMounted] = useState(false);
  const router = useRouter();

  useEffect(() => {
    setMounted(true);
    // Check authentication on mount
    if (!isAuthenticated()) {
      router.push('/login');
    }
  }, [router]);

  const handleLogout = () => {
    removeAuthToken();
    router.push('/');
  };

  const handleTaskCreated = () => {
    setRefreshKey(prev => prev + 1);
  };

  if (!mounted) {
    return null;
  }

  if (!isAuthenticated()) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl md:text-3xl font-bold text-gray-900">My Tasks</h1>
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Add Task Button */}
        <div className="mb-6">
          <button
            onClick={() => setIsAddModalOpen(true)}
            className="w-full sm:w-auto px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors flex items-center justify-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add New Task
          </button>
        </div>

        {/* Todo List */}
        <TodoList key={refreshKey} />
      </main>

      {/* Add Task Modal */}
      <AddTaskModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onTaskCreated={handleTaskCreated}
      />
    </div>
  );
}