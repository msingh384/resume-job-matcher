# Frontend - Resume-Job Matcher

Modern React frontend for the Resume-Job Matcher application.

## Tech Stack

- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **Lucide React**: Icon library

## Development

```bash
# Install dependencies
npm install

# Start development server (with backend proxy)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── components/
│   ├── ResumeUpload.jsx       # Drag-and-drop resume upload
│   ├── JobList.jsx            # List of all jobs
│   ├── JobCard.jsx            # Individual job card with actions
│   ├── AddJobModal.jsx        # Modal for adding new jobs
│   └── MatchDetailsModal.jsx  # Detailed match analysis modal
├── App.jsx                     # Main application component
├── api.js                      # API service layer
├── main.jsx                    # Entry point
└── index.css                   # Tailwind CSS imports and custom styles
```

## API Integration

The frontend communicates with the Flask backend through `/api` endpoints. In development, Vite proxies API requests to `http://localhost:5000`.

## Building for Production

```bash
npm run build
```

The build output goes to `dist/` and is served by the Flask backend in production mode.

## Customization

### Colors
Edit `tailwind.config.js` to customize the color scheme:

```js
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors
      }
    }
  }
}
```

### Components
All components are in `src/components/` and use Tailwind CSS for styling.

## Environment

The frontend automatically detects the backend URL:
- Development: Uses Vite proxy to `localhost:5000`
- Production: Served from Flask at the same origin

## Features

- 📱 Fully responsive design
- 🎨 Modern, clean UI with smooth transitions
- 🚀 Fast development with HMR (Hot Module Replacement)
- ♿ Accessible components
- 🎯 Optimized production builds

