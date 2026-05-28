# AWS DMS Task Restart and Status Checker

<img width="727" height="357" alt="image" src="https://github.com/user-attachments/assets/0ba6aa30-893a-49a8-98e2-3c6db1d617e3" />

## Overview

**AWS DMS Task Restart and Status Checker** is a Python-based automation project designed to monitor, restart, and validate AWS Database Migration Service replication tasks.

The project uses **Boto3** to interact with AWS DMS and **Mage.ai** to orchestrate the execution as a data pipeline block. It supports scenarios where multiple DMS replication tasks need to be restarted and cases where a task should only be restarted when it is in a failed state.

This solution is useful for data engineering workflows that depend on stable, automated, and observable database migration pipelines.

## Main Features

* Monitor AWS DMS replication task status.
* Restart one or multiple DMS replication tasks.
* Restart tasks only when they are in failed states.
* Validate task execution using Mage.ai test blocks.
* Store AWS credentials securely through Mage.ai secrets.
* Support automated recovery for unstable DMS tasks.
* Improve reliability in ETL and data migration pipelines.

## Technologies Used

* Python
* AWS Database Migration Service
* Boto3
* Mage.ai
* AWS IAM
* AWS Secrets Management through Mage.ai secrets

## Project Structure

```bash
AWS-DMS-task-restart-and-status-checker/
├── README.md
├── requirements.txt
└── mage_blocks/
    ├── restart_multiple_dms_tasks.py
    └── check_and_restart_dms_task.py
```

## Prerequisites

Before running this project, make sure you have:

* An active AWS account.
* AWS DMS enabled.
* Existing DMS replication tasks.
* IAM permissions to describe and start DMS replication tasks.
* Mage.ai installed and configured.
* AWS credentials stored securely in Mage.ai secrets.

## Required IAM Permissions

The AWS user or role used by the pipeline must have permissions similar to:

```json
{
  "Effect": "Allow",
  "Action": [
    "dms:DescribeReplicationTasks",
    "dms:StartReplicationTask"
  ],
  "Resource": "*"
}
```

For production environments, it is recommended to restrict the `Resource` field to the specific DMS task ARNs used by the project.

## Installation

Clone the repository:

```bash
git clone https://github.com/nathadriele/AWS-DMS-task-restart-and-status-checker.git
cd AWS-DMS-task-restart-and-status-checker
```

Install the required dependencies:

```bash
pip install boto3 mage-ai
```

Alternatively, if using a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Mage.ai Secrets Configuration

This project expects the AWS credentials to be available through Mage.ai secrets.

Configure the following secrets in Mage.ai:

```text
aws_access_key_id
aws_secret_access_key
```

These values are accessed in the code using:

```python
get_secret_value('aws_access_key_id')
get_secret_value('aws_secret_access_key')
```

## Usage

### Option 1: Restart Multiple DMS Tasks

This approach restarts a predefined list of DMS replication tasks and returns their current status after the restart command is triggered.

Example task list:

```python
task_arns = [
    'arn:aws:dms:us-east-1:account-id:task:your-task-id1',
    'arn:aws:dms:us-east-1:account-id:task:your-task-id2',
    'arn:aws:dms:us-east-1:account-id:task:your-task-id3',
    'arn:aws:dms:us-east-1:account-id:task:your-task-id4',
    'arn:aws:dms:us-east-1:account-id:task:your-task-id5'
]
```

Each task is restarted using:

```python
client.start_replication_task(
    ReplicationTaskArn=task_arn,
    StartReplicationTaskType='reload-target'
)
```

After the restart command, the script checks the task status using:

```python
client.describe_replication_tasks(
    Filters=[{'Name': 'replication-task-arn', 'Values': [task_arn]}]
)
```

The output is a dictionary containing each task ARN and its returned status.

Example output:

```python
{
    "arn:aws:dms:us-east-1:account-id:task:your-task-id1": "starting",
    "arn:aws:dms:us-east-1:account-id:task:your-task-id2": "starting"
}
```

## Option 2: Check Status Before Restarting

This approach checks the current status of a DMS replication task before deciding whether to restart it.

The task is restarted only when its current status is one of the following:

```python
['failed', 'error', 'failed-move']
```

If the task is not in a failed state, no restart is performed.

Example behavior:

```text
Current task status: running
The task is not in a failed state. No need to restart.
```

If the task is failed:

```text
Current task status: failed
Restarting the DMS task...
DMS Task Restarted
starting
The task is running or completed.
```

## Task Monitoring Logic

After a restart, the script monitors the DMS task status in a loop.

Successful or acceptable states:

```python
[
    'stopped',
    'running',
    'ready',
    'starting',
    'stopping',
    'starting-replication',
    'replicating'
]
```

Failed states:

```python
[
    'failed',
    'failed-move',
    'error'
]
```

If the task reaches an acceptable state, the function returns:

```python
{'status': 1}
```

If the task reaches a failed state, the function returns:

```python
{'status': 0}
```

## Testing

Mage.ai allows testing pipeline block outputs using the `@test` decorator.

For the multiple-task restart approach, the test validates whether:

* The output is a dictionary.
* Each DMS task returned the expected status.

Example:

```python
@test
def test_output(output, *args) -> None:
    expected_status = 'starting'

    assert isinstance(output, dict), 'Output is not a dictionary'

    for task_arn, status in output.items():
        assert status == expected_status, (
            f'Task {task_arn} did not start correctly. Status: {status}'
        )
```

For the conditional restart approach, a recommended test is:

```python
@test
def test_output(output, *args) -> None:
    assert isinstance(output, dict), 'Output must be a dictionary'
    assert 'status' in output, 'Output must contain the status key'
    assert output['status'] in [0, 1], 'Status must be either 0 or 1'
```

## Example `requirements.txt`

```txt
boto3
mage-ai
```

## Contribution to Data Engineering

This project contributes to data engineering workflows by automating the operational management of AWS DMS replication tasks. It reduces manual intervention, improves reliability, and provides a reusable pattern for monitoring and recovering data migration processes.

By integrating AWS DMS, Boto3, and Mage.ai, the project demonstrates a practical approach to building cloud-native automation for ETL and data migration pipelines.

## Repository

```bash
https://github.com/nathadriele/AWS-DMS-task-restart-and-status-checker
```

