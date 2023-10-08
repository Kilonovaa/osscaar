import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

supaURL = "https://nwhobhigrgxtpnwydpxj.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53aG9iaGlncmd4dHBud3lkcHhqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NjY4Njg1MiwiZXhwIjoyMDEyMjYyODUyfQ.7UxyPZo5PLIEuuntEAXi01t0ZrEc7ZcReQRA08af1qU"
bucket = "data"
file_path = "test.mp4"

file_size = os.path.getsize(file_path)

url = f"{supaURL}/storage/v1/object/{bucket}/{file_path}"

multipart_encoder = MultipartEncoder(
    fields={
        'file': (os.path.basename(file_path), open(file_path, 'rb'), 'video/mp4')
    }
)

monitor = MultipartEncoderMonitor(multipart_encoder, lambda monitor: print(
    f"Upload progress: {monitor.bytes_read} / {file_size} bytes uploaded"))

headers = {
    'Authorization': f'Bearer {key}',
    'Content-Type': monitor.content_type
}

response = requests.post(url, data=monitor, headers=headers)

if response.status_code == 200:
    print("Upload successful.")
else:
    print(f"Upload failed with status code: {response.status_code}")
    print(response.text)
