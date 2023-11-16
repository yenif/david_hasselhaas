import requests
import os

# Save PNG files to a local directory
def save_png_file(file_url, local_dir):
    response = requests.get(file_url)
    file_name = file_url.split('/')[-1]
    file_path = os.path.join(local_dir, file_name)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    print(f"Saved PNG file to {file_path}")

# Function to handle the recursive download of files
def download_files_recursively(api_url, local_dir, concatenated_content=""):
    response = requests.get(api_url)
    content_items = response.json()

    for item in content_items:
        if item['type'] == 'file' and item['name'].endswith('.md'):
            # Download Markdown file content
            file_response = requests.get(item['download_url'])
            concatenated_content += f"File: {item['download_url']}\n{file_response.text}\n\n"
        elif item['type'] == 'file' and item['name'].endswith('.png'):
            # Save PNG files
            save_png_file(item['download_url'], local_dir)
        elif item['type'] == 'dir':
            # Recursively download the contents of the directory
            concatenated_content = download_files_recursively(item['url'], local_dir, concatenated_content)

    return concatenated_content

# GitHub API URL for the contents of the autogen/docs directory
GITHUB_API_URL = "https://api.github.com/repos/microsoft/autogen/contents/website/docs"
LOCAL_DIR = 'autogen_docs'

# Ensure the local directory exists
os.makedirs(LOCAL_DIR, exist_ok=True)

# Start the recursive download and concatenation process
docs_content = download_files_recursively(GITHUB_API_URL, LOCAL_DIR)

# Save the concatenated Markdown content to a file
concatenated_file_path = os.path.join(LOCAL_DIR, 'autogen_docs_concatenated.md')
with open(concatenated_file_path, 'w') as file:
    file.write(docs_content)

print(f"Markdown files recursively concatenated and saved to {concatenated_file_path}")

