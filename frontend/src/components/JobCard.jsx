import { useState } from 'react';
import { Building2, ExternalLink, Trash2, Eye, Calendar, TrendingUp } from 'lucide-react';
import { updateJob, deleteJob } from '../api';

const STATUS_OPTIONS = [
  { value: 'saved', label: 'Saved', color: 'badge-gray' },
  { value: 'applied', label: 'Applied', color: 'badge-info' },
  { value: 'interview', label: 'Interview', color: 'badge-warning' },
  { value: 'offer', label: 'Offer', color: 'badge-success' },
  { value: 'rejected', label: 'Rejected', color: 'badge-gray' },
];

function JobCard({ job, onJobUpdated, onJobDeleted, onViewDetails }) {
  const [isUpdating, setIsUpdating] = useState(false);

  const statusInfo = STATUS_OPTIONS.find(s => s.value === job.status) || STATUS_OPTIONS[0];

  const handleStatusChange = async (newStatus) => {
    setIsUpdating(true);
    try {
      await updateJob(job.id, { status: newStatus });
      onJobUpdated();
    } catch (error) {
      console.error('Error updating job:', error);
      alert('Failed to update job status');
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this job?')) return;
    
    try {
      await deleteJob(job.id);
      onJobDeleted();
    } catch (error) {
      console.error('Error deleting job:', error);
      alert('Failed to delete job');
    }
  };

  const getMatchColor = (score) => {
    if (score >= 70) return 'text-green-600 bg-green-50';
    if (score >= 50) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  const getMatchLabel = (score) => {
    if (score >= 70) return 'Great Match';
    if (score >= 50) return 'Good Match';
    return 'Fair Match';
  };

  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-900 mb-1">{job.title}</h3>
              {job.company && (
                <div className="flex items-center text-gray-600 mb-2">
                  <Building2 className="w-4 h-4 mr-2" />
                  <span>{job.company}</span>
                </div>
              )}
            </div>
            
            {/* Match Score */}
            <div className={`ml-4 px-4 py-2 rounded-lg ${getMatchColor(job.match_score || 0)}`}>
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-4 h-4" />
                <span className="text-2xl font-bold">{Math.round(job.match_score || 0)}%</span>
              </div>
              <p className="text-xs mt-1">{getMatchLabel(job.match_score || 0)}</p>
            </div>
          </div>

          {/* Description Preview */}
          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
            {job.description}
          </p>

          {/* Keyword Gaps */}
          {job.keyword_gaps && job.keyword_gaps.length > 0 && (
            <div className="mb-3">
              <p className="text-xs text-gray-600 mb-2">Missing Keywords:</p>
              <div className="flex flex-wrap gap-2">
                {job.keyword_gaps.slice(0, 5).map((keyword, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-red-50 text-red-700 rounded text-xs font-medium"
                  >
                    {keyword}
                  </span>
                ))}
                {job.keyword_gaps.length > 5 && (
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                    +{job.keyword_gaps.length - 5} more
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Metadata */}
          <div className="flex items-center space-x-4 text-sm text-gray-500 mb-4">
            <div className="flex items-center">
              <Calendar className="w-4 h-4 mr-1" />
              <span>{new Date(job.created_at).toLocaleDateString()}</span>
            </div>
            {job.url && (
              <a
                href={job.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center text-primary-600 hover:text-primary-700"
              >
                <ExternalLink className="w-4 h-4 mr-1" />
                <span>View Posting</span>
              </a>
            )}
          </div>

          {/* Actions */}
          <div className="flex items-center justify-between pt-3 border-t border-gray-200">
            <div className="flex items-center space-x-2">
              <label className="text-sm text-gray-600">Status:</label>
              <select
                value={job.status}
                onChange={(e) => handleStatusChange(e.target.value)}
                disabled={isUpdating}
                className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
              >
                {STATUS_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex items-center space-x-2">
              <button
                onClick={() => onViewDetails(job)}
                className="p-2 text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                title="View Details"
              >
                <Eye className="w-5 h-5" />
              </button>
              <button
                onClick={handleDelete}
                className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                title="Delete Job"
              >
                <Trash2 className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default JobCard;

