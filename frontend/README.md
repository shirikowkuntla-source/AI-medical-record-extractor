# AI Medical Record Extractor - Frontend

A modern, user-friendly React frontend for the AI Medical Record Extractor application.

## Features

- **📤 File Upload**: Drag-and-drop interface for uploading medical records
- **📝 Text Input**: Direct text input for medical record information
- **📜 History**: View and manage previously extracted records
- **✨ Modern UI**: Beautiful gradient design with smooth animations
- **📱 Responsive**: Works perfectly on desktop, tablet, and mobile devices
- **🔒 Privacy-First**: All processing happens offline with CPU-only inference
- **📊 Results Display**: Clear, organized presentation of extracted medical information
- **📋 Export**: Copy results to clipboard with one click

## Supported File Formats

- **PDF**: Portable Document Format
- **TXT**: Plain text files
- **Images**: PNG, JPG, JPEG, BMP, TIFF (with OCR support)

Maximum file size: 10MB

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend server running (see main README)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file in the frontend directory (optional):
```env
VITE_API_URL=http://localhost:8000/api
```

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Build

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── UploadComponent.jsx      # File upload with drag-and-drop
│   │   ├── TextInputComponent.jsx   # Direct text input
│   │   ├── ResultsComponent.jsx     # Display extracted information
│   │   └── HistoryComponent.jsx     # View extraction history
│   ├── services/
│   │   └── api.js                   # API service functions
│   ├── App.jsx                      # Main application component
│   ├── main.jsx                     # Application entry point
│   └── index.css                    # Global styles
├── index.html                       # HTML template
├── package.json                     # Dependencies and scripts
└── vite.config.js                   # Vite configuration
```

## Components

### UploadComponent
- Drag-and-drop file upload
- Support for multiple file formats
- Upload progress indicator
- File validation and error handling

### TextInputComponent
- Text area for direct input
- Example text provided as placeholder
- Clear and submit functionality

### ResultsComponent
- Organized display of extracted information
- Patient details, diagnosis, symptoms, medications
- Medical history and doctor information
- Confidence score visualization
- Copy to clipboard functionality

### HistoryComponent
- List of all extracted records
- View record details
- Delete records
- Refresh functionality

## API Integration

The frontend connects to the backend API at `/api` (configurable via `VITE_API_URL`).

### Available Endpoints

- `POST /api/extract` - Extract from file
- `POST /api/extract-text` - Extract from text
- `GET /api/records` - Get all records
- `GET /api/records/:id` - Get specific record
- `DELETE /api/records/:id` - Delete record
- `GET /api/health` - Health check

## Styling

The application uses custom CSS with:
- CSS custom properties (variables) for theming
- Gradient backgrounds and modern design
- Smooth animations and transitions
- Responsive grid layouts
- Mobile-first approach

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Technologies Used

- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **React Dropzone**: File upload handling
- **Axios**: HTTP client
- **CSS3**: Styling with modern features

## Development Tips

1. The app uses Vite for fast hot module replacement
2. Environment variables must start with `VITE_` to be accessible
3. API calls are centralized in `src/services/api.js`
4. Components are functional with hooks for state management

## Troubleshooting

### Backend Connection Issues
- Ensure the backend server is running on port 8000
- Check `VITE_API_URL` in your `.env` file
- Verify CORS is enabled on the backend

### File Upload Errors
- Check file size (max 10MB)
- Verify file format is supported
- Ensure backend has necessary dependencies (poppler, tesseract)

### Build Errors
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (should be v16+)

## Contributing

1. Follow the existing code style
2. Test on multiple browsers
3. Ensure responsive design works
4. Add comments for complex logic

## License

MIT License - See LICENSE file for details