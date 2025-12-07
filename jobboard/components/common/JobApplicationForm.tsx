'use client';

import React, { useState, FormEvent } from 'react';
import { JobApplication, FormErrors, Job } from '@/interfaces';
import { VALIDATION_MESSAGES } from '@/constants';
import { useJobs } from '@/context/JobContext';

interface JobApplicationFormProps {
  job: Job;
  onClose: () => void;
  onSuccess: () => void;
}

/**
 * JobApplicationForm Component
 * Accessible form for job applications with validation
 */
export const JobApplicationForm: React.FC<JobApplicationFormProps> = ({
  job,
  onClose,
  onSuccess,
}) => {
  const { applyForJob } = useJobs();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});
  const [formData, setFormData] = useState({
    applicantName: '',
    email: '',
    phone: '',
    coverLetter: '',
    linkedIn: '',
    portfolio: '',
    yearsOfExperience: 0,
  });

  /**
   * Validates form fields
   */
  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Name validation
    if (!formData.applicantName.trim()) {
      newErrors.applicantName = VALIDATION_MESSAGES.REQUIRED;
    } else if (formData.applicantName.length < 2) {
      newErrors.applicantName = VALIDATION_MESSAGES.MIN_LENGTH(2);
    }

    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = VALIDATION_MESSAGES.REQUIRED;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = VALIDATION_MESSAGES.INVALID_EMAIL;
    }

    // Phone validation
    if (!formData.phone.trim()) {
      newErrors.phone = VALIDATION_MESSAGES.REQUIRED;
    } else if (!/^[\d\s()+-]+$/.test(formData.phone) || formData.phone.length < 10) {
      newErrors.phone = VALIDATION_MESSAGES.INVALID_PHONE;
    }

    // Cover letter validation
    if (!formData.coverLetter.trim()) {
      newErrors.coverLetter = VALIDATION_MESSAGES.REQUIRED;
    } else if (formData.coverLetter.length < 50) {
      newErrors.coverLetter = VALIDATION_MESSAGES.MIN_LENGTH(50);
    } else if (formData.coverLetter.length > 1000) {
      newErrors.coverLetter = VALIDATION_MESSAGES.MAX_LENGTH(1000);
    }

    // Years of experience validation
    if (formData.yearsOfExperience < 0) {
      newErrors.yearsOfExperience = VALIDATION_MESSAGES.MIN_VALUE(0);
    }

    // LinkedIn validation (if provided)
    if (formData.linkedIn && !/^https?:\/\/(www\.)?linkedin\.com/.test(formData.linkedIn)) {
      newErrors.linkedIn = 'Please enter a valid LinkedIn URL';
    }

    // Portfolio validation (if provided)
    if (formData.portfolio && !/^https?:\/\/.+/.test(formData.portfolio)) {
      newErrors.portfolio = 'Please enter a valid URL';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * Handles form submission
   */
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const application: JobApplication = {
        jobId: job.id,
        ...formData,
      };

      const success = await applyForJob(application);

      if (success) {
        onSuccess();
      } else {
        alert('Failed to submit application. Please try again.');
      }
    } catch (error) {
      console.error('Application error:', error);
      alert('An error occurred. Please try again later.');
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * Handles input change
   */
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      role="dialog"
      aria-modal="true"
      aria-labelledby="form-title"
    >
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <div>
            <h2 id="form-title" className="text-2xl font-bold text-gray-900">
              Apply for {job.title}
            </h2>
            <p className="text-sm text-gray-600 mt-1">{job.company}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-full p-1"
            aria-label="Close application form"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="px-6 py-4" noValidate>
          {/* Full Name */}
          <div className="mb-4">
            <label htmlFor="applicantName" className="block text-sm font-semibold text-gray-700 mb-2">
              Full Name <span className="text-red-500" aria-label="required">*</span>
            </label>
            <input
              type="text"
              id="applicantName"
              name="applicantName"
              value={formData.applicantName}
              onChange={handleChange}
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.applicantName ? 'border-red-500' : 'border-gray-300'
              }`}
              aria-required="true"
              aria-invalid={!!errors.applicantName}
              aria-describedby={errors.applicantName ? 'name-error' : undefined}
            />
            {errors.applicantName && (
              <p id="name-error" className="text-red-500 text-sm mt-1" role="alert">
                {errors.applicantName}
              </p>
            )}
          </div>

          {/* Email */}
          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-semibold text-gray-700 mb-2">
              Email Address <span className="text-red-500" aria-label="required">*</span>
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.email ? 'border-red-500' : 'border-gray-300'
              }`}
              aria-required="true"
              aria-invalid={!!errors.email}
              aria-describedby={errors.email ? 'email-error' : undefined}
            />
            {errors.email && (
              <p id="email-error" className="text-red-500 text-sm mt-1" role="alert">
                {errors.email}
              </p>
            )}
          </div>

          {/* Phone */}
          <div className="mb-4">
            <label htmlFor="phone" className="block text-sm font-semibold text-gray-700 mb-2">
              Phone Number <span className="text-red-500" aria-label="required">*</span>
            </label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="(123) 456-7890"
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.phone ? 'border-red-500' : 'border-gray-300'
              }`}
              aria-required="true"
              aria-invalid={!!errors.phone}
              aria-describedby={errors.phone ? 'phone-error' : undefined}
            />
            {errors.phone && (
              <p id="phone-error" className="text-red-500 text-sm mt-1" role="alert">
                {errors.phone}
              </p>
            )}
          </div>

          {/* Years of Experience */}
          <div className="mb-4">
            <label htmlFor="yearsOfExperience" className="block text-sm font-semibold text-gray-700 mb-2">
              Years of Experience <span className="text-red-500" aria-label="required">*</span>
            </label>
            <input
              type="number"
              id="yearsOfExperience"
              name="yearsOfExperience"
              value={formData.yearsOfExperience}
              onChange={handleChange}
              min="0"
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.yearsOfExperience ? 'border-red-500' : 'border-gray-300'
              }`}
              aria-required="true"
              aria-invalid={!!errors.yearsOfExperience}
              aria-describedby={errors.yearsOfExperience ? 'experience-error' : undefined}
            />
            {errors.yearsOfExperience && (
              <p id="experience-error" className="text-red-500 text-sm mt-1" role="alert">
                {errors.yearsOfExperience}
              </p>
            )}
          </div>

          {/* LinkedIn (Optional) */}
          <div className="mb-4">
            <label htmlFor="linkedIn" className="block text-sm font-semibold text-gray-700 mb-2">
              LinkedIn Profile (Optional)
            </label>
            <input
              type="url"
              id="linkedIn"
              name="linkedIn"
              value={formData.linkedIn}
              onChange={handleChange}
              placeholder="https://www.linkedin.com/in/yourprofile"
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.linkedIn ? 'border-red-500' : 'border-gray-300'
              }`}
              aria-invalid={!!errors.linkedIn}
              aria-describedby={errors.linkedIn ? 'linkedin-error' : undefined}
            />
            {errors.linkedIn && (
              <p id="linkedin-error" className="text-red-500 text-sm mt-1" role="alert">
                {errors.linkedIn}
              </p>
            )}
          </div>

          {/* Portfolio (Optional) */}
          <div className="mb-4">
            <label htmlFor="portfolio" className="block text-sm font-semibold text-gray-700 mb-2">
              Portfolio Website (Optional)
            </label>
            <input
              type="url"
              id="portfolio"
              name="portfolio"
              value={formData.portfolio}
              onChange={handleChange}
              placeholder="https://yourportfolio.com"
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.portfolio ? 'border-red-500' : 'border-gray-300'
              }`}
              aria-invalid={!!errors.portfolio}
              aria-describedby={errors.portfolio ? 'portfolio-error' : undefined}
            />
            {errors.portfolio && (
              <p id="portfolio-error" className="text-red-500 text-sm mt-1" role="alert">
                {errors.portfolio}
              </p>
            )}
          </div>

          {/* Cover Letter */}
          <div className="mb-6">
            <label htmlFor="coverLetter" className="block text-sm font-semibold text-gray-700 mb-2">
              Cover Letter <span className="text-red-500" aria-label="required">*</span>
            </label>
            <textarea
              id="coverLetter"
              name="coverLetter"
              value={formData.coverLetter}
              onChange={handleChange}
              rows={6}
              placeholder="Tell us why you're a great fit for this position..."
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none ${
                errors.coverLetter ? 'border-red-500' : 'border-gray-300'
              }`}
              aria-required="true"
              aria-invalid={!!errors.coverLetter}
              aria-describedby={errors.coverLetter ? 'cover-letter-error' : 'cover-letter-help'}
            />
            <p id="cover-letter-help" className="text-xs text-gray-500 mt-1">
              {formData.coverLetter.length}/1000 characters (minimum 50)
            </p>
            {errors.coverLetter && (
              <p id="cover-letter-error" className="text-red-500 text-sm mt-1" role="alert">
                {errors.coverLetter}
              </p>
            )}
          </div>

          {/* Form Actions */}
          <div className="flex gap-4 justify-end sticky bottom-0 bg-white border-t border-gray-200 pt-4 -mx-6 px-6 pb-4">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="px-6 py-2 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              aria-busy={isSubmitting}
            >
              {isSubmitting ? 'Submitting...' : 'Submit Application'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
