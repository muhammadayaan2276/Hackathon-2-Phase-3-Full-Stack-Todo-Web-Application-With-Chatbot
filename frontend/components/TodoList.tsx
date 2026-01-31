'use client';

import { useState, useEffect } from 'react';
import { todosApi } from '@/lib/api';
import EditTaskModal from '@/components/EditTaskModal';

interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export default function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null);

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const response = await todosApi.getAll();
      if (response.error) {
        setError(response.error);
      } else {
        setTodos(response.data || []);
      }
    } catch (err) {
      setError('Failed to load todos. Please try again.');
      console.error('Error fetching todos:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleComplete = async (id: string) => {
    try {
      const response = await todosApi.toggleCompletion(id);
      if (response.error) {
        setError('Failed to update todo status.');
      } else {
        // Refresh the list
        fetchTodos();
      }
    } catch (err) {
      setError('Failed to update todo status.');
      console.error('Error toggling todo:', err);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      const response = await todosApi.delete(id);
      if (response.error) {
        setError('Failed to delete todo.');
      } else {
        setTodos(todos.filter(todo => todo.id !== id));
      }
    } catch (err) {
      setError('Failed to delete todo.');
      console.error('Error deleting todo:', err);
    }
  };

  const handleEdit = (todo: Todo) => {
    setEditingTodo(todo);
  };

  const handleTaskUpdated = () => {
    setEditingTodo(null);
    fetchTodos();
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
        <p className="text-red-700">{error}</p>
      </div>
    );
  }

  if (todos.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
        <div className="text-6xl mb-4">📝</div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">No tasks yet</h3>
        <p className="text-gray-500">Create your first task to get started!</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {todos.map((todo) => (
        <div
          key={todo.id}
          className={`flex items-start p-4 rounded-lg border transition-all ${
            todo.completed
              ? 'bg-gray-50 border-gray-200'
              : 'bg-white border-gray-200 hover:shadow-md'
          }`}
        >
          <button
            onClick={() => handleToggleComplete(todo.id)}
            className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center mr-3 mt-0.5 transition-colors ${
              todo.completed
                ? 'bg-green-500 border-green-500'
                : 'border-gray-300 hover:border-blue-500'
            }`}
            aria-label={todo.completed ? "Mark as incomplete" : "Mark as complete"}
          >
            {todo.completed && (
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>

          <div className="flex-1 min-w-0">
            <h3 className={`font-medium text-lg ${todo.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {todo.title}
            </h3>
            {todo.description && (
              <p className={`text-sm mt-1 ${todo.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                {todo.description}
              </p>
            )}
            <p className="text-xs text-gray-400 mt-2">
              Created: {new Date(todo.created_at).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
              })}
            </p>
          </div>

          <button
            onClick={() => handleEdit(todo)}
            className="flex-shrink-0 ml-3 text-gray-400 hover:text-blue-500 p-2 rounded-md hover:bg-blue-50 transition-colors"
            aria-label="Edit todo"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>

          <button
            onClick={() => handleDelete(todo.id)}
            className="flex-shrink-0 ml-3 text-gray-400 hover:text-red-500 p-2 rounded-md hover:bg-red-50 transition-colors"
            aria-label="Delete todo"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      ))}

      {editingTodo && (
        <EditTaskModal
          isOpen={true}
          onClose={() => setEditingTodo(null)}
          task={editingTodo}
          onTaskUpdated={handleTaskUpdated}
        />
      )}
    </div>
  );
}