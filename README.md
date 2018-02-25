# AWS Qiita Backup
To store all Qiita posting to Amazon S3.

# Prepare
Configure dev.yml or prd.yml

|Key|Contents|
|---|---|
|S3_BUCKET|Amazon S3 target bucket name|
|SETTING_FILE_NAME|Setting file name for URL list|
|BACKUP_FILE_NAME|Backup file name for Qiita contents|

# Deploy

```sh
$ sls deploy [--stage prd/dev]
```
(Default stage is "dev")

# Parameter of execution
JSON data for name setting is needed. Sample is below.

```
{
  "name": "kojiisd"
}
```
