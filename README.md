
# emr-on-airflow-toolkit

A template that allows users effectively set-up data pipelines on AWS EMR clusters using Airflow for scheduling and managing ETL workflows with the option of doing this either ```locally``` (i.e. the infrastructure sits on a docker container in a local environment) or on the ```cloud``` (in this scenario, AWS MWAA manages the infrastructure/workflow).


## Usage
As discussed during the overview; the project is split into two alternative sections - A section that allows for the workflow to work entirely on AWS MWAA (```cloud```); and a section where the workflow will be executed exclusively on the ```local``` environment (via ```docker/airflow```)

####  *Cloud*
![alt text](https://github.com/BrightEmah123/emr-on-airflow-toolkit/blob/main/img/cloud.png?raw=true)

* Clone the repo to the local environment
* The first thing that has to be done is to set-up the configurations for the EMR cluster; this can all be done on the [configuration](https://github.com/BrightEmah123/emr-on-airflow-toolkit/tree/main/cloud/dags/configuration) directory. 
  * The first config file to edit will be the [airflow_variables.json](https://github.com/BrightEmah123/emr-on-airflow-toolkit/blob/main/cloud/dags/configuration/airflow_variables/airflow_variables.json) file``` which stores the settings needed by the airflow DAGS. As seen
	below here’s a sample of the json file with its definitions.
	```
		{
    		"BOOTSTRAP_KEY": <s3://bucket/configuration/emr_bootstrap/emr_bootstrap.sh>,
    		"JOB_NAME": <EMR Job Name>,
            "RELEASE_LABEL": <EMR version>,
            "CORE_INSTANCE_TYPE": <instance type>,
            "MASTER_INSTANCE_TYPE": <instance type>,
            "MASTER_INSTANCE_COUNT": <instance count>,
            "CORE_INSTANCE_COUNT": <instance count>,
            "INSTANCE_GROUP_MARKET": <group market>,
            "EXECUTOR_MEMORY": <executor memory>,
            "EBSROOTVOLSIZE": <root vol size>

		}
	```

  * What follows next will be to edit the [applications.json](https://github.com/BrightEmah123/emr-on-airflow-toolkit/blob/main/cloud/dags/configuration/emr_applications/applications.json).
	```
		[
            {
        		"Name": <application name like Hive, Hadoop, Spark, Livy, etc>
    		}
		]
	```

  * If there’s a need to install additional software like python packages on the EMR cluster, edit the [emr_bootstrap.sh](https://github.com/BrightEmah123/emr-on-airflow-toolkit/blob/main/cloud/dags/configuration/emr_bootstrap/emr_bootstrap.sh) bash script.

  * [EMR Steps](https://github.com/BrightEmah123/emr-on-airflow-toolkit/blob/main/cloud/dags/configuration/emr_steps/steps.json) has a template that can be completed from the configurations directory


* With the configurations complete, create the ```ETL``` script on the [src](https://github.com/BrightEmah123/emr-on-airflow-toolkit/tree/main/cloud/dags/src) directory, this script will be moved to the EMR cluster subsequently

* Next create a  ```DAG``` folder on a specified s3 bucket on AWS.

* Upload the [configuration](https://github.com/BrightEmah123/emr-on-airflow-toolkit/tree/main/cloud/dags/configuration) and [src](https://github.com/BrightEmah123/emr-on-airflow-toolkit/tree/main/cloud/dags/src) folder along with its contents to the ```DAG``` folder on the s3 bucket 

* Also upload the [spark_submit_DAG.py](https://github.com/BrightEmah123/emr-on-airflow-toolkit/tree/main/cloud/dags/spark_submit_DAG.py) script to the ```DAG``` folder on the s3 bucket

* Setup the airflow environment on AWS MWAA; feel free to follow this [step-on-setting-AWS-mwaa-up](https://www.youtube.com/watch?v=ZET50M20hkU&t=3s) and then run the DAG from the Airflow UI to initiate the ETL pipeline

####  *Local*
![alt text](https://github.com/BrightEmah123/emr-on-airflow-toolkit/blob/main/img/local.png?raw=true)

💥 Note: Docker is required for this section.
* Same as discussed on the ```Cloud``` section, the templates on the [configurations](https://github.com/BrightEmah123/emr-on-airflow-toolkit/tree/main/local/dags/configuration) directory will be worked on and uploaded to a specified s3 bucket; 
	* The definitions for the airflow_variables.json template is quite different; here’s the template
	```
    {
	    "BOOTSTRAP_KEY": <s3://bucket/configuration/emr_bootstrap/emr_bootstrap.sh>,
        "SPARK_SCRIPT_KEY": <s3://bucket/src/>,
        "JOB_NAME": <name of the EMR cluster>,
        "RELEASE_LABEL": <EMR version>,
        "CORE_INSTANCE_TYPE": <instance type>,
        "MASTER_INSTANCE_TYPE": <instance type>,
        "MASTER_INSTANCE_COUNT": <instance count>,
        "CORE_INSTANCE_COUNT": <instance count>,
        "INSTANCE_GROUP_MARKET": <group market>,
        "EXECUTOR_MEMORY": <executor memory>,
        "EBSROOTVOLSIZE": <root vol size>
    }
    ``` 
	* Refer to the ```Cloud``` section on how to work on the other configuration files  (i.e. the [applications.json](), [emr_bootstrap.json](), [steps.json]()
	
* Initiate the airflow container by running this command on the terminal
```bash
docker-compose up
```

* If everything goes well, visit the [airflow](http://localhost:8080) admin console to start-up the ETL dags.


## Appendix

This project is open to contributions and additions from the community; feel free to open an issue if you experience any problem


## Authors

- [@bright_emah](https://www.github.com/BrightEmah123)

  