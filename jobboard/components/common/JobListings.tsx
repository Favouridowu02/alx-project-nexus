'use client';

import React, { useState } from 'react';
import { useJobs } from '@/context/JobContext';
import { Job } from '@/interfaces';
import { JobCard } from './JobCard';
import { LoadingSpinner } from './LoadingSpinner';
import { ErrorMessage } from './ErrorMessage';
import { JobApplicationForm } from './JobApplicationForm';

/**
 * JobListings Component
 * Displays a grid of job cards with loading and error states
 */
export const JobListings: React.FC = () => {
  const { filteredJobs, loading, error } = useJobs();
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [showApplicationForm, setShowApplicationForm] = useState(false);

  const handleApply = (jobId: string) => {
    const job = filteredJobs.find(j => j.id === jobId);
    if (job) {
      setSelectedJob(job);
      setShowApplicationForm(true);
    }
  };

  const handleCloseForm = () => {
    setShowApplicationForm(false);
    setSelectedJob(null);
  };

  // Loading state
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <LoadingSpinner size="large" />
        <p className="mt-4 text-gray-600 text-lg">Loading job opportunities...</p>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="py-10">
        <ErrorMessage message={error} />
      </div>
    );
  }

  // Empty state
  if (filteredJobs.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 px-4">
        <svg
          className="w-24 h-24 text-gray-300 mb-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">No jobs found</h3>
        <p className="text-gray-600 text-center max-w-md">
          We couldn&apos;t find any jobs matching your criteria. Try adjusting your filters or search terms.
        </p>
      </div>
    );
  }

  return (
    <>
      <div className="mb-6">
        <p className="text-gray-700" role="status" aria-live="polite">
          Showing <span className="font-semibold">{filteredJobs.length}</span> job{filteredJobs.length !== 1 ? 's' : ''}
        </p>
      </div>

      {/* Job Grid */}
      <div
        className="grid gap-6 grid-cols-1 lg:grid-cols-2 xl:grid-cols-2 2xl:grid-cols-3"
        role="list"
        aria-label="Job listings"
      >
        {filteredJobs.map((job) => (
          <JobCard key={job.id} job={job} onApply={handleApply} />
        ))}
      </div>

      {/* Application Form Modal */}
      {showApplicationForm && selectedJob && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto"
          role="dialog"
          aria-modal="true"
          aria-labelledby="application-form-title"
          onClick={(e) => {
            if (e.target === e.currentTarget) {
              handleCloseForm();
            }
          }}
        >
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full my-8">
            <div className="flex justify-between items-center p-6 border-b border-gray-200">
              <h2 id="application-form-title" className="text-2xl font-bold text-gray-900">
                Apply for Position
              </h2>
              <button
                onClick={handleCloseForm}
                className="text-gray-400 hover:text-gray-600 transition-colors"
                aria-label="Close application form"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="p-6">
              <JobApplicationForm
                job={selectedJob}
                onClose={handleCloseForm}
                onSuccess={handleCloseForm}
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
};
