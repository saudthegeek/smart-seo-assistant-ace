# 🚀 Smart SEO Assistant - Deployment Guide

## Pre-Deployment Checklist ✅

### 1. Environment Setup

Before deploying, ensure you have:

- [ ] Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Git repository cloned

### 2. Environment Variables

Set the following environment variables:

```bash
# Required
set GEMINI_API_KEY=your-actual-gemini-api-key-here

# Optional (will use secure defaults)
set JWT_SECRET_KEY=your-custom-jwt-secret-key
```

### 3. Quick Start Commands

```bash
# Check environment
python check_env.py

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies  
cd ../frontend
npm install

# Build frontend for production
npm run build

# Start backend server
cd ../backend
python start_server.py

# In another terminal, test with demo
cd ..
python demo.py
```

## 🏗️ Production Deployment

### Local Development

1. **Backend Development Server:**
   ```bash
   cd backend
   python start_server.py
   # Available at: http://localhost:8000
   # API Docs: http://localhost:8000/docs
   ```

2. **Frontend Development Server:**
   ```bash
   cd frontend
   npm run dev
   # Available at: http://localhost:5173
   ```

3. **Test Everything:**
   ```bash
   python demo.py
   ```

### Production Build

1. **Build Frontend:**
   ```bash
   cd frontend
   npm run build
   # Creates dist/ folder with production files
   ```

2. **Production Backend:**
   ```bash
   cd backend
   # Set production environment variables
   set GEMINI_API_KEY=your-production-key
   set JWT_SECRET_KEY=your-secure-production-secret
   
   # Start with production settings
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### Docker Deployment (Optional)

Create `Dockerfile` for backend:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt

ENV GEMINI_API_KEY=""
ENV JWT_SECRET_KEY=""

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
  
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend/dist:/usr/share/nginx/html
```

### Cloud Deployment Options

#### 1. Vercel (Frontend) + Railway (Backend)
- **Frontend:** Deploy to Vercel with `npm run build`
- **Backend:** Deploy to Railway with Python runtime

#### 2. Netlify (Frontend) + Heroku (Backend)
- **Frontend:** Deploy to Netlify with build command `npm run build`
- **Backend:** Deploy to Heroku with Python buildpack

#### 3. AWS/GCP/Azure
- **Frontend:** S3 + CloudFront / Storage + CDN
- **Backend:** EC2 / Compute Engine / App Service

## 🔒 Security Considerations

### Environment Variables
- Never commit API keys to version control
- Use secure random strings for JWT secrets
- Consider using environment variable management services

### API Security
- JWT tokens expire after 7 days (configurable)
- CORS is configured for common development origins
- All user inputs are validated with Pydantic models

### Database Security
- SQLite is used for simplicity (consider PostgreSQL for production)
- User passwords are hashed with bcrypt
- Prepared statements prevent SQL injection

## 📊 Monitoring & Analytics

### Health Checks
- `GET /health` - Basic health check
- `GET /stats` - Pipeline statistics
- Monitor response times and error rates

### Logging
- FastAPI automatically logs requests
- Add structured logging for production monitoring
- Consider tools like Sentry for error tracking

## 🚀 Performance Optimization

### Backend
- Async/await used throughout for better concurrency
- Background tasks for long-running operations
- Caching can be added for frequently accessed data

### Frontend
- Vite for fast builds and hot reloading
- TailwindCSS purged for minimal CSS bundle
- Lazy loading and code splitting can be added

## 🔧 Maintenance

### Updates
- Keep dependencies updated regularly
- Monitor Google Gemini API changes
- Test thoroughly after any LLM provider updates

### Backups
- SQLite database files should be backed up regularly
- Consider automated backup solutions for production

### Scaling
- Add Redis for session storage and caching
- Consider horizontal scaling with load balancers
- Monitor API rate limits and implement backoff strategies

## 📞 Support

For deployment issues:
1. Check `python check_env.py` output
2. Verify all environment variables are set
3. Ensure API keys have proper permissions
4. Check logs for detailed error messages

---

**Ready for production deployment! 🎉**
