import { Job, JobApplication, ApiResponse, ApiError } from '@/interfaces';
import { API_CONFIG, MOCK_JOBS } from '@/constants';

/**
 * Simulates network delay for realistic API behavior
 */
const simulateDelay = (ms: number = 1000): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

/**
 * Fetches job listings from the API with real-time search filters
 */
export const fetchJobs = async (
  query: string = 'software developer',
  location: string = 'remote',
  filters?: {
    experienceLevel?: string;
    category?: string;
    jobType?: string;
    remoteOnly?: boolean;
  }
): Promise<Job[]> => {
  try {
    // Build query parameters
    const params = new URLSearchParams({
      q: query,
      l: location,
    });

    // Add optional filters
    if (filters?.experienceLevel && filters.experienceLevel !== '' && filters.experienceLevel !== 'All Levels') {
      params.append('experienceLevel', filters.experienceLevel);
    }
    if (filters?.category && filters.category !== 'All Categories') {
      params.append('category', filters.category);
    }
    if (filters?.jobType && filters.jobType !== '' && filters.jobType !== 'All Types') {
      params.append('jobType', filters.jobType);
    }
    if (filters?.remoteOnly) {
      params.append('remote', 'true');
    }

    // Fetch from our Next.js API route
    const response = await fetch(`/api?${params.toString()}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store', // Ensure fresh data for real-time search
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: ApiResponse<Job[]> & { totalResults?: number } = await response.json();
    
    // If API returns empty results, fall back to mock data
    if (!data.data || data.data.length === 0) {
      console.warn('API returned no results, using mock data');
      return MOCK_JOBS;
    }
    
    return data.data;
  } catch (error) {
    // Fall back to mock data if API fails
    console.warn('API unavailable, using mock data:', error);
    return MOCK_JOBS;
  }
};

/**
 * Submits a job application with real-time validation
 */
export const submitJobApplication = async (
  application: JobApplication
): Promise<{ success: boolean; message?: string; applicationId?: string }> => {
  try {
    // Submit to our real application API endpoint
    const response = await fetch('/api/apply', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(application),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || `HTTP error! status: ${response.status}`);
    }

    return {
      success: data.success,
      message: data.message,
      applicationId: data.data?.applicationId,
    };
  } catch (error) {
    console.error('Application submission error:', error);
    return {
      success: false,
      message: error instanceof Error ? error.message : 'Failed to submit application',
    };
  }
};

/**
 * Custom error handler for API calls
 */
export const handleApiError = (error: unknown): ApiError => {
  if (error instanceof Error) {
    return {
      message: error.message,
      code: 'API_ERROR',
      details: error,
    };
  }

  return {
    message: 'An unknown error occurred',
    code: 'UNKNOWN_ERROR',
    details: error,
  };
};
