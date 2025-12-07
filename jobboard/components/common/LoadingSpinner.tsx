import React from 'react';

interface LoadingSpinnerProps {
  message?: string;
  size?: 'small' | 'medium' | 'large';
}

/**
 * LoadingSpinner Component
 * Displays an accessible loading indicator
 */
export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message = 'Loading...',
  size = 'medium',
}) => {
  const sizeClasses = {
    small: 'w-6 h-6 border-2',
    medium: 'w-12 h-12 border-4',
    large: 'w-16 h-16 border-4',
  };

  return (
    <div
      className="flex flex-col items-center justify-center p-8"
      role="status"
      aria-live="polite"
      aria-busy="true"
    >
      <div
        className={`${sizeClasses[size]} border-blue-200 border-t-blue-600 rounded-full animate-spin`}
        aria-hidden="true"
      ></div>
      <p className="mt-4 text-gray-600 text-sm md:text-base">{message}</p>
      <span className="sr-only">{message}</span>
    </div>
  );
};
