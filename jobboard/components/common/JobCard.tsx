import React from 'react';
import { Job } from '@/interfaces';

interface JobCardProps {
  job: Job;
  onApply: (jobId: string) => void;
}

/**
 * JobCard Component
 * Displays job information in a card format with accessibility features and responsive design
 */
export const JobCard: React.FC<JobCardProps> = ({ job, onApply }) => {
  const formatSalary = () => {
    if (!job.salary) return null;
    
    const { min, max, currency } = job.salary;
    
    // Check if it's hourly rate (for Contract/Internship positions)
    if (job.type === 'Contract' || job.type === 'Internship') {
      return `$${min}-$${max}/${currency === 'USD' ? 'hr' : currency}`;
    }
    
    return `$${min.toLocaleString()}-$${max.toLocaleString()}/${currency}`;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return date.toLocaleDateString();
  };

  return (
    <article
      className="bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-300 p-4 sm:p-6 border border-gray-200 flex flex-col h-full"
      aria-label={`Job posting for ${job.title} at ${job.company}`}
    >
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-3 mb-4">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg sm:text-xl font-bold text-gray-900 mb-2 wrap-break-word">
            {job.title}
          </h3>
          <p className="text-base sm:text-lg text-gray-700 font-medium truncate">{job.company}</p>
        </div>
        {job.remote && (
          <span
            className="px-3 py-1 bg-green-100 text-green-800 text-xs sm:text-sm font-semibold rounded-full self-start whitespace-nowrap"
            aria-label="Remote position"
          >
            Remote
          </span>
        )}
      </div>

      {/* Job Details */}
      <div className="space-y-2 mb-4 grow">
        <div className="flex items-center text-gray-600 text-sm sm:text-base">
          <svg
            className="w-4 h-4 sm:w-5 sm:h-5 mr-2 shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
          <span className="truncate">{job.location}</span>
        </div>

        <div className="flex items-center text-gray-600 text-sm sm:text-base">
          <svg
            className="w-4 h-4 sm:w-5 sm:h-5 mr-2 shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
            />
          </svg>
          <span>{job.type}</span>
        </div>

        {job.salary && (
          <div className="flex items-center text-gray-600 font-semibold text-sm sm:text-base">
            <svg
              className="w-4 h-4 sm:w-5 sm:h-5 mr-2 shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span className="truncate">{formatSalary()}</span>
          </div>
        )}
      </div>

      {/* Tags */}
      <div className="flex flex-wrap gap-2 mb-4">
        <span className="px-2 sm:px-3 py-1 bg-blue-100 text-blue-800 text-xs sm:text-sm rounded-full whitespace-nowrap">
          {job.category}
        </span>
        <span className="px-2 sm:px-3 py-1 bg-purple-100 text-purple-800 text-xs sm:text-sm rounded-full whitespace-nowrap">
          {job.experienceLevel}
        </span>
      </div>

      {/* Description */}
      <p className="text-gray-600 text-sm sm:text-base mb-4 line-clamp-3">{job.description}</p>

      {/* Footer */}
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 pt-4 border-t border-gray-200 mt-auto">
        <span className="text-xs sm:text-sm text-gray-500">
          Posted {formatDate(job.postedDate)}
        </span>
        <button
          onClick={() => onApply(job.id)}
          className="w-full sm:w-auto px-4 sm:px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 active:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors text-sm sm:text-base"
          aria-label={`Apply for ${job.title} position at ${job.company}`}
        >
          Apply Now
        </button>
      </div>
    </article>
  );
};

