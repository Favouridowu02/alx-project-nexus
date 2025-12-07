import { NextRequest, NextResponse } from 'next/server';
import { Job } from '@/interfaces';

/**
 * Transform RemoteOK API response to our Job interface
 */
function transformRemoteOKJob(remoteJob: any): Job {
  return {
    id: remoteJob.id || remoteJob.slug || `job-${Date.now()}`,
    title: remoteJob.position || 'Untitled Position',
    company: remoteJob.company || 'Company Confidential',
    location: remoteJob.location || 'Remote',
    category: determineCategory(remoteJob.tags || []),
    experienceLevel: determineExperienceLevel(remoteJob.position || ''),
    type: 'Full-time',
    salary: remoteJob.salary_min && remoteJob.salary_max ? {
      min: remoteJob.salary_min,
      max: remoteJob.salary_max,
      currency: 'USD',
    } : undefined,
    description: remoteJob.description || 'No description available',
    requirements: extractRequirements(remoteJob.description || ''),
    responsibilities: [],
    postedDate: remoteJob.date ? new Date(remoteJob.date * 1000).toISOString() : new Date().toISOString(),
    remote: true, // RemoteOK only has remote jobs
  };
}

/**
 * Determine job category based on tags or title
 */
function determineCategory(tagsOrTitle: string[] | string): string {
  let searchText = '';
  
  if (Array.isArray(tagsOrTitle)) {
    searchText = tagsOrTitle.join(' ').toLowerCase();
  } else {
    searchText = tagsOrTitle.toLowerCase();
  }
  
  if (searchText.includes('dev') || searchText.includes('engineer') || searchText.includes('programmer') || searchText.includes('frontend') || searchText.includes('backend') || searchText.includes('fullstack') || searchText.includes('full stack')) {
    return 'Software Development';
  }
  if (searchText.includes('data') || searchText.includes('analyst') || searchText.includes('scientist') || searchText.includes('ml') || searchText.includes('machine learning')) {
    return 'Data Science';
  }
  if (searchText.includes('design') || searchText.includes('ux') || searchText.includes('ui') || searchText.includes('graphic')) {
    return 'Design';
  }
  if (searchText.includes('market') || searchText.includes('seo') || searchText.includes('growth')) {
    return 'Marketing';
  }
  if (searchText.includes('product') || searchText.includes('pm')) {
    return 'Product Management';
  }
  if (searchText.includes('sales') || searchText.includes('business development')) {
    return 'Sales';
  }
  if (searchText.includes('support') || searchText.includes('customer') || searchText.includes('success')) {
    return 'Customer Support';
  }
  if (searchText.includes('hr') || searchText.includes('human') || searchText.includes('recruiter') || searchText.includes('talent')) {
    return 'Human Resources';
  }
  if (searchText.includes('finance') || searchText.includes('accounting') || searchText.includes('accountant')) {
    return 'Finance';
  }
  if (searchText.includes('devops') || searchText.includes('sre') || searchText.includes('infrastructure')) {
    return 'DevOps';
  }
  if (searchText.includes('qa') || searchText.includes('test') || searchText.includes('quality')) {
    return 'Quality Assurance';
  }
  if (searchText.includes('security') || searchText.includes('cyber')) {
    return 'Security';
  }
  
  return 'Software Development';
}

/**
 * Determine experience level based on title
 */
function determineExperienceLevel(title: string): 'Entry-Level' | 'Mid-Level' | 'Senior' | 'Lead' {
  const lowerTitle = title.toLowerCase();
  
  if (lowerTitle.includes('senior') || lowerTitle.includes('sr.') || lowerTitle.includes('principal')) {
    return 'Senior';
  }
  if (lowerTitle.includes('lead') || lowerTitle.includes('staff') || lowerTitle.includes('chief')) {
    return 'Lead';
  }
  if (lowerTitle.includes('junior') || lowerTitle.includes('jr.') || lowerTitle.includes('entry') || lowerTitle.includes('intern')) {
    return 'Entry-Level';
  }
  
  return 'Mid-Level';
}

/**
 * Extract requirements from job description
 */
function extractRequirements(description: string): string[] {
  const requirements: string[] = [];
  
  // Simple extraction - in a real app, this would be more sophisticated
  if (description) {
    const sentences = description.split(/[.!?]+/).filter(s => s.trim().length > 10);
    requirements.push(...sentences.slice(0, 3).map(s => s.trim()));
  }
  
  if (requirements.length === 0) {
    requirements.push('Experience in relevant field');
    requirements.push('Strong communication skills');
    requirements.push('Ability to work in a team environment');
  }
  
  return requirements;
}

/**
 * GET /api/jobs - Fetch job listings from RemoteOK API with real-time search
 * Supports dynamic filtering by query, location, experience level, category, and job type
 */
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    
    // Extract search parameters with defaults
    const query = searchParams.get('q') || searchParams.get('query') || '';
    const experienceLevel = searchParams.get('experience') || searchParams.get('experienceLevel');
    const category = searchParams.get('category');
    const jobType = searchParams.get('jobType');
    const remoteOnly = searchParams.get('remote') === 'true';

    console.log('Fetching jobs from RemoteOK API...');
    
    // Fetch from RemoteOK API (no auth required!)
    const response = await fetch('https://remoteok.com/api', {
      method: 'GET',
      headers: {
        'User-Agent': 'JobBoard-App',
      },
    });

    if (!response.ok) {
      throw new Error(`RemoteOK API error: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    
    // RemoteOK returns array with first item being metadata, skip it
    const jobData = Array.isArray(result) ? result.slice(1) : [];
    
    // Transform RemoteOK jobs to our Job interface
    let jobs: Job[] = jobData
      .filter((job: any) => job && job.id) // Filter out invalid entries
      .map((job: any) => transformRemoteOKJob(job));
    
    // Apply client-side filters
    if (query && query.trim() !== '') {
      const searchQuery = query.toLowerCase();
      jobs = jobs.filter(job => 
        job.title.toLowerCase().includes(searchQuery) ||
        job.company.toLowerCase().includes(searchQuery) ||
        job.description.toLowerCase().includes(searchQuery) ||
        job.category.toLowerCase().includes(searchQuery)
      );
    }
    
    if (experienceLevel && experienceLevel !== 'All Levels' && experienceLevel !== '') {
      jobs = jobs.filter(job => job.experienceLevel === experienceLevel);
    }
    
    if (category && category !== 'All Categories' && category !== '') {
      jobs = jobs.filter(job => job.category === category);
    }
    
    if (jobType && jobType !== 'All Types' && jobType !== '') {
      jobs = jobs.filter(job => job.type === jobType);
    }

    console.log(`Found ${jobs.length} jobs after filtering`);

    return NextResponse.json({
      data: jobs,
      status: 200,
      message: 'Jobs fetched successfully from RemoteOK',
      totalResults: jobs.length,
      source: 'RemoteOK',
      query: {
        q: query,
        experienceLevel,
        category,
        jobType,
        remoteOnly,
      },
    }, {
      headers: {
        'Cache-Control': 'public, s-maxage=600, stale-while-revalidate=1200',
      },
    });

  } catch (error) {
    console.error('API Error:', error);
    
    return NextResponse.json(
      {
        data: [],
        status: 500,
        message: error instanceof Error ? error.message : 'Failed to fetch jobs',
        error: process.env.NODE_ENV === 'development' ? error : undefined,
      },
      { status: 500 }
    );
  }
}