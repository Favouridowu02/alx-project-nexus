'use client';

import React from 'react';
import { FilterPanel } from '@/components/common/FilterPanel';
import { JobListings } from '@/components/common/JobListings';

/**
 * Home Page Component
 * Main landing page with job search and filtering functionality
 */
export default function Home() {
  return (
    <div className="min-h-screen bg-linear-to-br from-gray-50 to-gray-100">
      {/* Hero Section */}
      <section className="bg-linear-to-r from-blue-600 to-blue-700 text-white py-16 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4 tracking-tight">
              Find Your Dream Job
            </h1>
            <p className="text-xl md:text-2xl text-blue-100 mb-8 max-w-3xl mx-auto">
              Explore thousands of job opportunities with all the information you need. 
              It&apos;s your future. Come find it.
            </p>
            
            {/* Key Features */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12 max-w-4xl mx-auto">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 text-left">
                <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">Smart Search</h3>
                <p className="text-blue-100 text-sm">
                  Find jobs by title, company, or keywords with advanced filtering
                </p>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 text-left">
                <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">Advanced Filters</h3>
                <p className="text-blue-100 text-sm">
                  Filter by category, location, experience level, and more
                </p>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 text-left">
                <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">Quick Apply</h3>
                <p className="text-blue-100 text-sm">
                  Apply to jobs instantly with our streamlined application process
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content - Jobs Section */}
      <section className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar - Filters */}
          <aside className="lg:col-span-1">
            <FilterPanel />
          </aside>

          {/* Main Content - Job Listings */}
          <main className="lg:col-span-3">
            <JobListings />
          </main>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="bg-white py-16 px-4 mt-12">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Ready to Take the Next Step?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Join thousands of professionals who found their dream job through our platform
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
              Browse All Jobs
            </button>
            <button className="px-8 py-3 bg-white text-blue-600 border-2 border-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
              Post a Job
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
