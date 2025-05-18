import os
import shutil
import re
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

def fix_static_paths(content, static_url):
    """Fix static file paths in the generated HTML."""
    # Replace Django's static paths with the correct GitHub Pages paths
    content = content.replace(
        f'href="{static_url}'.encode(),
        b'href="'
    ).replace(
        f'src="{static_url}'.encode(),
        b'src="'
    )
    return content

def generate_static_site(build_dir):
    """Generate static HTML files manually."""
    client = Client()
    
    # Add debug info
    print("Debug: Starting static site generation")
    print(f"Debug: ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
    print(f"Debug: DEBUG = {settings.DEBUG}")
    print(f"Debug: STATIC_URL = {settings.STATIC_URL}")
    
    # Ensure we have the right settings for static generation
    settings.ALLOWED_HOSTS = ['*']  # Allow any host during generation
    settings.DEBUG = False  # Ensure we're in production mode
    
    # Try multiple URL patterns
    urls_to_try = ['/', '', '/index.html']
    last_status_code = None
    last_response = None
    
    for url in urls_to_try:
        try:
            print(f"Debug: Trying URL: {url}")
            response = client.get(url, follow=True, HTTP_HOST='localhost')
            print(f"Debug: Response status code: {response.status_code}")
            
            if response.status_code == 200:
                content = fix_static_paths(response.content, settings.STATIC_URL)
                index_path = build_dir / 'index.html'
                index_path.write_bytes(content)
                print(f"Generated {index_path}")
                return
            
            last_status_code = response.status_code
            last_response = response
            
            # Print redirect chain if any
            if response.redirect_chain:
                print("Debug: Redirect chain:", response.redirect_chain)
                
        except Exception as e:
            print(f"Debug: Error trying {url}: {str(e)}")
            continue
    
    # If we get here, all attempts failed
    error_msg = f"Failed to generate index.html: Last status code was {last_status_code}"
    if last_response and hasattr(last_response, 'redirect_chain'):
        error_msg += f"\nRedirect chain: {last_response.redirect_chain}"
    raise Exception(error_msg)

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