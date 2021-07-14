import json
from airflow.models import Variable


BOOTSTRAP_KEY = Variable.get("BOOTSTRAP_KEY")
JOB_NAME = Variable.get("JOB_NAME")
RELEASE_LABEL = Variable.get("RELEASE_LABEL")
CORE_INSTANCE_TYPE = Variable.get("CORE_INSTANCE_TYPE")
MASTER_INSTANCE_TYPE = Variable.get("MASTER_INSTANCE_TYPE")
MASTER_INSTANCE_COUNT = Variable.get("MASTER_INSTANCE_COUNT")
CORE_INSTANCE_COUNT = Variable.get("CORE_INSTANCE_COUNT")
INSTANCE_GROUP_MARKET = Variable.get("INSTANCE_GROUP_MARKET")
EXECUTOR_MEMORY = Variable.get("EXECUTOR_MEMORY")
EBSROOTVOLSIZE = Variable.get("EBSROOTVOLSIZE")


with open("emr_applications/applications.json") as app:
    APPLICATIONS = json.load(app)

with open("emr_steps/steps.json") as step:
    STEPS = json.load(step)


# JOB FLOW OVERRIDES Configuration
JOB_FLOW_OVERRIDES = {
    "Name": "{{ var.value.JOB_NAME }}",
    "ReleaseLabel": "{{ var.value.RELEASE_LABEL }}",
    "Applications": APPLICATIONS,
    "Configurations": [
        {
            "Classification": "spark-env",
            "Configurations": [
                {
                    "Classification": "export",
                    "Properties": {"PYSPARK_PYTHON": "/usr/bin/python3"}, # by default EMR uses py2, change it to py3
                }
            ],
        },
        {
            "Classification": "spark",
            "Properties": {
                "maximizeResourceAllocation": "true"
            }
        },
        {
            "Classification": "spark-defaults",
            "Properties": {
                "spark.executor.memory": "{{ var.value.EXECUTOR_MEMORY }}",
            }
        },
    ],
    "Instances": {
        "InstanceGroups": [
            {
                "Name": "Master node",
                "Market": "{{ var.value.INSTANCE_GROUP_MARKET }}",
                "InstanceRole": "MASTER", 
                "InstanceType": "{{ var.value.MASTER_INSTANCE_TYPE }}",
                "InstanceCount": "{{ var.value.MASTER_INSTANCE_COUNT }}",
            },
            {
                "Name": "Core - 2",
                "Market": "{{ var.value.INSTANCE_GROUP_MARKET }}",
                "InstanceRole": "CORE",
                "InstanceType": "{{ var.value.CORE_INSTANCE_TYPE }}",
                "InstanceCount": "{{ var.value.CORE_INSTANCE_COUNT }}",
            },
        ],
        "KeepJobFlowAliveWhenNoSteps": True,
        "TerminationProtected": False, # this lets us programmatically terminate the cluster
    },
    "BootstrapActions": [
        {
            "Name": "Bootstrap",
            "ScriptBootstrapAction": {
                "Path": "s3://{{ var.value.BOOTSTRAP_KEY }}/emr_bootstrap.sh"
            } 
        }
    ],
    "JobFlowRole": "EMR_EC2_DefaultRole",
    "ServiceRole": "EMR_DefaultRole",
    "EbsRootVolumeSize": "{{ var.value.EBSROOTVOLSIZE }}"
}



# EMR STEPS Configuration
EMR_STEPS = [
    STEPS
]

