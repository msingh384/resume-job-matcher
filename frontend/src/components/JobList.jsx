import JobCard from './JobCard';

function JobList({ jobs, onJobUpdated, onJobDeleted, onViewDetails }) {
  if (jobs.length === 0) {
    return (
      <div className="card text-center py-12">
        <p className="text-gray-600 text-lg">No jobs yet. Add your first job to get started!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {jobs.map((job) => (
        <JobCard
          key={job.id}
          job={job}
          onJobUpdated={onJobUpdated}
          onJobDeleted={onJobDeleted}
          onViewDetails={onViewDetails}
        />
      ))}
    </div>
  );
}

export default JobList;

