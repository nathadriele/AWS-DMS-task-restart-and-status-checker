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


















