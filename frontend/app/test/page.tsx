import ChatBot from '@/components/ChatBot';

export default function TestPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">ChatBot Test Page</h1>
        <p className="text-gray-600 mb-8">
          This is a test page to verify the chatbot functionality. 
          The chatbot should appear in the bottom-right corner when you're authenticated.
        </p>
        
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Test Instructions</h2>
          <ul className="list-disc pl-5 space-y-2 text-gray-700">
            <li>Make sure you're logged in (the chatbot only appears when authenticated)</li>
            <li>Click the floating blue button in the bottom-right corner</li>
            <li>The chat sidebar should slide in from the right</li>
            <li>Type a message and press Enter or click Send</li>
            <li>The chatbot should respond with a message</li>
          </ul>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-medium text-blue-800 mb-2">Important Notes:</h3>
          <p className="text-blue-700 text-sm">
            • The chatbot connects to your deployed /chat endpoint on Hugging Face<br />
            • It uses the URL from your .env.local file: {process.env.NEXT_PUBLIC_API_URL}<br />
            • Make sure your backend is running and the /chat endpoint is accessible
          </p>
        </div>
      </div>
      
      {/* ChatBot will be rendered here when authenticated */}
    </div>
  );
}