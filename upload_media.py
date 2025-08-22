import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MilkConnect.settings')
django.setup()

from Mainapp.models import Dairyimages

# Base Cloudinary URL
CLOUDINARY_BASE = "https://res.cloudinary.com/dsanolt1o/image/upload/"

for item in Dairyimages.objects.all():
    for field in ['pic1', 'pic2', 'pic3', 'pic4']:
        img = getattr(item, field)
        if img:
            # Extract relative path from local media folder
            # Example: "F:\RURAL\MilkConnect\Milk-Connect\media\dairy\image.png"
            relative_path = os.path.relpath(img.path, r"F:\RURAL\MilkConnect\Milk-Connect\media")
            relative_path = relative_path.replace("\\", "/")  # fix backslashes
            public_id = os.path.splitext(relative_path)[0]  # remove extension
            # Construct Cloudinary URL with .png extension
            cloud_url = f"{CLOUDINARY_BASE}{public_id}.png"
            # Update the field
            setattr(item, field, cloud_url)
    item.save()
    print(f"Updated Dairyimages id={item.id}")
