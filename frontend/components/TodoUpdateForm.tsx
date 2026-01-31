'use client';

import { useState } from 'react';
import { todosApi } from '@/lib/api';

interface TodoUpdateFormProps {
  todoId: string;
  initialTitle: string;
  initialDescription: string;
  onComplete: () => void;
}

export default function TodoUpdateForm({ 
  todoId, 
  initialTitle, 
  initialDescription,
  onComplete 
}: TodoUpdateFormProps) {
  const [title, setTitle] = useState(initialTitle);
  const [description, setDescription] = useState(initialDescription);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    
    try {
      await todosApi.update(todoId, { title, description });
      onComplete();
    } catch (err) {
      console.error('Error updating todo:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="update-title" className="block text-sm font-medium text-gray-700 mb-1">
          Title
        </label>
        <input
          id="update-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Update task title"
          required
        />
      </div>
      
      <div>
        <label htmlFor="update-description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="update-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={2}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Update description..."
        />
      </div>
      
      <div className="flex gap-2">
        <button
          type="submit"
          disabled={loading}
          className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {loading ? 'Updating...' : 'Update'}
        </button>
        <button
          type="button"
          onClick={onComplete}
          className="flex-1 bg-gray-200 text-gray-800 py-2 px-4 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}