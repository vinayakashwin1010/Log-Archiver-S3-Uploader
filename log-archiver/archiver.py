import os
import shutil
import boto3
from datetime import datetime, timedelta

# Configuration
LOG_DIR = "/var/log"
ARCHIVE_DIR = "./archives"
S3_BUCKET_NAME = "log-archiver-by-vinayak"  # Replace with your bucket name
DAYS_OLD = 7

# Initialize S3 client
s3 = boto3.client('s3')

def get_old_log_files(directory, days_old):
    old_files = []
    threshold = datetime.now() - timedelta(days=days_old)
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".log"):
                filepath = os.path.join(root, file)
                if datetime.fromtimestamp(os.path.getmtime(filepath)) < threshold:
                    old_files.append(filepath)
    return old_files

def zip_logs(log_files):
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"logs_{timestamp}"
    archive_path = os.path.join(ARCHIVE_DIR, archive_name)
    
    with shutil.make_archive(archive_path, 'zip', root_dir=os.path.dirname(log_files[0]), base_dir=".") as archive:
        pass  # `make_archive` returns the name of the archive
    
    return archive_path + ".zip"

def upload_to_s3(file_path, bucket_name):
    file_name = os.path.basename(file_path)
    try:
        s3.upload_file(file_path, bucket_name, f"archived_logs/{file_name}")
        print(f"✅ Uploaded {file_name} to S3 bucket '{bucket_name}'")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

def main():
    print("🔍 Scanning for old log files...")
    old_logs = get_old_log_files(LOG_DIR, DAYS_OLD)
    
    if not old_logs:
        print("No logs older than 7 days found.")
        return

    print(f"📦 Zipping {len(old_logs)} log file(s)...")
    zip_path = zip_logs(old_logs)

    print(f"☁️ Uploading archive to S3...")
    upload_to_s3(zip_path, S3_BUCKET_NAME)

    print("✅ Done.")

if __name__ == "__main__":
    main()