import airflow

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from airflow.contrib.operators.emr_create_job_flow_operator import EmrCreateJobFlowOperator
from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor
from airflow.contrib.operators.emr_terminate_job_flow_operator import EmrTerminateJobFlowOperator

from configuration.config import JOB_FLOW_OVERRIDES, EMR_STEPS


DAG_ID = os.path.basename(__file__).replace(".py", "")


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1),      # this in combination with catchup=False ensures the DAG being triggered from the current date onwards along the set interval
    'provide_context': True,                            # this is set to True as we want to pass variables on from one task to another
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,

}


with DAG(
	dag_id=DAG_ID, 
	default_args=args, 
	dagrun_timeout=timedelta(hours=2), 
	schedule_interval='@once', 
	catchup=False,
	tags=['emr'],
	) as dag:


	start_data_pipeline = DummyOperator(
		task_id="start_data_pipeline"
	)


	create_emr_cluster = EmrCreateJobFlowOperator(
		task_id="create_emr_cluster",
		aws_conn_id="aws_default",
		emr_conn_id="emr_default",
		job_flow_overrides=JOB_FLOW_OVERRIDES

	)


	add_emr_steps = EmrAddStepsOperator(
		task_id="add_emr_steps",
		job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
		aws_conn_id="aws_default",
		steps=EMR_STEPS
	)


	last_step = len(EMR_STEPS) - 1



	execute_emr_step = EmrStepSensor(
		task_id="execute_(monitor)_emr_step",
		job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value')  }}",
		step_id="{{ task_instance.xcom_pull(task_ids='add_emr_steps', key='return_value')["
		+ str(last_step)
		+ "] }}",
		aws_conn_id="aws_default"
	)


	terminate_emr_cluster = EmrTerminateJobFlowOperator(
		task_id="terminate_emr_cluster",
		job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
		aws_conn_id="aws_default"

	)


	end_data_pipeline = DummyOperator(
		task_id="end_data_pipeline"
	)


	start_data_pipeline >> create_emr_cluster >> add_emr_steps 
	add_emr_steps >> execute_emr_step >> terminate_emr_cluster >> end_data_pipeline