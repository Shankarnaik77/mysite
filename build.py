import os
import shutil
from pathlib import Path
import django
from django.core.management import call_command
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def copy_static_files():
    script_dir = Path(__file__).parent.absolute()
    build_dir = script_dir / 'build'
    temp_static_dir = script_dir / 'temp_static'
    
    # Clean build directory if it exists
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()

    # Clean temp static directory if it exists
    if temp_static_dir.exists():
        shutil.rmtree(temp_static_dir)
    temp_static_dir.mkdir()

    # First, collect static files to a temporary directory
    print("Collecting static files...")
    settings.STATIC_ROOT = str(temp_static_dir)
    call_command('collectstatic', '--noinput', '--clear')

    # Then generate static site with django-distill
    print("Generating static site with django-distill...")
    call_command('distill-local', '--force', output_dir=str(build_dir))

    # Clean up temp directory
    shutil.rmtree(temp_static_dir)
    
    print("Build completed successfully!")
    print(f"Build directory: {build_dir}")
    print("Contents of build directory:")
    for path in build_dir.rglob('*'):
        print(f"  {path.relative_to(build_dir)}")

if __name__ == '__main__':
    copy_static_files() 