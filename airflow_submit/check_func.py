import os
import constants
import glob


def get_last_dag_id (uid, db_connection):
    """Get the latest dag run for current uid"""
    db_connection.cursor.execute("select dag_id from dag_run where dag_id like '%{0}%'".format(uid))
    dags = db_connection.cursor.fetchall()
    return sorted([dag[0] for dag in dags])[-1] if dags else None


def get_tasks (uid, db_connection):
    """Get all tasks splitted into status groups for running dag by uid"""
    db_connection.cursor.execute("select task_id, state from task_instance where dag_id='{0}'".format(get_last_dag_id(uid, db_connection)))
    collected = {}
    tasks = db_connection.cursor.fetchall()
    for state in ['queued','running','success','shutdown','failed','up_for_retry','upstream_failed','skipped']:
        collected[state] = [task[0] for task in tasks if task[1]==state]
    return collected, len(tasks)


# def check_job(db_connection, uid, jobs_folder):
#     """Check status for current job from Airflow DB"""
#     tasks, total = get_tasks(uid, db_connection)
#     tasks = {k: v for k,v in tasks.iteritems() if v}
#     failed_file = os.path.join(jobs_folder, constants.JOBS_FAIL, uid + '.json')
#     running_file = os.path.join(jobs_folder, constants.JOBS_RUNNING, uid + '.json')
#     new_file = os.path.join(jobs_folder, constants.JOBS_NEW, uid + '.json')
#     if not tasks and os.path.isfile(failed_file):
#         return constants.STATUS["FAIL_PROCESS"], None
#     elif not tasks and (os.path.isfile(running_file) or os.path.isfile(new_file)):
#         return constants.STATUS["JOB_CREATED"], None
#     elif tasks.get("failed"):
#         return constants.STATUS["FAIL_PROCESS"], tasks
#     elif total > 0 and len(tasks.get("success", [])) == total: # All the tasks exit with success
#         return constants.STATUS["SUCCESS_PROCESS"], tasks
#     else:
#         return constants.STATUS["PROCESSING"], tasks


def check_job(db_connection, uid, jobs_folder):
    """Check status for current job from Airflow DB"""
    tasks, total = get_tasks(uid, db_connection)
    tasks = {k: v for k,v in tasks.iteritems() if v}
    failed_file = os.path.join(jobs_folder, constants.JOBS_FAIL, uid + '.*')
    running_file = os.path.join(jobs_folder, constants.JOBS_RUNNING, uid + '.*')
    new_file = os.path.join(jobs_folder, constants.JOBS_NEW, uid + '.*')
    if tasks:
        if tasks.get("failed"):
            return constants.STATUS["FAIL_PROCESS"], tasks
        elif total > 0 and len(tasks.get("success", [])) == total:  # All the tasks exit with success
            return constants.STATUS["SUCCESS_PROCESS"], tasks
        else:
            return constants.STATUS["PROCESSING"], tasks
    else:
        if glob.glob(failed_file):
            return constants.STATUS["FAIL_PROCESS"], None
        elif glob.glob(running_file) or glob.glob(new_file):
            return constants.STATUS["JOB_CREATED"], None
        else:
            return constants.STATUS["UNKNOWN"], None