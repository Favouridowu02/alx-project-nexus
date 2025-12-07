'use client';

import React, { useState } from 'react';
import { useJobs } from '@/context/JobContext';
import {
  JOB_CATEGORIES,
  LOCATIONS,
  EXPERIENCE_LEVELS,
  JOB_TYPES,
} from '@/constants';

/**
 * FilterPanel Component
 * Provides accessible filtering options for job listings with mobile responsiveness
 */
export const FilterPanel: React.FC = () => {
  const { filters, updateFilter, resetFilters, filteredJobs } = useJobs();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Mobile Filter Toggle Button */}
      <div className="lg:hidden mb-4">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-between px-4 py-3 bg-white rounded-lg shadow-md border border-gray-200 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          aria-expanded={isOpen}
          aria-controls="filter-panel"
        >
          <span className="flex items-center text-gray-900 font-semibold">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            Filters ({filteredJobs.length} jobs)
          </span>
          <svg
            className={`w-5 h-5 transform transition-transform ${isOpen ? 'rotate-180' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

      {/* Filter Panel */}
      <aside
        id="filter-panel"
        className={`
          bg-white rounded-lg shadow-md p-6 
          ${isOpen ? 'block' : 'hidden'} lg:block lg:sticky lg:top-4
          transition-all duration-300
        `}
        aria-label="Job filters"
      >
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-gray-900">Filters</h2>
          <button
            onClick={resetFilters}
            className="text-sm text-blue-600 hover:text-blue-700 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1"
            aria-label="Reset all filters"
          >
            Reset All
          </button>
        </div>

        {/* Search Input */}
        <div className="mb-6">
          <label htmlFor="search" className="block text-sm font-semibold text-gray-700 mb-2">
            Search
          </label>
          <input
            type="text"
            id="search"
            value={filters.searchQuery}
            onChange={(e) => updateFilter('searchQuery', e.target.value)}
            placeholder="Job title, company, keyword..."
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            aria-describedby="search-description"
          />
          <p id="search-description" className="sr-only">
            Search for jobs by title, company name, or keywords
          </p>
        </div>

        {/* Category Filter */}
        <div className="mb-6">
          <label htmlFor="category" className="block text-sm font-semibold text-gray-700 mb-2">
            Category
          </label>
          <select
            id="category"
            value={filters.category}
            onChange={(e) => updateFilter('category', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white cursor-pointer transition-colors"
            aria-label="Filter by job category"
          >
            {JOB_CATEGORIES.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </div>

        {/* Location Filter */}
        <div className="mb-6">
          <label htmlFor="location" className="block text-sm font-semibold text-gray-700 mb-2">
            Location
          </label>
          <select
            id="location"
            value={filters.location}
            onChange={(e) => updateFilter('location', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white cursor-pointer transition-colors"
            aria-label="Filter by location"
          >
            {LOCATIONS.map((location) => (
              <option key={location} value={location}>
                {location}
              </option>
            ))}
          </select>
        </div>

        {/* Experience Level Filter */}
        <div className="mb-6">
          <label htmlFor="experience" className="block text-sm font-semibold text-gray-700 mb-2">
            Experience Level
          </label>
          <select
            id="experience"
            value={filters.experienceLevel}
            onChange={(e) => updateFilter('experienceLevel', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white cursor-pointer transition-colors"
            aria-label="Filter by experience level"
          >
            <option value="">All Levels</option>
            {EXPERIENCE_LEVELS.map((level) => (
              <option key={level} value={level}>
                {level}
              </option>
            ))}
          </select>
        </div>

        {/* Job Type Filter */}
        <div className="mb-6">
          <label htmlFor="jobType" className="block text-sm font-semibold text-gray-700 mb-2">
            Job Type
          </label>
          <select
            id="jobType"
            value={filters.jobType}
            onChange={(e) => updateFilter('jobType', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white cursor-pointer transition-colors"
            aria-label="Filter by job type"
          >
            <option value="">All Types</option>
            {JOB_TYPES.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>

        {/* Remote Only Checkbox */}
        <div className="mb-6">
          <label className="flex items-center cursor-pointer group">
            <input
              type="checkbox"
              checked={filters.remoteOnly}
              onChange={(e) => updateFilter('remoteOnly', e.target.checked)}
              className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500 cursor-pointer"
              aria-label="Show only remote positions"
            />
            <span className="ml-2 text-sm font-medium text-gray-700 group-hover:text-gray-900">
              Remote Only
            </span>
          </label>
        </div>

        {/* Results Count */}
        <div className="pt-4 border-t border-gray-200">
          <p className="text-sm text-gray-600" aria-live="polite" aria-atomic="true">
            Showing <span className="font-semibold">{filteredJobs.length}</span>{' '}
            {filteredJobs.length === 1 ? 'job' : 'jobs'}
          </p>
        </div>

        {/* Mobile Close Button */}
        <div className="lg:hidden mt-6">
          <button
            onClick={() => setIsOpen(false)}
            className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 font-semibold transition-colors"
          >
            Show {filteredJobs.length} Jobs
          </button>
        </div>
      </aside>
    </>
  );
};

