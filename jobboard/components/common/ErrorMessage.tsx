import React from 'react';

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

/**
 * ErrorMessage Component
 * Displays accessible error messages with optional retry functionality
 */
export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onRetry }) => {
  return (
    <div
      className="flex flex-col items-center justify-center p-8 bg-red-50 border border-red-200 rounded-lg my-4"
      role="alert"
      aria-live="assertive"
    >
      <svg
        className="w-12 h-12 text-red-500 mb-4"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <h3 className="text-lg font-semibold text-red-800 mb-2">Error</h3>
      <p className="text-red-700 text-center mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors"
          aria-label="Retry loading"
        >
          Try Again
        </button>
      )}
    </div>
  );
};
