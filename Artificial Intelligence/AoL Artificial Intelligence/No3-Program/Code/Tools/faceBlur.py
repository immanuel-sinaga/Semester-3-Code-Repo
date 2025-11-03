import cv2
import os

def blur_faces(input_folder, output_folder):
    # Load the pre-trained Haar cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each image in the input folder
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        
        # Only process files with supported image extensions
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Read the image
            img = cv2.imread(file_path)

            # Convert to grayscale for face detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect faces in the image
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0:
                # Blur the faces detected in the image
                for (x, y, w, h) in faces:
                    face = img[y:y+h, x:x+w]
                    face = cv2.GaussianBlur(face, (99, 99), 30)  # Adjust the blur intensity
                    img[y:y+h, x:x+w] = face

                print(f"Faces detected and blurred in {filename}")
            else:
                print(f"No faces detected in {filename}, passing through.")

            # Save the processed image to the output folder
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, img)

# Usage example
input_folder = 'images'  # Folder containing the images to process
output_folder = 'output_images'  # Folder where processed images will be saved

blur_faces(input_folder, output_folder)
