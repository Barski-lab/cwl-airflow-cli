**usage**
```
usage: cwl-airflow-cli [-h] {submit,check,time} ...

cwl-airflow-cli

positional arguments:
  {submit,check,time}
    submit             Submit new job
    check              Check status by uid
    time               Check time by uid

optional arguments:
  -h, --help           show this help message and exit
```  
**submit**
```bash
usage: cwl-airflow-cli submit [-h] [-o OUTPUT] [-c CONFIG] [-u UID] -w
                              WORKFLOW -j JOB

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Save output to file
  -c CONFIG, --config CONFIG
                        Path to configuration file
  -u UID, --uid UID     Unique ID for submitted job
  -w WORKFLOW, --workflow WORKFLOW
                        Path to workflow file
  -j JOB, --job JOB     Path to job file
```
**check**

```bash
usage: cwl-airflow-cli check [-h] [-o OUTPUT] [-c CONFIG] -u UID

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Save output to file
  -c CONFIG, --config CONFIG
                        Path to configuration file
  -u UID, --uid UID     Unique ID for submitted job
```
**time**

```bash
usage: cwl-airflow-cli time [-h] [-o OUTPUT] [-c CONFIG] -u UID

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Save output to file
  -c CONFIG, --config CONFIG
                        Path to configuration file
  -u UID, --uid UID     Unique ID for submitted job
```