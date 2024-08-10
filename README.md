## AWS DMS Task Restart and Status Checker

### Overview

The AWS DMS Task Restart and Status Checker is a Python script designed to restart multiple AWS Database Migration Service (DMS) tasks and verify their statuses. This script leverages AWS SDK (Boto3) and Mage.ai for seamless integration and management of DMS tasks, ensuring efficient and reliable task handling.

### Prerequisites

- Before using this script, ensure you have the following:
    - `AWS Account`: Access to an AWS account with DMS service enabled.
    - `IAM Permissions`: Appropriate IAM permissions to restart DMS tasks and describe their statuses.
    - `Mage.ai`: Installed and configured in your environment.
    - `AWS Credentials`: Stored securely and accessible through `get_secret_value` function.

### Installation

1. Clone the Repository:

```py
git clone https://github.com/nathadriele/AWS-DMS-task-restart-and-status-checker.git
cd dms-task-manager
```

2. Install Dependencies:
Make sure you have boto3 and mage-ai installed:

```py
pip install boto3 mage-ai
```

### Code Explanation

#### Load Data Function

The `load_data` function is decorated with `@data_loader` from Mage.ai. It initializes a list of DMS task ARNs and a Boto3 DMS client using credentials fetched via `get_secret_value`. The function iterates over the task ARNs, restarting each task and collecting their statuses into a dictionary, which is then returned.

#### Restart Task Function

The `restart_task` function handles the logic for restarting a specific DMS task using its ARN. It prints confirmation of the restart and retrieves the task's status, which is returned to the caller.

#### Test Output Function

The `test_output` function is decorated with `@test` and is used to validate the functionality of the `load_data` function. It ensures that the output is a dictionary and that each task has the expected status `('starting')`.

#### Testing

To test the script, ensure you have appropriate credentials and ARNs configured. Then, run the script and observe the printed outputs for task restart confirmations and statuses. The `test_output` function will validate the results automatically.

#### Contribution to Data Engineering

This script provides a practical solution for managing AWS DMS tasks by automating task restarts and status checks. It integrates with cloud services using Boto3 and includes automated testing to ensure accurate execution. These features support efficient data migration data engineering practices.
