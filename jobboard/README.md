# Job Board Application

A Next.js-based job search platform with real-time job listings and application management.

## Key Highlights

- ✨ **Real-time job search** powered by RemoteOK API
- 🔍 **Advanced filtering system** (category, location, experience level, job type)
- ⚡ **Intelligent search** with 300ms debouncing for optimal performance
- 📝 **Complete job application system** with server-side validation
- 📱 **Responsive design** with mobile-first approach and collapsible filters
- 🚀 **Dynamic API endpoints** with caching for improved performance
- ♿ **Accessible UI** with ARIA labels and keyboard navigation
- 🎨 **Loading states, error handling**, and empty state management

## Tech Stack

**Frontend:** Next.js 15 | TypeScript | React 19 | Tailwind CSS  
**API:** RemoteOK API (real-time remote job listings)  
**State Management:** React Context API  
**Styling:** Tailwind CSS with responsive utilities

---

## Key Design Principles

### **Real-Time First Architecture**
- Live job data from RemoteOK API with no stale information
- Debounced search (300ms) for optimal API efficiency
- Server-side filtering at API level for faster responses
- Response caching (5min/10min stale-while-revalidate) for performance

### **Component-Based Architecture**
- Reusable UI components (JobCard, FilterPanel, JobListings)
- Separation of concerns: API layer, state management, presentation
- Centralized type definitions in `/interfaces`
- Shared constants for maintainability

### **Mobile-First Responsive Design**
- Progressive enhancement from mobile → tablet → desktop
- Collapsible filter panel on small screens
- Fluid typography and spacing (sm:, md:, lg: breakpoints)
- Touch-optimized interactions with adequate tap targets

### **Accessibility (WCAG 2.1 AA)**
- Semantic HTML with proper ARIA attributes
- Keyboard navigation and focus management
- Screen reader support with `aria-live` regions
- Color contrast ratios meeting accessibility standards

### **Performance Optimization**
- API response caching with Cache-Control headers
- Debounced user input to prevent excessive requests
- Code splitting and lazy loading for modals
- Minimal re-renders with React optimization hooks

### **Data Validation & Security**
- Server-side validation for all form submissions
- Input sanitization to prevent XSS attacks
- Type safety with TypeScript throughout
- Environment variables for sensitive configuration

### **Developer Experience**
- TypeScript for type safety and IntelliSense
- JSDoc comments for component documentation
- Consistent naming conventions and file structure
- Comprehensive error handling at every layer

---

## Page Structure

```
/
├── app/
│   ├── layout.tsx                    # Root layout with providers, header, footer
│   ├── page.tsx                      # Home page - Job listings with filters
│   ├── globals.css                   # Global styles and Tailwind directives
│   │
│   ├── api/
│   │   ├── route.ts                  # GET: Fetch jobs from RemoteOK API
│   │   └── apply/
│   │       └── route.ts              # POST: Submit job application
│   │                                 # GET: View applications (admin)
│   │
│   └── dashboard/                    # (Future) User dashboard for saved jobs
│
├── components/
│   ├── common/
│   │   ├── ErrorMessage.tsx          # Error display component
│   │   ├── FilterPanel.tsx           # Job filtering sidebar
│   │   ├── JobApplicationForm.tsx    # Application form modal
│   │   ├── JobCard.tsx               # Individual job listing card
│   │   ├── JobListings.tsx           # Job grid with modal handler
│   │   └── LoadingSpinner.tsx        # Loading state indicator
│   │
│   └── layouts/
│       ├── Footer.tsx                # Site footer
│       ├── Header.tsx                # Site header with navigation
│       └── SideBar.tsx               # (Future) Navigation sidebar
│
├── context/
│   └── JobContext.tsx                # Global state management (jobs, filters, loading)
│
├── interfaces/
│   └── index.ts                      # TypeScript interfaces and types
│
├── lib/
│   └── api.ts                        # API functions (fetchJobs, submitApplication)
│
├── constants/
│   └── index.ts                      # App constants (categories, locations, mock data)
│
└── public/                           # Static assets
```

---

## API Routes

### **GET `/api`** - Fetch Jobs

**Query Parameters:**
- `q` (query) - Search keyword
- `l` (location) - Location filter
- `experienceLevel` - Entry-Level/Mid-Level/Senior/Lead
- `category` - Job category
- `jobType` - Full-time/Part-time/Contract/Internship
- `remote` - Boolean for remote only
- `page` - Pagination offset

**Response:**
```json
{
  "data": [...],
  "totalResults": 150,
  "page": 0,
  "query": {...}
}
```

### **POST `/api/apply`** - Submit Application

**Request Body:**
```json
{
  "jobId": "string",
  "applicantName": "string",
  "email": "string",
  "phone": "string",
  "coverLetter": "string",
  "linkedIn": "string (optional)",
  "portfolio": "string (optional)",
  "yearsOfExperience": 0
}
```

**Response:**
```json
{
  "success": true,
  "message": "Application submitted successfully",
  "data": {
    "applicationId": "app-xxx",
    "submittedAt": "2025-12-07T..."
  }
}
```

---

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm, yarn, pnpm, or bun

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Favouridowu02/alx-project-nexus.git
cd alx-project-nexus/jobboard
```

2. Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
```

3. Create `.env` file (optional, uses RemoteOK public API):
```env
# No API key required for RemoteOK
```

4. Run the development server:
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

---

## Responsive Breakpoints

- **Mobile** (< 640px): Single column, collapsible filters
- **Tablet** (640px - 1024px): 2-column job grid
- **Desktop** (1024px+): Sidebar + 2-3 column job grid
- **Large Desktop** (1536px+): Sidebar + 3 column job grid

---

## Component Hierarchy

```
App (layout.tsx)
└── JobProvider (context)
    ├── Header
    ├── Home Page
    │   ├── Hero Section
    │   ├── Jobs Section
    │   │   ├── FilterPanel
    │   │   │   ├── Search Input
    │   │   │   ├── Category Select
    │   │   │   ├── Location Select
    │   │   │   ├── Experience Select
    │   │   │   ├── Job Type Select
    │   │   │   └── Remote Checkbox
    │   │   │
    │   │   └── JobListings
    │   │       ├── LoadingSpinner (conditional)
    │   │       ├── ErrorMessage (conditional)
    │   │       ├── Empty State (conditional)
    │   │       ├── JobCard[] (grid)
    │   │       └── Application Modal
    │   │           └── JobApplicationForm
    │   │
    │   └── CTA Section
    └── Footer
```

---

## Deployment Architecture

**Production:** Vercel/Netlify with serverless API routes  
**Development:** Local Next.js dev server with hot module replacement  
**API:** RemoteOK public API (no authentication required)  
**State Management:** React Context API for global state  
**Styling:** Tailwind CSS for utility-first styling

---

## Deploy on Vercel

The easiest way to deploy this app is using [Vercel](https://vercel.com):

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Favouridowu02/alx-project-nexus)

1. Push your code to GitHub
2. Import project to Vercel
3. Deploy (no environment variables needed)
4. Your app is live! 🎉

---

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [RemoteOK API](https://remoteok.com/api)

---

## License

This project is part of the ALX Project Nexus initiative.

## Author

**Favour Idowu**  
GitHub: [@Favouridowu02](https://github.com/Favouridowu02)
