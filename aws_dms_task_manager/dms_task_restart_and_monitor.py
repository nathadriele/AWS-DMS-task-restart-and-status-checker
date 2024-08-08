import boto3
import time
from mage_ai.data_preparation.decorators import data_loader, test
from mage_ai.data_preparation.shared.secrets import get_secret_value

DEFAULT_REPLICATION_TASK_NAME = 'arn:aws:dms:us-east-1:account-id:task:your-task-id1'

@data_loader
def load_data(*args, **kwargs):
    replication_task_name = DEFAULT_REPLICATION_TASK_NAME
    client = boto3.client(
        'dms',
        aws_access_key_id=get_secret_value('aws_access_key_id'),
        aws_secret_access_key=get_secret_value('aws_secret_access_key'),
        region_name='us-east-1'
    )

    # Obtaining the current task status
    current_status = get_task_status(client, replication_task_name)
    print(f'Current task status: {current_status}')

    # Check if the task is in a failed state
    if current_status in ['failed', 'error', 'failed-move']:
        print('Restarting the DMS task...')
        restart_dms_task(client, replication_task_name)
        func_return = monitor_task_status(client, replication_task_name)
    else:
        print('The task is not in a failed state. No need to restart.')
        func_return = {'status': 1}

    return func_return

def get_task_status(client, replication_task_name):
    response = client.describe_replication_tasks(
        Filters=[{'Name': 'replication-task-arn', 'Values': [replication_task_name]}]
    )
    return response['ReplicationTasks'][0]['Status']

def restart_dms_task(client, replication_task_name):
    response = client.start_replication_task(
        ReplicationTaskArn=replication_task_name,
        StartReplicationTaskType='reload-target'
    )
    print('DMS Task Restarted')

def monitor_task_status(client, replication_task_name):
    while True:
        current_status = get_task_status(client, replication_task_name)
        print(current_status)

        if current_status in ['stopped', 'running', 'ready', 'starting', 'stopping', 'starting-replication', 'replicating']:
            print('The task is running or completed.')
            return {'status': 1}
        
        if current_status in ['failed', 'failed-move', 'error']:
            print('The task has failed.')
            return {'status': 0}
        
        time.sleep(10)

@test
def test_output(output, *args) -> None:
    # Template code for testing the output of the block
    pass
