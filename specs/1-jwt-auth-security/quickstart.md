# Quickstart Guide: JWT Authentication & Security for Todo Application

## Environment Setup

### 1. Configure Shared Secret
Create `.env` file in backend directory:
```env
BETTER_AUTH_SECRET=your-strong-secret-key-here-32-characters-minimum
```

**Security Note**: Never commit `.env` files to version control. Add to `.gitignore`.

### 2. Frontend Setup (Next.js)
Install Better Auth:
```bash
npm install @better-auth/react
```

Configure in `pages/_app.tsx` or equivalent:
```typescript
import { BetterAuth } from '@better-auth/react';

export default function App({ Component, pageProps }) {
  return (
    <BetterAuth 
      config={{
        secret: process.env.NEXT_PUBLIC_BETTER_AUTH_SECRET,
        // Other configuration options
      }}
    >
      <Component {...pageProps} />
    </BetterAuth>
  );
}
```

### 3. Backend Setup (FastAPI)
Install required packages:
```bash
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt]
```

## Implementation Steps

### Step 1: Authentication Flow
1. **User Signup**
   - POST `/api/auth/signup` with `{ "email": "user@example.com", "password": "strong-password" }`
   - Returns JWT token on success

2. **User Signin**
   - POST `/api/auth/signin` with `{ "email": "user@example.com", "password": "strong-password" }`
   - Returns JWT token on success

### Step 2: API Request Handling
For all protected endpoints, include the JWT token:
```http
GET /api/tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 3: Backend Middleware
Implement JWT verification middleware in FastAPI:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError

security = HTTPBearer()

def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(
            token.credentials, 
            settings.BETTER_AUTH_SECRET, 
            algorithms=["HS256"]
        )
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "email": payload.get("email")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Step 4: Task Ownership Enforcement
In all task-related endpoints, validate ownership:
```python
@app.put("/api/tasks/{task_id}")
async def update_task(task_id: str, task_data: TaskUpdate, current_user: dict = Depends(get_current_user)):
    # Verify task belongs to current user
    task = await get_task_by_id(task_id)
    if task.owner_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to modify this task")
    
    # Update task logic here
    return await update_task_in_db(task_id, task_data, current_user["user_id"])
```

## Testing Procedures

### 1. Authentication Testing
- ✅ Test signup with valid credentials → should return JWT
- ✅ Test signin with valid credentials → should return JWT  
- ❌ Test signin with invalid credentials → should return 401
- ✅ Test token validation with valid token → should succeed
- ❌ Test token validation with expired token → should return 401
- ❌ Test token validation with tampered token → should return 401

### 2. Ownership Testing
- ✅ User A creates task → should succeed
- ✅ User A reads their own task → should succeed
- ❌ User B reads User A's task → should return 403
- ❌ User B updates User A's task → should return 403
- ✅ User A updates their own task → should succeed

## Security Best Practices

1. **Token Storage**: Use HttpOnly cookies for JWT storage when possible
2. **Secret Management**: Rotate `BETTER_AUTH_SECRET` periodically
3. **Error Handling**: Use generic error messages to prevent enumeration attacks
4. **Rate Limiting**: Implement rate limiting at infrastructure level (Nginx, Cloudflare, etc.)
5. **Logging**: Sanitize logs to prevent token leakage

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 Unauthorized on all requests | Check `BETTER_AUTH_SECRET` matches between frontend and backend |
| Token not being attached to requests | Verify request interceptor is properly configured |
| 403 Forbidden on owned tasks | Check ownership validation logic and database relationships |
| Token expiration too frequent | Adjust token lifetime in Better Auth configuration |

## Next Steps

1. Implement the authentication flows
2. Integrate with existing todo API endpoints
3. Write comprehensive tests
4. Perform security review
5. Deploy and monitor