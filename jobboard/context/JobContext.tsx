'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import {
  Job,
  JobContextType,
  FilterState,
  JobApplication,
} from '@/interfaces';
import { DEFAULT_FILTERS, ERROR_MESSAGES } from '@/constants';
import { fetchJobs, submitJobApplication, handleApiError } from '@/lib/api';

const JobContext = createContext<JobContextType | undefined>(undefined);

/**
 * JobProvider Component
 * Manages global state for jobs, filtering, and applications
 */
export const JobProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [filteredJobs, setFilteredJobs] = useState<Job[]>([]);
  const [filters, setFilters] = useState<FilterState>(DEFAULT_FILTERS);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fetches jobs with real-time filters
   */
  const loadJobs = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Build filter object for API
      const apiFilters = {
        experienceLevel: filters.experienceLevel,
        category: filters.category,
        jobType: filters.jobType,
        remoteOnly: filters.remoteOnly,
      };
      
      const jobData = await fetchJobs(
        filters.searchQuery || 'software developer',
        filters.location || 'remote',
        apiFilters
      );
      
      setJobs(jobData);
      setFilteredJobs(jobData);
    } catch (err) {
      const apiError = handleApiError(err);
      setError(apiError.message || ERROR_MESSAGES.FETCH_FAILED);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  /**
   * Load jobs on mount and when filters change (with debouncing for search)
   */
  useEffect(() => {
    // Debounce search queries to avoid too many API calls
    const debounceTimer = setTimeout(() => {
      loadJobs();
    }, 300); // 300ms delay for search input

    return () => clearTimeout(debounceTimer);
  }, [loadJobs]);

  /**
   * Updates a specific filter
   */
  const updateFilter = useCallback(
    (filterName: keyof FilterState, value: string | boolean) => {
      setFilters((prev) => ({
        ...prev,
        [filterName]: value,
      }));
    },
    []
  );

  /**
   * Resets all filters to default values
   */
  const resetFilters = useCallback(() => {
    setFilters(DEFAULT_FILTERS);
  }, []);

  /**
   * Handles job application submission with real-time API
   */
  const applyForJob = useCallback(async (application: JobApplication): Promise<boolean> => {
    try {
      const result = await submitJobApplication(application);
      
      if (result.success) {
        console.log('Application submitted successfully:', result.applicationId);
        return true;
      } else {
        console.error('Application submission failed:', result.message);
        return false;
      }
    } catch (err) {
      const apiError = handleApiError(err);
      console.error('Application submission error:', apiError);
      return false;
    }
  }, []);

  const value: JobContextType = {
    jobs,
    filteredJobs,
    filters,
    loading,
    error,
    updateFilter,
    resetFilters,
    applyForJob,
  };

  return <JobContext.Provider value={value}>{children}</JobContext.Provider>;
};

/**
 * Custom hook to use JobContext
 */
export const useJobs = (): JobContextType => {
  const context = useContext(JobContext);
  if (!context) {
    throw new Error('useJobs must be used within a JobProvider');
  }
  return context;
};
