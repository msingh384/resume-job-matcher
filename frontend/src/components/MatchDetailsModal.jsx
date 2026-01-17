import { X, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react';

function MatchDetailsModal({ job, onClose }) {
  const getMatchColor = (score) => {
    if (score >= 70) return 'text-green-600';
    if (score >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getMatchRecommendation = (score) => {
    if (score >= 70) {
      return {
        icon: CheckCircle,
        color: 'text-green-600',
        title: 'Great Match!',
        message: 'Your resume aligns well with this job. You should definitely apply!',
      };
    }
    if (score >= 50) {
      return {
        icon: AlertCircle,
        color: 'text-yellow-600',
        title: 'Good Match',
        message: 'This job is a decent fit. Consider highlighting the missing keywords in your application.',
      };
    }
    return {
      icon: AlertCircle,
      color: 'text-red-600',
      title: 'Fair Match',
      message: 'This job might be challenging. Focus on the missing skills or consider if it\'s the right fit.',
    };
  };

  const matchScore = job.match_score || 0;
  const recommendation = getMatchRecommendation(matchScore);
  const Icon = recommendation.icon;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">Match Analysis</h2>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-6 h-6 text-gray-600" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Job Info */}
          <div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">{job.title}</h3>
            {job.company && (
              <p className="text-lg text-gray-600">{job.company}</p>
            )}
          </div>

          {/* Match Score */}
          <div className="card bg-gradient-to-br from-primary-50 to-primary-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Overall Match Score</p>
                <div className="flex items-center space-x-3">
                  <TrendingUp className={`w-8 h-8 ${getMatchColor(matchScore)}`} />
                  <span className={`text-5xl font-bold ${getMatchColor(matchScore)}`}>
                    {Math.round(matchScore)}%
                  </span>
                </div>
              </div>
              <div className="w-32 h-32">
                <svg className="transform -rotate-90 w-32 h-32">
                  <circle
                    cx="64"
                    cy="64"
                    r="56"
                    stroke="currentColor"
                    strokeWidth="8"
                    fill="transparent"
                    className="text-gray-200"
                  />
                  <circle
                    cx="64"
                    cy="64"
                    r="56"
                    stroke="currentColor"
                    strokeWidth="8"
                    fill="transparent"
                    strokeDasharray={`${2 * Math.PI * 56}`}
                    strokeDashoffset={`${2 * Math.PI * 56 * (1 - matchScore / 100)}`}
                    className={getMatchColor(matchScore)}
                    strokeLinecap="round"
                  />
                </svg>
              </div>
            </div>
          </div>

          {/* Recommendation */}
          <div className={`card border-2 ${recommendation.color.replace('text-', 'border-')}`}>
            <div className="flex items-start space-x-3">
              <Icon className={`w-6 h-6 ${recommendation.color} flex-shrink-0 mt-1`} />
              <div>
                <h4 className={`font-semibold text-lg mb-1 ${recommendation.color}`}>
                  {recommendation.title}
                </h4>
                <p className="text-gray-600">{recommendation.message}</p>
              </div>
            </div>
          </div>

          {/* Keyword Gaps */}
          {job.keyword_gaps && job.keyword_gaps.length > 0 && (
            <div>
              <h4 className="font-semibold text-lg text-gray-900 mb-3">
                Missing Keywords ({job.keyword_gaps.length})
              </h4>
              <p className="text-sm text-gray-600 mb-3">
                These important keywords from the job description are not in your resume:
              </p>
              <div className="flex flex-wrap gap-2">
                {job.keyword_gaps.map((keyword, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-2 bg-red-50 text-red-700 rounded-lg text-sm font-medium border border-red-200"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
              <p className="text-sm text-gray-600 mt-3">
                💡 <strong>Tip:</strong> If you have experience with these skills, consider adding them to your resume or cover letter.
              </p>
            </div>
          )}

          {/* Job Description */}
          <div>
            <h4 className="font-semibold text-lg text-gray-900 mb-3">Full Job Description</h4>
            <div className="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto">
              <p className="text-sm text-gray-700 whitespace-pre-wrap">{job.description}</p>
            </div>
          </div>

          {/* Actions */}
          <div className="flex space-x-3 pt-4 border-t border-gray-200">
            {job.url && (
              <a
                href={job.url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary flex-1 text-center"
              >
                View Job Posting
              </a>
            )}
            <button onClick={onClose} className="btn-secondary">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MatchDetailsModal;

