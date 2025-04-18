# Log Archiver & S3 Uploader

## 🔧 Tools
- Python
- boto3, os, shutil

## 📦 Features
- Scans `/var/log` for `.log` files older than 7 days
- Zips the logs with a timestamped filename
- Uploads the archive to an S3 bucket under `archived_logs/`

## 📁 Structure
log-archiver/ ├── archiver.py ├── README.md ├── requirements.txt └── logs/ └── sample.log

## 🚀 Usage

1. Set your AWS credentials in the environment or via AWS config
2. Replace `your-s3-bucket-name` in `archiver.py`
3. Run the script:

```bash
python3 archiver.py