DEFAULT_CONFIG="./airflow_submit.cfg"

JOBS_NEW = 'new'
JOBS_SUCCESS = 'success'
JOBS_FAIL = 'fail'
JOBS_RUNNING = 'running'


STATUS = {
    "JOB_CREATED":       1010, # Job file is created
    "FAIL_PROCESS":      2010, # Processing failed
    "SUCCESS_PROCESS":   12,   # Processing succeed
    "PROCESSING":        11,   # Processing
    "UNKNOWN":           0     # Unknown
}