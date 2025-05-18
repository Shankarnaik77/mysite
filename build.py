import os
import shutil
from pathlib import Path

def copy_static_files():
    # Create build directory
    build_dir = Path('build')
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()

    # Copy index.html to root
    shutil.copy2('mysite/templates/mysite/index.html', build_dir / 'index.html')

    # Copy static files
    static_src = Path('mysite/static/mysite')
    static_dest = build_dir
    shutil.copytree(static_src, static_dest / 'static')

    # Update paths in index.html to use relative paths
    index_path = build_dir / 'index.html'
    with open(index_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace Django static tags with relative paths
    content = content.replace("{% load static %}", "")
    content = content.replace("{% static 'mysite/", "/mysite/static/")
    content = content.replace("' %}", "")
    content = content.replace("{% csrf_token %}", "")

    with open(index_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print("Build completed successfully!")

if __name__ == '__main__':
    copy_static_files() 