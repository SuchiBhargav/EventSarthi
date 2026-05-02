# EventSarthi Frontend - Complete Setup Guide

This guide will help you set up and run the EventSarthi planner dashboard frontend.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js**: Version 18.0.0 or higher
- **npm**: Version 9.0.0 or higher (comes with Node.js)
- **Git**: For version control

Check your versions:
```bash
node --version  # Should be v18.0.0 or higher
npm --version   # Should be 9.0.0 or higher
```

## 🚀 Quick Start

### Step 1: Navigate to Frontend Directory
```bash
cd frontend
```

### Step 2: Install Dependencies
```bash
npm install
```

This will install all required packages including:
- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios
- And more...

### Step 3: Configure Environment
```bash
cp .env.example .env
```

Edit the `.env` file if needed:
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_ENV=development
```

### Step 4: Start Development Server
```bash
npm run dev
```

The application will start at `http://localhost:3000`

## 🔧 Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

## 📱 Using the Application

### 1. Login
- Navigate to `http://localhost:3000`
- You'll be redirected to the login page
- Enter your phone number and password
- Click "Login"

**Note**: You need to register via the backend API first or use existing credentials.

### 2. Dashboard
After login, you'll see:
- **Statistics**: Total events, upcoming events, completed events, total guests
- **Event List**: All your events with quick actions
- **Quick Actions**: Links to manage events, guests, and documents

### 3. Create Event
1. Click "Create Event" button
2. Fill in event details:
   - Event name
   - Event type (wedding, birthday, corporate, etc.)
   - Description
   - Date and time
   - Venue
   - Expected guests
3. Click "Create"

### 4. Upload Guest List

#### Option A: Using Template
1. Go to Guest Management
2. Click "Download Template"
3. Fill in the Excel/CSV file with guest data
4. Click "Upload Guest List"
5. Select your filled file
6. Guests will be imported automatically

#### Option B: Manual Entry
1. Go to Guest Management
2. Click "Add Guest"
3. Fill in guest details
4. Click "Save"

#### Guest List Format
```csv
name,phone,email,relation_type,room_number,food_preference,vip_level
John Doe,+919876543210,john@example.com,friend,101,vegetarian,0
Jane Smith,+919876543211,jane@example.com,uncle,102,non-vegetarian,0
```

### 5. Upload Documents

Supported document types:
- **Guest Lists**: CSV, Excel (.xlsx, .xls)
- **Menus**: PDF
- **Maps**: Images (JPG, PNG), PDF
- **Schedules**: PDF, Excel
- **FAQs**: PDF, Text files

To upload:
1. Navigate to Documents section
2. Drag and drop files or click to browse
3. Select files (max 5 at a time)
4. Upload progress will be shown
5. Files are automatically categorized

### 6. Manage FAQs

1. Go to FAQ Management
2. Click "Add FAQ"
3. Select category:
   - Venue
   - Food
   - Schedule
   - Transport
   - Accommodation
   - General
4. Enter question and answer
5. Click "Add FAQ"

The AI bot will use these FAQs to answer guest queries via WhatsApp.

## 🎨 Features Overview

### Authentication
- ✅ Phone-based login
- ✅ JWT token management
- ✅ Automatic session persistence
- ✅ Secure API calls

### Dashboard
- ✅ Event statistics
- ✅ Quick event overview
- ✅ Fast navigation
- ✅ Responsive design

### Guest Management
- ✅ Bulk CSV/Excel upload
- ✅ Template download
- ✅ Search and filter
- ✅ Guest details view
- ✅ Check-in status tracking

### Document Upload
- ✅ Drag and drop interface
- ✅ Multiple file support
- ✅ Progress tracking
- ✅ File type validation
- ✅ Error handling

### FAQ Management
- ✅ Category-based organization
- ✅ CRUD operations
- ✅ AI bot integration
- ✅ Easy editing

## 🔍 Troubleshooting

### Issue: Dependencies not installing
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Issue: Port 3000 already in use
```bash
# Kill process on port 3000
# On Mac/Linux:
lsof -ti:3000 | xargs kill -9

# On Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use a different port
npm run dev -- --port 3001
```

### Issue: Cannot connect to backend
1. Ensure backend is running on `http://localhost:8000`
2. Check `.env` file has correct `VITE_API_URL`
3. Verify CORS is enabled in backend
4. Check browser console for errors

### Issue: TypeScript errors
These are expected before `npm install`. After installation:
```bash
# Restart VS Code
# Or restart TypeScript server in VS Code:
# Cmd/Ctrl + Shift + P -> "TypeScript: Restart TS Server"
```

### Issue: Build fails
```bash
# Clear Vite cache
rm -rf .vite

# Clear dist folder
rm -rf dist

# Rebuild
npm run build
```

## 📊 Project Structure Explained

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── auth/           # Login, Register components
│   │   └── documents/      # File upload components
│   │
│   ├── pages/              # Full page components
│   │   ├── Dashboard.tsx   # Main dashboard
│   │   ├── GuestManagement.tsx
│   │   └── FAQManagement.tsx
│   │
│   ├── contexts/           # React Context providers
│   │   └── AuthContext.tsx # Authentication state
│   │
│   ├── services/           # API integration
│   │   └── api.ts         # Axios client with interceptors
│   │
│   ├── types/             # TypeScript definitions
│   │   └── index.ts       # All type definitions
│   │
│   ├── App.tsx            # Main app with routing
│   ├── main.tsx           # React entry point
│   └── index.css          # Global styles + Tailwind
│
├── public/                # Static assets
├── index.html            # HTML template
└── Configuration files...
```

## 🎯 Next Steps

After setup:

1. **Create your first event**
2. **Upload guest list**
3. **Add FAQs for common questions**
4. **Upload event documents** (menu, map, schedule)
5. **Test the dashboard features**

## 📚 Additional Resources

- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [React Router Tutorial](https://reactrouter.com/en/main/start/tutorial)

## 🆘 Getting Help

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review the main README.md
3. Check browser console for errors
4. Verify backend is running and accessible
5. Check network tab in browser dev tools

## 🔐 Security Notes

- Never commit `.env` file
- Keep JWT tokens secure
- Use HTTPS in production
- Validate all user inputs
- Keep dependencies updated

## 🚀 Deployment

For production deployment:

```bash
# Build
npm run build

# Output will be in dist/ folder
# Deploy dist/ folder to:
# - Vercel
# - Netlify
# - AWS S3 + CloudFront
# - Any static hosting service
```

---

**Happy Coding! 🎉**