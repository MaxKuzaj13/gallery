from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from . import models


def preview_image(request, index):
    # Get the gallery image object by index
    gallery_image = get_object_or_404(models.GalleryImage, index=index)

    # If there's no image uploaded for this index, return a 404 response
    if not gallery_image.image:
        return HttpResponse("No image uploaded for this index.", status=404)

    # Open the image from the file path
    image_path = gallery_image.image.path
    image = Image.open(image_path)

    # Create a thumbnail with a size of 200x200 pixels
    image.thumbnail((200, 200))

    # Save the thumbnail to memory (not to disk)
    thumb_io = BytesIO()
    image.save(thumb_io, format='JPEG')
    thumb_io.seek(0)

    # Create an InMemoryUploadedFile from the thumbnail in memory
    thumbnail_image = InMemoryUploadedFile(
        thumb_io, None, 'thumb_200x200.jpg', 'image/jpeg', thumb_io.tell(), None
    )

    # Generate the response with the image directly in the browser
    response = HttpResponse(content_type='image/jpeg')
    response['Content-Disposition'] = 'inline; filename="thumb_200x200.jpg"'

    # Write the thumbnail to the response to send it directly to the browser
    response.write(thumb_io.getvalue())
    return response


@csrf_exempt
def gallery_image(request, index):
    if request.method == 'GET':
        # Retrieve the current image for the given index
        gallery_image = get_object_or_404(models.GalleryImage, index=index)
        image_url = gallery_image.image.url

        return JsonResponse({'image_url': image_url})

    elif request.method == 'POST':
        # Update or create an image for the given index
        image_file = request.FILES.get('image')  # Assuming the image is sent in the request

        gallery_image, created = models.GalleryImage.objects.update_or_create(
            index=index,
            defaults={'image': image_file}
        )

        return JsonResponse({'message': 'Image updated successfully'})
