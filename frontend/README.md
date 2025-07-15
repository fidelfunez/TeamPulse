# TeamPulse Frontend

React-based frontend for TeamPulse, built with TypeScript, Vite, Tailwind CSS, and shadcn/ui components.

## Features

- **Modern UI**: Clean, responsive design with dark mode support
- **Authentication**: Secure login with JWT token management
- **Role-Based Access**: Different interfaces for admin and employee users
- **Real-time Updates**: Live data updates and notifications
- **Analytics Dashboard**: Interactive charts and insights
- **Responsive Design**: Works on desktop, tablet, and mobile

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (Radix UI)
- **Routing**: React Router DOM
- **Forms**: React Hook Form with Zod validation
- **Charts**: Recharts
- **Icons**: Lucide React
- **State Management**: React Context API

## Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:5173`

## Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── ui/             # shadcn/ui components
│   ├── Layout.tsx      # Main layout component
│   ├── ProtectedRoute.tsx
│   └── ...
├── contexts/           # React contexts
│   └── AuthContext.tsx
├── hooks/              # Custom React hooks
│   ├── useAuth.ts
│   ├── useApi.ts
│   └── ...
├── lib/               # Utility functions
│   ├── api.ts         # API client
│   ├── utils.ts       # Helper functions
│   └── ...
├── pages/             # Page components
│   ├── Login.tsx
│   ├── Dashboard.tsx
│   ├── CheckIn.tsx
│   └── ...
├── types/             # TypeScript type definitions
│   ├── auth.ts
│   ├── user.ts
│   └── ...
├── App.tsx            # Main App component
├── main.tsx           # React entry point
└── index.css          # Global styles
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:5000
VITE_APP_NAME=TeamPulse
```

### Vite Configuration

The Vite configuration includes:
- React plugin
- Path aliases (`@/` points to `src/`)
- API proxy for development
- TypeScript support

### Tailwind Configuration

The Tailwind configuration includes:
- shadcn/ui color system
- Custom animations
- Responsive breakpoints
- Dark mode support

## Components

### UI Components (shadcn/ui)

All shadcn/ui components are available in `src/components/ui/`:

- `Button` - Various button styles
- `Card` - Content containers
- `Dialog` - Modal dialogs
- `Form` - Form components
- `Input` - Text inputs
- `Select` - Dropdown selects
- `Table` - Data tables
- `Toast` - Notifications
- And more...

### Custom Components

- `Layout` - Main application layout
- `ProtectedRoute` - Route protection
- `Navigation` - Main navigation
- `Sidebar` - Admin sidebar
- `CheckInForm` - Check-in form
- `AnalyticsChart` - Chart components

## Pages

### Authentication
- `Login` - User login page

### Employee Pages
- `Dashboard` - Employee dashboard
- `CheckIn` - Weekly check-in form

### Admin Pages
- `AdminDashboard` - Admin overview
- `Users` - User management
- `Teams` - Team management
- `Projects` - Project management
- `Analytics` - Analytics dashboard

## Hooks

### useAuth
Authentication state management:

```typescript
const { user, login, logout, isLoading } = useAuth();
```

### useApi
API client with authentication:

```typescript
const { get, post, put, del } = useApi();
```

## API Integration

The frontend communicates with the backend API through the `useApi` hook, which automatically:

- Adds JWT tokens to requests
- Handles authentication errors
- Provides loading states
- Manages request/response types

## Styling

### Tailwind CSS
The application uses Tailwind CSS for styling with:

- Custom color palette
- Responsive design
- Dark mode support
- Component variants

### CSS Variables
Custom CSS variables for theming:

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 221.2 83.2% 53.3%;
  /* ... */
}
```

## State Management

The application uses React Context API for state management:

- `AuthContext` - Authentication state
- `ThemeContext` - Theme preferences (future)
- `NotificationContext` - Toast notifications (future)

## Routing

React Router DOM handles routing with:

- Protected routes for authenticated users
- Admin-only routes
- Nested routing for layouts
- Route-based code splitting (future)

## TypeScript

The application is fully typed with TypeScript:

- API response types
- Component prop types
- Hook return types
- Utility function types

## Development

### Code Style
- ESLint configuration
- Prettier formatting
- TypeScript strict mode
- React best practices

### Testing
- Unit tests with Jest (future)
- Component tests with React Testing Library (future)
- E2E tests with Playwright (future)

## Building for Production

1. **Build the application**
   ```bash
   npm run build
   ```

2. **Preview the build**
   ```bash
   npm run preview
   ```

3. **Deploy to Netlify**
   - Connect GitHub repository
   - Set build command: `npm run build`
   - Set publish directory: `dist`
   - Add environment variables in dashboard

## Performance

### Optimizations
- Code splitting with React.lazy
- Image optimization
- Bundle analysis
- Tree shaking

### Monitoring
- Error boundaries
- Performance monitoring (future)
- Analytics integration (future)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Follow React best practices
2. Use TypeScript for all new code
3. Add proper prop types
4. Write tests for new components
5. Follow the existing code style

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Check backend server is running
   - Verify API URL in environment
   - Check CORS configuration

2. **Build Errors**
   - Clear node_modules and reinstall
   - Check TypeScript errors
   - Verify all dependencies

3. **Styling Issues**
   - Check Tailwind configuration
   - Verify CSS imports
   - Check component variants

## License

MIT License 