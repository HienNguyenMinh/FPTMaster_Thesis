import os
os.environ["TF_ENABLE_ONEDNN_OPTS"]="0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import tensorflow as tf
from PIL import Image
from keras.models import load_model
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for


# number of classification classes
numclasses = 10

# Get the current working directory
current_directory = os.getcwd()

# Get the absolute path to the file
file_path = os.path.abspath(current_directory + "/AI_models/VGG16CheckPt_Model.hdf5")
if os.path.exists(file_path):
    # Load the trained Machine Learning model
    vgg16_model = load_model(file_path)
else:
    print(f"Error: File not found at {file_path}")

# Get the absolute path to the file
file_path = os.path.abspath(current_directory + "/AI_models/VGG19CheckPt_Model.hdf5")
if os.path.exists(file_path):
    # Load the trained Machine Learning model
    vgg19_model = load_model(file_path)
else:
    print(f"Error: File not found at {file_path}")

# Get the absolute path to the file
file_path = os.path.abspath(current_directory + "/AI_models/InceptionV3_Model.hdf5")
if os.path.exists(file_path):
    # Load the trained Machine Learning model
    inception_model = load_model(file_path) 
else:
    print(f"Error: File not found at {file_path}")

#Create flask app
app = Flask(__name__,template_folder='template')
app.secret_key = 'Hair_Disease5324'  # Change this to a long, random string

#Running the app sends us to diagnostic.html
@app.route("/")
def Home():
    return render_template("diagnostic.html")


@app.route("/uploadImages", methods=["Post"])
# Processing image from uploaded images
def uploadImages():
    file_info_list = []

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'myfiles[]' not in request.files:
            return render_template('diagnostic.html', error='No file part')

        files = request.files.getlist('myfiles[]')

        # Check if files are selected
        if not files:
            return render_template('diagnostic.html', error='No selected files')

        # Save each file to the 'uploads' folder in the static directory
        upload_folder = 'static/uploads'
        os.makedirs(upload_folder, exist_ok=True)

        
        for file in files:
            if file.filename:
                file_path = os.path.join(upload_folder, file.filename)
                file.save(file_path)

                # Resize the image using PIL (Python Imaging Library)
                resized_path = os.path.join(upload_folder, 'resized_' + file.filename)
                resizeImage(file_path, resized_path)


                # Placeholder for prediction result (replace with your actual prediction logic)
                prediction_result_VGG16 = predictImage(resized_path, vgg16_model)
                prediction_result_VGG19 = predictImage(resized_path, vgg19_model)
                prediction_result_inception = predictImage(resized_path, inception_model)

                file_info_list.append({
                    'file_path': resized_path,
                    'prediction_result_VGG16': prediction_result_VGG16,
                    'prediction_result_VGG19': prediction_result_VGG19,
                    'prediction_result_inception': prediction_result_inception
                })


    # Render the template and pass the file paths to display the images
    return render_template('diagnostic.html', file_info_list=file_info_list)


# Resize image to a target size
def resizeImage(input_path, output_path, target_size=(224, 224)):
    img = Image.open(input_path)
    img.thumbnail(target_size)
    img.save(output_path)

# AI model predicts from an input image path
def predictImage(file_path, model):
    # img = image.load_img(file_path, target_size=(224, 224))
    # img_array = image.img_to_array(img)
    image = Image.open(file_path)
    image = image.resize((224, 224))
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255

    # model predict an image
    prediction = model.predict(img_array)
    # decode the prediciton to get the highest probability
    max_probabilitiesIndex = np.argmax(prediction)
    probability = np.round(prediction[0][max_probabilitiesIndex]*100,2)

    threshold = 0.5
    # list of hair diseases name
    li = ['Alopecia Areata', 'Contact Dermatitis', 'Folliculitis', 'Head Lice', 'Lichen Planus',
          'Male Pattern Baldness', 'Psoriasis', 'Seborrheic Dermatitis', 'Telogen Effluvium', 'Tinea Capitis']
    # If probability >= thredhold, return the prediction result of the highest probability
    # Else: return class_name = "Non-Hair Disease" and probability = 0
    if probability >= threshold:
        class_name = li[max_probabilitiesIndex]
    else:
        class_name = "Non-Hair Disease"
        probability = 0

    return {'class_name': class_name, 'probability': probability}


@app.route("/saveImage", methods=["Post"])
# Processing image from uploaded images
def saveImage():
    imagePath = request.form.get('file-path')
    diseaseName = request.form.get('conclusion-input')
    patientID = request.form.get('patient-ID')
    

    if imagePath and diseaseName and patientID:
        # Save image into download_folder
        download_folder = 'c:\DiagnosticDownImages'
        os.makedirs(download_folder, exist_ok=True)

        # Trim whitespace for string 
        diseaseName = diseaseName.strip()
        patientID = patientID.strip()

        img = Image.open(imagePath)             
        img.save(os.path.join(download_folder,f'{patientID}_' f'{diseaseName}.jpg'))   
        # Show message 
        return jsonify({'success': True})
        
    else:
        # Show message 
        return jsonify({'success': False, 'error': 'Conclusion or Patient ID is missing'})
    


@app.route('/saveAll', methods=['POST'])
def saveAll():
    data = request.get_json()

    for form_data in data:
        imagePath = form_data['file-path']
        conclusion = form_data['conclusion-input']
        patientID = form_data['patient-ID']

        # Save image into download_folder
        download_folder = 'c:\DiagnosticDownImages'
        os.makedirs(download_folder, exist_ok=True)

        # Trim whitespace for string 
        conclusion = conclusion.strip()
        patientID = patientID.strip()

        img = Image.open(imagePath)             
        img.save(os.path.join(download_folder,f'{patientID}_' f'{conclusion}.jpg'))         

    return jsonify({'message': 'Save All successful!'})

if __name__ == "__main__":
    app.run()



