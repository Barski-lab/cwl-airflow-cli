import sys
import argparse
import os
import constants
import ConfigParser
import uuid
import json
import connect
import ruamel.yaml as yaml
from check_func import check_job


def read_config(config_file):
    """Reads configuration file"""
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config

# SubParsers function
def submit(args, conf):
    workflow_dest = os.path.join(conf.get('cwl','cwl_workflows'), args.uid + os.path.splitext(args.workflow)[1])
    job_dest = os.path.join(conf.get('cwl','cwl_jobs'), constants.JOBS_NEW,  args.uid + os.path.splitext(args.job)[1])
    os.rename(args.workflow, workflow_dest)
    os.rename(args.job, job_dest)
    return {"uid": args.uid,
            "worflow": workflow_dest,
            "job": job_dest}


def check(args, conf):
    db_connection=connect.DbConnect(conf)
    status, tasks = check_job (db_connection, args.uid, conf.get('cwl','cwl_jobs'))
    return {'uid':    args.uid,
            'status': next((status_txt for status_txt,status_code in constants.STATUS.items() if status_code == status), None),
            'tasks':  tasks
    }


def gen_error_status(args, ex):
    return {"uid": args.uid,
            "error": str(ex)}


def gen_uid (args):
    try:
        with open(args.job, 'r') as f:
            job = yaml.safe_load(f) or {}
            uid = job.get("uid") or args.uid or str(uuid.uuid4())
            return uid
    except IOError as ex: # submit is used, but job is not found
        raise ex
    except: # check is used
        return args.uid


def normalize(args):
    normalized_args = {}
    for key,value in args.__dict__.iteritems():
        if key in ['config', 'workflow', 'job', 'output']:
            normalized_args[key] = value if not value or os.path.isabs(value) else os.path.join(os.getcwd(), value)
        elif key=='uid':
            normalized_args['uid'] = gen_uid (args)
        else:
            normalized_args[key]=value
    return argparse.Namespace (**normalized_args)


def export_to_file(filepath, data):
    with open(filepath, 'w') as output_stream:
        output_stream.write(json.dumps(data, indent=4))


def arg_parser():
    """Returns argument parser"""
    # parent_parser
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("-o", "--output", help="Save output to file", default=None)
    parent_parser.add_argument("-c", "--config", help="Path to configuration file", default=constants.DEFAULT_CONFIG)

    # general_parser
    general_parser = argparse.ArgumentParser(description='airflow-cwl-cli')
    subparsers = general_parser.add_subparsers()
    subparsers.required = True
    submit_parser = subparsers.add_parser(submit.__name__, help="Submit new job", parents=[parent_parser])
    check_parser =  subparsers.add_parser(check.__name__,  help="Check status by uid", parents=[parent_parser])

    # submit_parser
    submit_parser.add_argument ("-u", "--uid", help="Unique ID for submitted job", default=None)
    submit_parser.add_argument ("-w", "--workflow", help="Path to workflow file", required=True)
    submit_parser.add_argument ("-j", "--job", help="Path to job file", required=True)
    submit_parser.set_defaults(func=submit)

    # check_parser
    check_parser.add_argument("-u", "--uid", help="Unique ID for submitted job", required=True)
    check_parser.set_defaults(func=check)

    return general_parser


def main(argsl=None):
    if argsl is None:
        argsl = sys.argv[1:]
    args,_ = arg_parser().parse_known_args(argsl)
    status={}
    try:
        args = normalize(args)
        conf=read_config(args.config)
        status=args.func(args, conf)
    except Exception as ex:
        status=gen_error_status(args,ex)
        sys.exit(1)
    finally:
        if args.output:
            export_to_file(args.output, status)
        else:
            print json.dumps(status, indent=4)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
