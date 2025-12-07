// Job-related interfaces
export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  category: string;
  experienceLevel: ExperienceLevel;
  type: JobType;
  salary?: {
    min: number;
    max: number;
    currency: string;
  };
  description: string;
  requirements: string[];
  responsibilities: string[];
  benefits?: string[];
  postedDate: string;
  applicationDeadline?: string;
  remote: boolean;
}

export type ExperienceLevel = 'Entry-Level' | 'Mid-Level' | 'Senior' | 'Lead';
export type JobType = 'Full-time' | 'Part-time' | 'Contract' | 'Internship';

// Filter interfaces
export interface FilterOptions {
  categories: string[];
  locations: string[];
  experienceLevels: ExperienceLevel[];
  jobTypes: JobType[];
  searchQuery: string;
  remoteOnly: boolean;
}

export interface FilterState {
  category: string;
  location: string;
  experienceLevel: string;
  jobType: string;
  searchQuery: string;
  remoteOnly: boolean;
}

// Application form interfaces
export interface JobApplication {
  jobId: string;
  applicantName: string;
  email: string;
  phone: string;
  coverLetter: string;
  resume?: File;
  linkedIn?: string;
  portfolio?: string;
  yearsOfExperience: number;
}

export interface FormErrors {
  [key: string]: string;
}

// Context API interfaces
export interface JobContextType {
  jobs: Job[];
  filteredJobs: Job[];
  filters: FilterState;
  loading: boolean;
  error: string | null;
  updateFilter: (filterName: keyof FilterState, value: string | boolean) => void;
  resetFilters: () => void;
  applyForJob: (application: JobApplication) => Promise<boolean>;
}

// API Response interfaces
export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

export interface ApiError {
  message: string;
  code?: string;
  details?: unknown;
}
