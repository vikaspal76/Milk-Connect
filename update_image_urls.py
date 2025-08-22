from Mainapp.models import *

for item in Costumer.objects.all():
    if item.pic:
        # Convert local path to Cloudinary URL
        relative_path = str(item.pic).replace("\\", "/").lstrip("media/").strip()
        public_id = relative_path.rsplit(".", 1)[0]  # remove extension
        # Use the correct Cloudinary URL (extension must match actual file)
        item.pic = f"https://res.cloudinary.com/dsanolt1o/image/upload/{public_id}.jpg"
        item.save()
