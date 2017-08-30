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
    db_connection.cursor.execute("select task_id, state, start_date, end_date, duration from task_instance where dag_id='{0}'".format(get_last_dag_id(uid, db_connection)))
    collected = {}
    tasks = db_connection.cursor.fetchall()
    for state in ['queued','running','success','shutdown','failed','up_for_retry','upstream_failed','skipped']:
        collected[state] = [{"task_id": task[0], "start_date": task[2], "end_date": task[3], "duration": task[4]} for task in tasks if task[1]==state]
    return collected, len(tasks)


def check_job(db_connection, uid, jobs_folder):
    """Check status for current job from Airflow DB"""
    tasks_raw, total = get_tasks(uid, db_connection)
    tasks= {}
    for state, task_group in tasks_raw.iteritems():
        if task_group:
            tasks[state]=[]
            for task in task_group:
                tasks[state].append(task["task_id"])
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


def get_time(tasks):
    total_duration = 0
    time_stamp_list = []
    for state, task_group in tasks.iteritems():
        for task in task_group:
            if task.get("duration") and task.get("start_date") and task.get("end_date"):
                total_duration = total_duration + task["duration"]
                time_stamp_list.append(task["start_date"])
                time_stamp_list.append(task["end_date"])
    time_stamp_list.sort()
    if time_stamp_list and total_duration:
        return (time_stamp_list[-1]-time_stamp_list[0]).total_seconds(), total_duration
    else:
        return 0,0


def check_time(db_connection, uid):
    tasks, total = get_tasks(uid, db_connection)
    if total > 0 and len(tasks.get("success", [])) == total:  # All the tasks exit with success
        return get_time(tasks)
    else:
        return None,None
