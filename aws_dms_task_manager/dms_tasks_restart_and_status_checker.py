if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import boto3
from mage_ai.data_preparation.shared.secrets import get_secret_value

@data_loader
def load_data(*args, **kwargs):
    task_arns = [
        'arn:aws:dms:us-east-1:account-id:task:your-task-id1',
        'arn:aws:dms:us-east-1:account-id:task:your-task-id2',
        'arn:aws:dms:us-east-1:account-id:task:your-task-id3',
        'arn:aws:dms:us-east-1:account-id:task:your-task-id4',
        'arn:aws:dms:us-east-1:account-id:task:your-task-id5'
    ]
    
    client = boto3.client(
        'dms',
        aws_access_key_id=get_secret_value('aws_access_key_id'),
        aws_secret_access_key=get_secret_value('aws_secret_access_key'),
        region_name='us-east-1'
    )
    
    task_statuses = {}
    
    for task_arn in task_arns:
        status = restart_task(client, task_arn)
        task_statuses[task_arn] = status
    
    return task_statuses

def restart_task(client, task_arn):
    response = client.start_replication_task(
        ReplicationTaskArn=task_arn,
        StartReplicationTaskType='reload-target'
    )
    print(f'DMS Task {task_arn} Restarted')

    task_status = client.describe_replication_tasks(
        Filters=[{'Name': 'replication-task-arn', 'Values': [task_arn]}]
    )
    status = task_status["ReplicationTasks"][0]["Status"]
    
    return status

@test
def test_output(output, *args) -> None:
    """
    Test if the tasks were restarted correctly and if the expected statuses were returned.
    """
    expected_status = 'starting'  # Assuming the initial expected status after restarting is 'starting'

    # Check if the output is a dictionary
    assert isinstance(output, dict), 'Output is not a dictionary'

    # Check if all tasks have the expected restart status
    for task_arn, status in output.items():
        assert status == expected_status, f'Task {task_arn} did not start correctly. Status: {status}'
