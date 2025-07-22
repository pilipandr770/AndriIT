import sys
import os
import shutil

# Path to the blog.py file
blog_file_path = 'flask_shop/app/routes/blog.py'

# Create a backup of the original file
backup_file_path = 'flask_shop/app/routes/blog.py.bak'
shutil.copy2(blog_file_path, backup_file_path)
print(f"Created backup at {backup_file_path}")

# Read the content of the file
with open(blog_file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the OpenAI client initialization
new_content = content.replace(
    "client = OpenAI(api_key=current_app.config['OPENAI_API_KEY'])",
    "# Create client with only the required parameters\n        api_key = current_app.config['OPENAI_API_KEY']\n        client = OpenAI(api_key=api_key)"
)

# Write the modified content back to the file
with open(blog_file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated {blog_file_path}")
print("The OpenAI client initialization has been fixed.")