# LMS Portal - Netlify Deployment Guide

## GitHub से Netlify पर Deploy करने के लिए Complete Guide

### 1. GitHub Repository Setup

1. **Repository बनाएं:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - LMS Portal"
   git branch -M main
   git remote add origin https://github.com/yourusername/lms-portal.git
   git push -u origin main
   ```

### 2. Netlify Setup

1. **Netlify Account बनाएं:**
   - [netlify.com](https://netlify.com) पर जाएं
   - GitHub से sign up करें

2. **New Site Add करें:**
   - Dashboard में "Add new site" > "Import an existing project" क्लिक करें
   - GitHub को connect करें
   - अपना `lms-portal` repository select करें

### 3. Build Settings

**Build Settings Configure करें:**

```
Build command: cd frontend && npm install && npm run build
Publish directory: frontend/public
```

**Environment Variables Add करें:**
```
NODE_VERSION: 18
PHP_VERSION: 8.1
NPM_VERSION: 9
```

### 4. Netlify Configuration File

`netlify.toml` file already configured है project में:

```toml
[build]
  publish = "frontend/public"
  command = "cd frontend && npm install && npm run build"

[build.environment]
  NODE_VERSION = "18"
  PHP_VERSION = "8.1"
  NPM_VERSION = "9"

[[redirects]]
  from = "/api/*"
  to = "https://your-backend-api.com/api/:splat"
  status = 200
  force = true

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 5. GitHub Actions Setup

अपने GitHub repository में Secrets add करें:

1. GitHub repository में जाएं
2. Settings > Secrets and variables > Actions
3. इन Secrets को add करें:

```
NETLIFY_AUTH_TOKEN: your_netlify_auth_token
NETLIFY_SITE_ID: your_netlify_site_id
```

**Tokens कहाँ से पाएं:**
- Netlify Auth Token: Netlify Dashboard > Site settings > Build & deploy > Continuous Deployment > API access
- Site ID: Netlify Dashboard > Site settings > General > Site details > Site information

### 6. Backend API Configuration

Backend API को deploy करने के लिए:

1. **Backend को Railway/Heroku/Render पर deploy करें:**
   ```bash
   # Railway के लिए
   railway login
   railway init
   railway up
   
   # या Heroku के लिए
   heroku create your-lms-api
   git subtree push --prefix backend heroku main
   ```

2. **Netlify में API URL update करें:**
   - `netlify.toml` में `to = "https://your-backend-api.com/api/:splat"` को update करें
   - या Netlify environment variables में add करें

### 7. Automatic Deployment

अब जब भी आप `main` branch में code push करेंगे:

1. GitHub Actions automatically build करेगा
2. Netlify पर automatically deploy होगा
3. Production site live हो जाएगा

### 8. Custom Domain (Optional)

Custom domain add करने के लिए:

1. Netlify Dashboard > Site settings > Domain management
2. Custom domain add करें
3. DNS settings update करें

### 9. Environment Variables for Production

Production environment variables add करें Netlify में:

```
VITE_API_URL: https://your-backend-api.com
VITE_APP_NAME: LMS Portal
VITE_APP_ENV: production
```

### 10. Testing Deployment

Deploy होने के बाद test करें:

1. **Frontend:** `https://your-site.netlify.app`
2. **API:** `https://your-backend-api.com/docs`
3. **Login functionality test करें**
4. **All user roles test करें** (Student, Instructor, Admin)

### 11. Monitoring और Maintenance

**Netlify Functions के लिए:**
- Site analytics check करें
- Form submissions monitor करें
- Error logs check करें

**Backend monitoring के लिए:**
- Railway/Heroku logs check करें
- Database performance monitor करें
- API response times track करें

### 12. Security Considerations

1. **HTTPS:** Netlify automatically HTTPS provide करता है
2. **Environment Variables:** Sensitive data कभी code में न रखें
3. **API Security:** Backend में proper authentication और CORS setup करें
4. **Rate Limiting:** API calls के लिए rate limiting implement करें

### 13. Backup और Recovery

1. **GitHub:** Code automatically backed up रहता है
2. **Database:** Regular backups schedule करें
3. **Media Files:** Cloud storage (AWS S3) use करें

### 14. Performance Optimization

1. **Images:** Optimize करें और lazy loading implement करें
2. **Code Splitting:** Vue.js में automatic code splitting है
3. **CDN:** Netlify automatically CDN provide करता है
4. **Caching:** Browser caching implement करें

### Troubleshooting Common Issues

**Build Failures:**
- Node.js version check करें
- Dependencies properly install हो रहे हैं या नहीं
- Build logs check करें

**API Connection Issues:**
- CORS settings check करें
- API URL correct है या नहीं
- Environment variables properly set हैं या नहीं

**Login Issues:**
- JWT token properly working है या नहीं
- Backend API accessible है या नहीं
- Frontend और Backend URLs correct हैं या नहीं

यह complete setup आपका LMS Portal को successfully GitHub से Netlify पर deploy करने में मदद करेगा! 🚀
