## AWS DMS Task Restart and Status Checker

### Overview

The AWS DMS Task Restart and Status Checker is a Python script designed to restart multiple AWS Database Migration Service (DMS) tasks and verify their statuses. This script leverages AWS SDK (Boto3) and Mage.ai for seamless integration and management of DMS tasks, ensuring efficient and reliable task handling.

### Prerequisites

- Before using this script, ensure you have the following:
    - AWS Account: Access to an AWS account with DMS service enabled.
    - IAM Permissions: Appropriate IAM permissions to restart DMS tasks and describe their statuses.
    - Mage.ai: Installed and configured in your environment.
    - AWS Credentials: Stored securely and accessible through get_secret_value function.

### Installation

1. Clone the Repository:

git clone https://github.com/nathadriele/AWS-DMS-task-restart-and-status-checker.git
cd dms-task-manager

2. Install Dependencies:
Make sure you have boto3 and mage-ai installed:

pip install boto3 mage-ai


















