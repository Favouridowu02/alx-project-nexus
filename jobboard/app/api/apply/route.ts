import { NextRequest, NextResponse } from 'next/server';
import { JobApplication } from '@/interfaces';

// In-memory storage for demo purposes (in production, use a database)
const applications: Array<JobApplication & { id: string; submittedAt: string }> = [];

/**
 * Validate email format
 */
function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate phone format
 */
function isValidPhone(phone: string): boolean {
  const phoneRegex = /^[\d\s\-\+\(\)]+$/;
  return phoneRegex.test(phone) && phone.replace(/\D/g, '').length >= 10;
}

/**
 * Validate job application data
 */
function validateApplication(data: any): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (!data.jobId || typeof data.jobId !== 'string') {
    errors.push('Job ID is required');
  }

  if (!data.applicantName || typeof data.applicantName !== 'string' || data.applicantName.trim().length < 2) {
    errors.push('Applicant name must be at least 2 characters');
  }

  if (!data.email || !isValidEmail(data.email)) {
    errors.push('Valid email address is required');
  }

  if (!data.phone || !isValidPhone(data.phone)) {
    errors.push('Valid phone number is required (minimum 10 digits)');
  }

  if (!data.coverLetter || typeof data.coverLetter !== 'string' || data.coverLetter.trim().length < 50) {
    errors.push('Cover letter must be at least 50 characters');
  }

  if (data.yearsOfExperience !== undefined && (typeof data.yearsOfExperience !== 'number' || data.yearsOfExperience < 0)) {
    errors.push('Years of experience must be a non-negative number');
  }

  if (data.linkedIn && typeof data.linkedIn === 'string' && data.linkedIn.trim() !== '') {
    if (!data.linkedIn.includes('linkedin.com')) {
      errors.push('LinkedIn URL must be a valid LinkedIn profile URL');
    }
  }

  if (data.portfolio && typeof data.portfolio === 'string' && data.portfolio.trim() !== '') {
    try {
      new URL(data.portfolio);
    } catch {
      errors.push('Portfolio must be a valid URL');
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * POST /api/apply - Submit a job application
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Validate the application data
    const validation = validateApplication(body);
    
    if (!validation.valid) {
      return NextResponse.json(
        {
          success: false,
          message: 'Validation failed',
          errors: validation.errors,
          status: 400,
        },
        { status: 400 }
      );
    }

    // Create application object
    const application: JobApplication & { id: string; submittedAt: string } = {
      id: `app-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      jobId: body.jobId,
      applicantName: body.applicantName.trim(),
      email: body.email.trim().toLowerCase(),
      phone: body.phone.trim(),
      coverLetter: body.coverLetter.trim(),
      linkedIn: body.linkedIn?.trim() || undefined,
      portfolio: body.portfolio?.trim() || undefined,
      yearsOfExperience: body.yearsOfExperience || 0,
      submittedAt: new Date().toISOString(),
    };

    // Store the application (in production, save to database)
    applications.push(application);
    
    // Log for debugging
    console.log('New application received:', {
      id: application.id,
      jobId: application.jobId,
      applicant: application.applicantName,
      email: application.email,
    });

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 500));

    return NextResponse.json(
      {
        success: true,
        message: 'Application submitted successfully',
        data: {
          applicationId: application.id,
          submittedAt: application.submittedAt,
          jobId: application.jobId,
        },
        status: 201,
      },
      { status: 201 }
    );

  } catch (error) {
    console.error('Application submission error:', error);
    
    if (error instanceof SyntaxError) {
      return NextResponse.json(
        {
          success: false,
          message: 'Invalid JSON data',
          status: 400,
        },
        { status: 400 }
      );
    }

    return NextResponse.json(
      {
        success: false,
        message: error instanceof Error ? error.message : 'Failed to submit application',
        status: 500,
        error: process.env.NODE_ENV === 'development' ? error : undefined,
      },
      { status: 500 }
    );
  }
}

/**
 * GET /api/apply - Get application statistics (for admin/debugging)
 */
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const jobId = searchParams.get('jobId');

  if (jobId) {
    // Get applications for a specific job
    const jobApplications = applications.filter(app => app.jobId === jobId);
    return NextResponse.json({
      jobId,
      count: jobApplications.length,
      applications: jobApplications.map(app => ({
        id: app.id,
        applicantName: app.applicantName,
        email: app.email,
        submittedAt: app.submittedAt,
      })),
    });
  }

  // Get all applications summary
  return NextResponse.json({
    totalApplications: applications.length,
    recentApplications: applications
      .slice(-10)
      .reverse()
      .map(app => ({
        id: app.id,
        jobId: app.jobId,
        applicantName: app.applicantName,
        email: app.email,
        submittedAt: app.submittedAt,
      })),
  });
}
