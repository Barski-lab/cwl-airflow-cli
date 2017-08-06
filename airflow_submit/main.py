import sys
import argparse
import os
import constants
import ConfigParser

def arg_parser():
    """Returns argument parser"""
    parser = argparse.ArgumentParser(description='Airflow-submit, 2017')
    parser.add_argument ("-w", "--workflow", help="Path to workflow file", required=True)
    parser.add_argument ("-j", "--job", help="Path to job file", required=True)
    parser.add_argument("-u", "--uid", help="Unique ID for submitted job", default=None)

    parser.add_argument("-c", "--config", help="Path to configuration file", default=None)
    parser.add_argument("-s", "--workflow-folder", help="Path to the folder to save workflow", default=None)
    parser.add_argument("-t", "--job-folder", help="Path to the folder to save job file", default=None)

    parser.add_argument("-o", "--output", help="Save output to file", default=None)
    return parser


def main(argsl=None):
    if argsl is None:
        argsl = sys.argv[1:]
    args, _ = arg_parser().parse_known_args(argsl)
    argv=args.__dict__

    # trying to read workflow and job folder from config file
    try:
        config = ConfigParser.ConfigParser()
        config_file = argv.config if argv.config else constants.DEFAULT_CONFIG
        abs_config_file= config_file if os.path.isabs(config_file) else os.path.join(os.getcwd(), config_file)
        config.read(abs_config_file)
        argv["workflow_folder"] = config.get('cwl', 'cwl_workflows')
        argv["job_folder"] = config.get('cwl', 'cwl_jobs')
        print "workflow_folder and job_folder are set from config file"
    except ConfigParser.Error:
        pass

    # trying to get workflow and job folder as arguments
    try:
        argv["workflow_folder"]=args.workflow_folder
        argv["job_folder"] = args.job_folder
    except:
        pass




    try:
        connection = sqlite3.connect(sql_temp_file)
        run_sql_script(connection, CREATE_REFGENE_TABLE_SCRIPT)
        header = load_from_file(connection, args.input)
        export_to_file (header, select_from_db(connection, args.querry, args.order), args.output)
        connection.close()
    except Exception as ex:
        print str(ex)
    finally:
        os.remove(sql_temp_file)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
