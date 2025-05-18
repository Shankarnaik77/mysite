import os
import shutil
from pathlib import Path
import django
from django.core.management import call_command
from django.conf import settings
from django.test import Client
from django.urls import reverse

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
os.environ.setdefault('DJANGO_SETTINGS_SKIP_LOCAL', 'True')
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
django.setup()

def generate_static_site(build_dir):
    """Generate static HTML files manually."""
    client = Client()
    
    # Try both with and without trailing slash
    for url in ['/', '']:
        response = client.get(url)
        if response.status_code == 200:
            index_path = build_dir / 'index.html'
            index_path.write_bytes(response.content)
            print(f"Generated {index_path}")
            return
    
    # If we get here, both attempts failed
    raise Exception(f"Failed to generate index.html: Last status code was {response.status_code}")

def copy_static_files():
    build_dir = Path(settings.BUILD_DIR)
    temp_static_dir = Path(settings.BASE_DIR) / 'temp_static'
    
    # Clean directories
    for dir_path in [build_dir, temp_static_dir]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
        dir_path.mkdir(parents=True)

    # First, collect static files
    print("Collecting static files...")
    settings.STATIC_ROOT = str(temp_static_dir)
    call_command('collectstatic', '--noinput', '--clear', verbosity=0)

    # Generate static site
    print("Generating static site...")
    generate_static_site(build_dir)

    # Copy static files
    print("Copying static files...")
    static_build_dir = build_dir / 'static'
    if not static_build_dir.exists():
        static_build_dir.mkdir(parents=True)
    
    # Copy all static files
    for item in temp_static_dir.iterdir():
        dest_path = static_build_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest_path, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest_path)

    # Clean up
    shutil.rmtree(temp_static_dir)
    
    print("Build completed successfully!")
    print(f"Build directory: {build_dir}")
    print("\nContents of build directory:")
    for path in build_dir.rglob('*'):
        if path.is_file():
            print(f"  {path.relative_to(build_dir)}")

if __name__ == '__main__':
    copy_static_files() 