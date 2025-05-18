import os
import requests
from urllib.parse import urlparse

def download_image(url, filename):
    """Download an image from a URL and save it to the specified filename."""
    try:
        # Add Unsplash API parameters for proper attribution
        parsed_url = urlparse(url)
        if 'unsplash.com' in parsed_url.netloc:
            url = f"{url}?ixid=travel-website&ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80"
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Save the image
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")
        return False

def main():
    # Define the image directory
    image_dir = 'mysite/static/mysite/images'
    
    # Dictionary of images to download
    images = {
        'hero-bg.jpg': 'https://images.unsplash.com/photo-1469474968028-56623f02e42e',
        'bali.jpg': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4',
        'santorini.jpg': 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e',
        'machu-picchu.jpg': 'https://images.unsplash.com/photo-1587595431973-160d0d94add1',
        'gallery1.jpg': 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd',
        'gallery2.jpg': 'https://images.unsplash.com/photo-1535530992830-e25d07cfa780',
        'gallery3.jpg': 'https://images.unsplash.com/photo-1523906834658-6e24ef2386f9',
        'gallery4.jpg': 'https://images.unsplash.com/photo-1516483638261-f4dbaf036963',
        'gallery5.jpg': 'https://images.unsplash.com/photo-1533105079780-92b9be482077',
        'gallery6.jpg': 'https://images.unsplash.com/photo-1492693429561-1c283eb1b2e8'
    }
    
    # Download each image
    for filename, url in images.items():
        filepath = os.path.join(image_dir, filename)
        download_image(url, filepath)

if __name__ == '__main__':
    main()
    print("Image download process completed!") 