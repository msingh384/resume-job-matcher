import { useState, useEffect } from 'react';
import { FileText, Briefcase, TrendingUp, Settings, Sparkles } from 'lucide-react';
import ResumeUpload from './components/ResumeUpload';
import JobList from './components/JobList';
import AddJobModal from './components/AddJobModal';
import MatchDetailsModal from './components/MatchDetailsModal';
import { getStatus, getJobs, switchMode } from './api';

function App() {
  const [status, setStatus] = useState({ has_resume: false, ml_mode: false });
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddJob, setShowAddJob] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [statusData, jobsData] = await Promise.all([getStatus(), getJobs()]);
      setStatus(statusData);
      setJobs(jobsData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleResumeUploaded = async () => {
    await loadInitialData();
  };

  const handleJobAdded = async () => {
    const jobsData = await getJobs();
    setJobs(jobsData);
    setShowAddJob(false);
  };

  const handleJobUpdated = async () => {
    const jobsData = await getJobs();
    setJobs(jobsData);
  };

  const handleJobDeleted = async () => {
    const jobsData = await getJobs();
    setJobs(jobsData);
  };

  const handleToggleML = async () => {
    try {
      setLoading(true);
      await switchMode(!status.ml_mode);
      await loadInitialData();
    } catch (error) {
      console.error('Error switching mode:', error);
      alert('Failed to switch mode. Make sure sentence-transformers is installed.');
    } finally {
      setLoading(false);
    }
  };

  const stats = {
    totalJobs: jobs.length,
    averageMatch: jobs.length > 0
      ? Math.round(jobs.reduce((sum, job) => sum + (job.match_score || 0), 0) / jobs.length)
      : 0,
    applied: jobs.filter(j => j.status === 'applied').length,
    interviewed: jobs.filter(j => j.status === 'interview').length,
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-primary-600 p-2 rounded-lg">
                <Briefcase className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Resume-Job Matcher</h1>
                <p className="text-sm text-gray-600">Smart job application assistant</p>
              </div>
            </div>
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              title="Settings"
            >
              <Settings className="w-5 h-5 text-gray-600" />
            </button>
          </div>
        </div>
      </header>

      {/* Settings Panel */}
      {showSettings && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Settings</h3>
            <div className="flex items-center justify-between">
              <div>
                <div className="flex items-center space-x-2">
                  <Sparkles className="w-5 h-5 text-primary-600" />
                  <span className="font-medium">ML Mode (Semantic Matching)</span>
                </div>
                <p className="text-sm text-gray-600 mt-1">
                  Uses sentence embeddings for better understanding. Requires sentence-transformers.
                </p>
              </div>
              <button
                onClick={handleToggleML}
                disabled={loading}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  status.ml_mode ? 'bg-primary-600' : 'bg-gray-300'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    status.ml_mode ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
            <div className="mt-2 text-sm">
              <span className="text-gray-600">Current mode:</span>{' '}
              <span className="font-medium text-primary-600">{status.matcher_type}</span>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading && !jobs.length ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : (
          <div className="space-y-8">
            {/* Resume Upload Section */}
            <ResumeUpload
              hasResume={status.has_resume}
              resumeFilename={status.resume_filename}
              onResumeUploaded={handleResumeUploaded}
            />

            {/* Stats */}
            {status.has_resume && jobs.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="card">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Total Jobs</p>
                      <p className="text-2xl font-bold text-gray-900">{stats.totalJobs}</p>
                    </div>
                    <Briefcase className="w-8 h-8 text-primary-600" />
                  </div>
                </div>
                <div className="card">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Avg Match</p>
                      <p className="text-2xl font-bold text-gray-900">{stats.averageMatch}%</p>
                    </div>
                    <TrendingUp className="w-8 h-8 text-green-600" />
                  </div>
                </div>
                <div className="card">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Applied</p>
                      <p className="text-2xl font-bold text-gray-900">{stats.applied}</p>
                    </div>
                    <FileText className="w-8 h-8 text-blue-600" />
                  </div>
                </div>
                <div className="card">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">Interviews</p>
                      <p className="text-2xl font-bold text-gray-900">{stats.interviewed}</p>
                    </div>
                    <Sparkles className="w-8 h-8 text-yellow-600" />
                  </div>
                </div>
              </div>
            )}

            {/* Jobs Section */}
            {status.has_resume && (
              <div>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-bold text-gray-900">Job Matches</h2>
                  <button onClick={() => setShowAddJob(true)} className="btn-primary">
                    + Add Job
                  </button>
                </div>
                <JobList
                  jobs={jobs}
                  onJobUpdated={handleJobUpdated}
                  onJobDeleted={handleJobDeleted}
                  onViewDetails={setSelectedJob}
                />
              </div>
            )}

            {/* Empty State */}
            {!status.has_resume && (
              <div className="text-center py-12">
                <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Upload your resume to get started
                </h3>
                <p className="text-gray-600">
                  Upload your resume and start matching it with job descriptions
                </p>
              </div>
            )}
          </div>
        )}
      </main>

      {/* Modals */}
      {showAddJob && (
        <AddJobModal onClose={() => setShowAddJob(false)} onJobAdded={handleJobAdded} />
      )}
      {selectedJob && (
        <MatchDetailsModal job={selectedJob} onClose={() => setSelectedJob(null)} />
      )}
    </div>
  );
}

export default App;

