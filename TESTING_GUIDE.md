# Testing Guide for Todo Application

This guide will help you test all features of the Todo application to ensure everything is working correctly.

## Prerequisites

Before testing, make sure:
- ✅ Backend is running on `http://localhost:8000`
- ✅ Frontend is running on `http://localhost:3000`
- ✅ Database is connected and accessible

## Test Scenarios

### 1. User Registration (Signup)

**Steps:**
1. Open `http://localhost:3000`
2. Click "Get Started" button
3. Enter a new email (e.g., `test@example.com`)
4. Enter a password (e.g., `password123`)
5. Confirm the password
6. Click "Create Account"

**Expected Results:**
- ✅ User is created successfully
- ✅ JWT token is stored in localStorage
- ✅ User is redirected to `/todos` page
- ✅ No error messages appear

**Common Issues:**
- ❌ "Email already registered" - Use a different email
- ❌ "Network error" - Check if backend is running
- ❌ "Passwords do not match" - Ensure passwords match

---

### 2. User Login (Signin)

**Steps:**
1. Go to `http://localhost:3000/login`
2. Enter your email
3. Enter your password
4. Click "Sign In"

**Expected Results:**
- ✅ User is authenticated
- ✅ JWT token is stored
- ✅ Redirected to todos page
- ✅ Can see "My Tasks" header

**Common Issues:**
- ❌ "Invalid email or password" - Check credentials
- ❌ Stuck on login page - Check browser console for errors

---

### 3. Create a New Task

**Steps:**
1. On the todos page, click "Add New Task"
2. Enter a task title (e.g., "Buy groceries")
3. Optionally add a description (e.g., "Milk, eggs, bread")
4. Click "Add Task"

**Expected Results:**
- ✅ Modal closes automatically
- ✅ New task appears in the list
- ✅ Task shows title and description
- ✅ Task is marked as incomplete (unchecked)

**Common Issues:**
- ❌ Modal doesn't close - Check for JavaScript errors
- ❌ Task doesn't appear - Refresh the page
- ❌ "Title is required" - Enter a title

---

### 4. Mark Task as Complete

**Steps:**
1. Find an incomplete task in your list
2. Click the circular checkbox on the left
3. Observe the visual change

**Expected Results:**
- ✅ Checkbox shows a green checkmark
- ✅ Task title gets a strikethrough
- ✅ Task background changes to gray
- ✅ Change persists after page refresh

**Common Issues:**
- ❌ Task doesn't update - Check network tab for API errors
- ❌ Change reverts - Backend might not be saving

---

### 5. Delete a Task

**Steps:**
1. Find any task in your list
2. Click the trash icon on the right
3. Observe the task removal

**Expected Results:**
- ✅ Task is removed from the list immediately
- ✅ Task doesn't reappear after refresh
- ✅ No error messages

**Common Issues:**
- ❌ Task reappears - Backend deletion failed
- ❌ Error message - Check authorization

---

### 6. User Logout

**Steps:**
1. On the todos page, click "Logout" button (top right)
2. Observe the redirect

**Expected Results:**
- ✅ JWT token is removed from localStorage
- ✅ Redirected to home page
- ✅ Cannot access `/todos` without logging in again

**Common Issues:**
- ❌ Still can access todos - Clear browser cache
- ❌ Not redirected - Check browser console

---

### 7. Protected Route Access

**Steps:**
1. Logout if logged in
2. Try to access `http://localhost:3000/todos` directly
3. Observe the behavior

**Expected Results:**
- ✅ Automatically redirected to `/login`
- ✅ Cannot see todos without authentication

**Common Issues:**
- ❌ Can see todos - Authentication check failed

---

### 8. Responsive Design (Mobile)

**Steps:**
1. Open browser DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select a mobile device (e.g., iPhone 12)
4. Test all features

**Expected Results:**
- ✅ Layout adapts to mobile screen
- ✅ Buttons are touch-friendly
- ✅ Text is readable
- ✅ All features work on mobile

---

### 9. Multiple Users Isolation

**Steps:**
1. Create User A and add some tasks
2. Logout
3. Create User B and add different tasks
4. Verify User B cannot see User A's tasks
5. Login as User A again
6. Verify User A's tasks are still there

**Expected Results:**
- ✅ Each user sees only their own tasks
- ✅ Tasks are properly isolated
- ✅ No data leakage between users

---

### 10. API Direct Testing

**Steps:**
1. Open `http://localhost:8000/docs`
2. Try the `/api/auth/signup` endpoint
3. Copy the access_token from response
4. Click "Authorize" button
5. Paste token as `Bearer <token>`
6. Try `/api/todos` GET endpoint

**Expected Results:**
- ✅ Swagger UI loads correctly
- ✅ Can test all endpoints
- ✅ Authentication works
- ✅ Returns user-specific data

---

## Performance Testing

### Load Time
- Home page should load in < 2 seconds
- Todos page should load in < 2 seconds
- Task operations should complete in < 1 second

### Browser Compatibility
Test on:
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari (if on Mac)

---

## Security Testing

### JWT Token
1. Open browser DevTools → Application → Local Storage
2. Find `auth_token`
3. Copy the token
4. Go to `https://jwt.io`
5. Paste and decode

**Expected:**
- Token contains `sub` (user ID)
- Token contains `email`
- Token has expiration time

### CORS
1. Try accessing API from different origin
2. Should be blocked by CORS policy

---

## Troubleshooting Common Issues

### "Network Error"
- Check if backend is running: `http://localhost:8000`
- Check if frontend .env.local has correct API URL
- Check browser console for CORS errors

### "401 Unauthorized"
- Token might be expired (15 minutes)
- Logout and login again
- Check if token exists in localStorage

### "Failed to fetch"
- Backend might be down
- Check backend terminal for errors
- Verify DATABASE_URL in backend .env

### Tasks not loading
- Check browser console for errors
- Verify JWT token is being sent in headers
- Check backend logs for database errors

### Styling issues
- Run `npm run dev` to rebuild
- Clear browser cache
- Check if Tailwind CSS is configured correctly

---

## Success Criteria

All tests pass when:
- ✅ Users can signup and login
- ✅ Users can create, read, update, delete tasks
- ✅ Tasks are properly isolated per user
- ✅ UI is responsive on mobile and desktop
- ✅ Authentication is secure with JWT
- ✅ No console errors
- ✅ All API endpoints work correctly

---

## Reporting Issues

If you find bugs:
1. Note the exact steps to reproduce
2. Check browser console for errors
3. Check backend terminal for errors
4. Note your environment (OS, browser, versions)
5. Take screenshots if applicable

Happy Testing! 🎉
