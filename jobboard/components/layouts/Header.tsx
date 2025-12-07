'use client';

import React, { useState } from 'react';
import Link from 'next/link';

/**
 * Header Component
 * Responsive navigation header with accessibility features
 */
export const Header: React.FC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  return (
    <header className="bg-white shadow-md sticky top-0 z-40" role="banner">
      <nav
        className="container mx-auto px-4 py-4"
        aria-label="Main navigation"
      >
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link
            href="/"
            className="flex items-center space-x-2 text-2xl font-bold text-blue-600 hover:text-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
            aria-label="Job Board - Home"
          >
            <svg
              className="w-8 h-8"
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
            <span>JobBoard</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link
              href="/"
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1"
            >
              Home
            </Link>
            <Link
              href="/#jobs"
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1"
            >
              Browse Jobs
            </Link>
            <Link
              href="/#about"
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1"
            >
              About
            </Link>
            <Link
              href="/#contact"
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1"
            >
              Contact
            </Link>
          </div>

          {/* CTA Button */}
          <div className="hidden md:block">
            <Link
              href="/#jobs"
              className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
            >
              Post a Job
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={toggleMobileMenu}
            className="md:hidden text-gray-700 hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded p-2"
            aria-expanded={mobileMenuOpen}
            aria-controls="mobile-menu"
            aria-label="Toggle mobile menu"
          >
            {mobileMenuOpen ? (
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            ) : (
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div
            id="mobile-menu"
            className="md:hidden mt-4 py-4 border-t border-gray-200"
          >
            <div className="flex flex-col space-y-4">
              <Link
                href="/"
                onClick={() => setMobileMenuOpen(false)}
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-2"
              >
                Home
              </Link>
              <Link
                href="/#jobs"
                onClick={() => setMobileMenuOpen(false)}
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-2"
              >
                Browse Jobs
              </Link>
              <Link
                href="/#about"
                onClick={() => setMobileMenuOpen(false)}
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-2"
              >
                About
              </Link>
              <Link
                href="/#contact"
                onClick={() => setMobileMenuOpen(false)}
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-2"
              >
                Contact
              </Link>
              <Link
                href="/#jobs"
                onClick={() => setMobileMenuOpen(false)}
                className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors text-center"
              >
                Post a Job
              </Link>
            </div>
          </div>
        )}
      </nav>
    </header>
  );
};