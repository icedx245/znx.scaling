def run_script(script_path):
"""
This module defines a Prefect flow for orchestrating a data pipeline with monitoring and scheduling capabilities.

Functions:
    run_script(script_path): Prefect task that executes a Python script at the given path, with retries and logging.
    data_pipeline(): Prefect flow that sequentially runs data ingestion, cleaning, analysis, and visualization scripts.
    deploy(): Applies the scheduled deployment for the data pipeline flow.

Deployment:
    A scheduled deployment is created to run the data pipeline daily at 2am UTC.

Usage:
    Run this module directly to create the deployment. Instructions for starting the Prefect server and UI are provided.
"""
from prefect import flow, task, get_run_logger
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
import subprocess

@task(retries=2, retry_delay_seconds=10)
def run_script(script_path):
    logger = get_run_logger()
    logger.info(f"Running {script_path}")
    try:
        subprocess.run(["python3", script_path], check=True)
        logger.info(f"Completed {script_path}")
    except Exception as e:
        logger.error(f"Error running {script_path}: {e}")
        raise

@flow(log_prints=True)
def data_pipeline():
    run_script("../workflows/data_ingestion.py")
    run_script("../workflows/data_cleaning.py")
    run_script("../workflows/data_analysis.py")
    run_script("../workflows/cash_flow.py")
    run_script("../workflows/data_visualization.py")

# Advanced: Create a scheduled deployment (runs every day at 2am)
data_pipeline_deployment = Deployment.build_from_flow(
    flow=data_pipeline,
    name="Daily Data Pipeline",
    schedule=(CronSchedule(cron="0 2 * * *", timezone="UTC")),
)

def deploy():
    data_pipeline_deployment.apply()

if __name__ == "__main__":
    deploy()
    print("Deployment created. To run Prefect server: 'prefect server start'")
    print("To view logs and monitor: 'prefect ui' or visit http://127.0.0.1:4200")
