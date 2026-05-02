# EventSarthi Frontend - Planner Dashboard

React-based frontend application for event planners to manage events, guests, documents, and FAQs.

## 🚀 Features

### Authentication
- **Phone-based Login**: Secure authentication using phone number and password
- **JWT Token Management**: Automatic token refresh and session management
- **Protected Routes**: Secure access to dashboard and management pages

### Dashboard
- **Event Overview**: View all events with statistics
- **Quick Stats**: Total events, upcoming events, completed events, and total guests
- **Event Management**: Create, view, and manage events
- **Quick Actions**: Fast access to common tasks

### Document Upload
- **Multi-format Support**: Upload PDF, CSV, Excel, and image files
- **Drag & Drop**: Easy file upload with drag-and-drop interface
- **Progress Tracking**: Real-time upload progress for each file
- **File Types**:
  - Guest lists (CSV/Excel)
  - Event menus (PDF)
  - Venue maps (Images/PDF)
  - Event schedules (PDF/Excel)
  - FAQ documents

### Guest Management
- **Bulk Upload**: Import guests from CSV or Excel files
- **Template Download**: Pre-formatted template for guest data
- **Guest Information**:
  - Name, phone, email
  - Relation type (uncle, aunt, friend, colleague, VIP)
  - Room assignments
  - Food preferences
  - VIP levels
  - Check-in status
- **Search & Filter**: Find guests quickly
- **Real-time Updates**: Live guest list updates

### FAQ Management
- **Category-based Organization**: 
  - Venue
  - Food
  - Schedule
  - Transport
  - Accommodation
  - General
- **CRUD Operations**: Create, read, update, and delete FAQs
- **AI Integration**: FAQs are used by the AI bot to answer guest queries
- **Rich Text Support**: Detailed answers with formatting

## 📋 Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running on `http://localhost:8000`

## 🛠️ Installation

1. **Clone and navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env`:
   ```env
   VITE_API_URL=http://localhost:8000/api/v1
   VITE_ENV=development
   ```

4. **Start development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

   Application will be available at `http://localhost:3000`

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable components
│   │   ├── auth/           # Authentication components
│   │   │   └── LoginForm.tsx
│   │   └── documents/      # Document upload components
│   │       └── DocumentUpload.tsx
│   │
│   ├── pages/              # Page components
│   │   ├── Dashboard.tsx   # Main dashboard
│   │   ├── GuestManagement.tsx
│   │   └── FAQManagement.tsx
│   │
│   ├── contexts/           # React contexts
│   │   └── AuthContext.tsx # Authentication state
│   │
│   ├── services/           # API services
│   │   └── api.ts         # API client
│   │
│   ├── types/             # TypeScript types
│   │   └── index.ts       # Type definitions
│   │
│   ├── utils/             # Utility functions
│   ├── hooks/             # Custom React hooks
│   ├── assets/            # Static assets
│   │
│   ├── App.tsx            # Main app component
│   ├── main.tsx           # Entry point
│   └── index.css          # Global styles
│
├── public/                # Public assets
├── index.html            # HTML template
├── package.json          # Dependencies
├── vite.config.ts        # Vite configuration
├── tailwind.config.js    # Tailwind CSS config
├── tsconfig.json         # TypeScript config
└── README.md            # This file
```

## 🎨 Tech Stack

- **React 18**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **React Hot Toast**: Toast notifications
- **Lucide React**: Icon library
- **React Dropzone**: File upload
- **XLSX**: Excel file processing
- **PapaParse**: CSV parsing
- **Zustand**: State management (optional)

## 🔑 Key Components

### Authentication Flow
```typescript
// Login
const { login } = useAuth();
await login(phone, password);

// Access protected routes
<ProtectedRoute>
  <Dashboard />
</ProtectedRoute>

// Logout
const { logout } = useAuth();
logout();
```

### Document Upload
```typescript
<DocumentUpload
  eventId={eventId}
  documentType="guest_list"
  onUploadComplete={() => loadGuests()}
  acceptedFileTypes=".pdf,.csv,.xlsx"
  maxFiles={5}
/>
```

### API Integration
```typescript
// Get events
const events = await api.getEvents({ page: 1, page_size: 10 });

// Upload guest list
await api.bulkAddGuests(eventId, guestData);

// Add FAQ
await api.addFAQ(eventId, { question, answer, category });
```

## 📝 Guest List CSV Format

Download the template from the app or use this format:

```csv
name,phone,email,relation_type,room_number,food_preference,vip_level
John Doe,+919876543210,john@example.com,friend,101,vegetarian,0
Jane Smith,+919876543211,jane@example.com,colleague,102,non-vegetarian,1
```

**Required Fields:**
- `name`: Guest full name
- `phone`: Phone number with country code

**Optional Fields:**
- `email`: Email address
- `relation_type`: uncle, aunt, friend, colleague, vip, other
- `room_number`: Hotel room number
- `food_preference`: vegetarian, non-vegetarian, vegan, etc.
- `vip_level`: 0 (regular), 1 (VIP), 2 (VVIP)

## 🚀 Build for Production

```bash
# Build
npm run build
# or
yarn build

# Preview production build
npm run preview
# or
yarn preview
```

Build output will be in the `dist/` directory.

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API base URL | `http://localhost:8000/api/v1` |
| `VITE_ENV` | Environment (development/production) | `development` |

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop (1920px+)
- Laptop (1024px - 1919px)
- Tablet (768px - 1023px)
- Mobile (320px - 767px)

## 🎯 Key Features Implementation

### Phone Authentication
- Uses JWT tokens stored in localStorage
- Automatic token refresh
- Secure API calls with Bearer token
- Session persistence across page reloads

### File Upload
- Drag-and-drop interface
- Multiple file support
- Progress tracking
- File type validation
- Size limits
- Error handling

### Guest Management
- CSV/Excel parsing
- Bulk import
- Data validation
- Search and filter
- Real-time updates

### FAQ Management
- Category-based organization
- CRUD operations
- Modal-based editing
- Validation

## 🐛 Troubleshooting

### TypeScript Errors
The TypeScript errors shown are expected before running `npm install`. They will be resolved once dependencies are installed.

### API Connection Issues
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in backend
- Verify `VITE_API_URL` in `.env`

### Build Issues
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf .vite
```

## 📚 Additional Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [React Router](https://reactrouter.com)

## 🤝 Contributing

1. Follow the existing code structure
2. Use TypeScript for type safety
3. Follow Tailwind CSS conventions
4. Add comments for complex logic
5. Test on multiple screen sizes

## 📄 License

MIT License - see LICENSE file for details

---

**Built with ❤️ for EventSarthi**