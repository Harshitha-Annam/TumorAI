from django.shortcuts import render
from .forms import ImageUploadForm
import numpy as np
from django.shortcuts import render
from .forms import ImageUploadForm
from .models import ImageUpload
from PIL import Image
import tensorflow as tf

model = tf.keras.models.load_model('models/tumormodel1.keras')
class_labels = ['pituitary', 'glioma','meningioma', 'notumor']
def preprocess_image(image_path):
    # Open the image using PIL
    img = Image.open(image_path)
    
    # Preprocess the image (Resize, normalize, etc.)
    img = img.resize((128, 128))  # Resize to match your model's input size
    img_array = np.array(img) / 255.0  # Normalize pixel values
    
    # Add batch dimension: (1, 224, 224, 3) for a single image
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array


def home_view(request):
    if request.method == 'POST' and request.FILES:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_path = uploaded_image.image.path

            processed_image = preprocess_image(image_path)

            prediction = model.predict(processed_image)

            predicted_class = np.argmax(prediction, axis = 1)
            print(prediction)
            print(predicted_class)
            result_class = str(predicted_class)[1]
            result_class = class_labels[int(result_class)]
            print(result_class)
            return render(request, 'baseapp/home.html', {'form':form, 'prediction': predicted_class, 'uploaded_image': uploaded_image , 'result_class':result_class})
    else:
        form = ImageUploadForm()

    return render(request, 'baseapp/home.html', {'form': form})


def about_view(request):
    return render(request, 'baseapp/about.html')