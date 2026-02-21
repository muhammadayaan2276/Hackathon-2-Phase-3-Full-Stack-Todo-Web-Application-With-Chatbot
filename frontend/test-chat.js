// Test script to verify chat endpoint connectivity
// Run this with: node test-chat.js

const https = require('https');

const API_URL = 'https://muhammad-ayaan-hackathon-2-phase-3-full-stack-to-ab1039f.hf.space';
const TEST_MESSAGE = 'Hello, how are you?';

console.log('Testing chat endpoint at:', API_URL);

// Test GET root endpoint first
https.get(`${API_URL}/`, (res) => {
  console.log('Root endpoint status:', res.statusCode);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    console.log('Root response:', data);
    
    // Test chat endpoint
    const postData = JSON.stringify({ message: TEST_MESSAGE });
    
    const options = {
      hostname: 'muhammad-ayaan-hackathon-2-phase-3-full-stack-to-ab1039f.hf.space',
      port: 443,
      path: '/api/chat',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
      }
    };

    const req = https.request(options, (chatRes) => {
      console.log('Chat endpoint status:', chatRes.statusCode);
      
      let chatData = '';
      chatRes.on('data', (chunk) => {
        chatData += chunk;
      });
      
      chatRes.on('end', () => {
        console.log('Chat response:', chatData);
        
        try {
          const parsed = JSON.parse(chatData);
          console.log('Parsed response:', parsed);
        } catch (e) {
          console.log('Response parsing error:', e.message);
        }
      });
    });

    req.on('error', (error) => {
      console.error('Chat request error:', error);
    });

    req.write(postData);
    req.end();
  });
}).on('error', (error) => {
  console.error('Root request error:', error);
});