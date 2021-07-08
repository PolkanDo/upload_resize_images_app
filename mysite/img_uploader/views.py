import requests

from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.images import get_image_dimensions
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse


from .models import Image

from .forms import NewImageForm, ResizeImageForm


def index(request):
    """Main page view"""
    images = Image.objects.order_by("-pk").all()
    return render(request, "index.html", {"images": images})


def get_remote_image(image_url):
    """The function allows you to access images, using a link"""
    memory = None
    image_name = ''

    try:
        request = requests.get(image_url, stream=True)
    except Exception:
        return None
    redirect("new")

    if request.status_code == 200:
        image_name = urlparse(image_url).path.split('/')[-1]
        image = Image.open(request.raw)
        buffer = BytesIO()

        if image.mode != "RGB":
            image = image.convert("RGB")

        image.thumbnail((image.width, image.height), Image.ANTIALIAS)
        image.save(buffer, format='JPEG')
        memory = InMemoryUploadedFile(buffer, None, image_name, 'image/jpeg',
                                      buffer.tell(), None)

    return {'im': memory, 'name': image_name}


def new_image_view(request):
    """New image upload view"""
    if request.method == "POST":
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            if (form.cleaned_data['imageFile'] and
                    not form.cleaned_data['imageName']):
                image = form.cleaned_data['imageFile']
                name = image.name
                width, height = get_image_dimensions(image)

            elif (form.cleaned_data['imageName']
                  and not form.cleaned_data['imageFile']):
                image = get_remote_image(form.cleaned_data['imageName'])
                if image is None:
                    error = "Invalid link"
                    return render(request, "new.html",
                                  {'form': form, 'error': error})
                image = image['im']
                name = image['name']
                width, height = get_image_dimensions(image['im'])

            else:
                error = "choose one way to upload the image "
                return render(request, "new.html",
                              {'form': form, 'error': error})

            result = Image.objects.create(image=image, name=name, width=width,
                                          height=height)
            return redirect("img_view", img_id=result.pk)

    else:
        form = NewImageForm()
    return render(request, "new.html", {'form': form})


def resize_image_view(request, image_pk):
    """View for resizing images"""
    image = get_object_or_404(Image, pk=image_pk)
    proportions = image.width / image.height
    image_size = f"{image.width} * {image.height}"

    form = ResizeImageForm(request.POST or None, instance=image)
    if request.method == "POST" and form.is_valid():
        new_size = form.save(commit=False)
        if form.cleaned_data['height'] and not form.cleaned_data['width']:
            new_size.width = form.cleaned_data['height'] * proportions
        else:
            new_size.height = form.cleaned_data['width'] / proportions
        new_size.save()
        return redirect("image_view", img_id=image.pk)

    context = {"form": form, "image": image, "image_size": image_size}
    return render(request, "image_view.html", context)
