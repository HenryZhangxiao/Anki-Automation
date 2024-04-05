import os, io
import cv2
import json
import numpy as np # scientific computing
import pandas as pd
import matplotlib.pyplot as plt # plotting
import matplotlib.image as mpimg # reading images
from collections import deque
from skimage.color import rgb2gray # converting rgb images to grayscale

# Google Vision imports
from importlib.resources import path
from google.cloud import vision
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

# Google Document AI imports
from typing import Optional
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore
from google.cloud import documentai_v1

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'japaneseocr-1-8883b9dcab0a.json'


# Resizing function
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    return cv2.resize(image, dim, interpolation=inter)


# Sharpening functions

def sharpen(img):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]], np.float32)
    sharpened_image = cv2.filter2D(img, -1, kernel)
    return sharpened_image

def laplacian(img):
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]], np.float32) 
    sharpened_image = cv2.filter2D(img, -1, kernel)
    return sharpened_image

def same(img):
    kernel = np.array([[0, 0, 0],
                       [0, 1, 0],
                       [0, 0, 0]], np.float32) 
    img = cv2.filter2D(img, -1, kernel)
    return img


# Shifting functions

def shiftUp(img, percent):
    height, width = img.shape[:2]
    tx, ty = 0, -(height*percent/100)
    translation_matrix = np.array([[1, 0, tx],
                                    [0, 1, ty]
                                ], dtype=np.float32)
    translated_image = cv2.warpAffine(src=img, M=translation_matrix, dsize=(width, height))
    return translated_image

def shiftDown(img, percent):
    height, width = img.shape[:2]
    tx, ty = 0, (height*percent/100)
    translation_matrix = np.array([[1, 0, tx],
                                    [0, 1, ty]
                                ], dtype=np.float32)
    translated_image = cv2.warpAffine(src=img, M=translation_matrix, dsize=(width, height))
    return translated_image

def shiftLeft(img, percent):
    height, width = img.shape[:2]
    tx, ty = -(height*percent/100), -0
    translation_matrix = np.array([[1, 0, tx],
                                    [0, 1, ty]
                                ], dtype=np.float32)
    translated_image = cv2.warpAffine(src=img, M=translation_matrix, dsize=(width, height))
    return translated_image

def shiftRight(img, percent):
    height, width = img.shape[:2]
    tx, ty = (height*percent/100), 0
    translation_matrix = np.array([[1, 0, tx],
                                    [0, 1, ty]
                                ], dtype=np.float32)
    translated_image = cv2.warpAffine(src=img, M=translation_matrix, dsize=(width, height))
    return translated_image


# Cropping function
def crop_image(img, height_percent, width_percent):
    h1, h2 = height_percent
    w1, w2 = width_percent
    height, width = img.shape[:2]
    cropped_image = img[int(height*h1/100):int(height*h2/100), int(width*w1/100):int(width*w2/100)]
    return cropped_image


# Format Anki function
# Data comes in in json format which is obtained from running Google Document AI
def format_anki(data):
    cards = []
    kana, kanji, jap_sen, eng_trans, eng_ex_sen = deque(), deque(), deque(), deque(), deque()
    for obj in data:
        #Add the text and relevant metadata to respective arrays
        match obj["type"]:
            case "English":
                d = {
                    "text": obj["mentionText"],
                    "bounding": obj["pageAnchor"]["pageRefs"][0]["boundingPoly"]["normalizedVertices"]
                }
                eng_trans.append(d)

            case "Kana":
                d = {
                    "text": obj["mentionText"],
                }
                kana.append(d)

            case "Kanji":
                d = {
                    "text": obj["mentionText"],
                    "bounding": obj["pageAnchor"]["pageRefs"][0]["boundingPoly"]["normalizedVertices"]
                }
                kanji.append(d)

            case "Sentence_English":
                d = {
                    "text": obj["mentionText"],
                }
                eng_ex_sen.append(d)

            case "Sentence_Japanese":
                d = {
                    "text": obj["mentionText"],
                }
                jap_sen.append(d)

    # Create the fields of the anki card
    while kana:
        kanaAdd = kana.popleft()['text']
        if kanji[0]['bounding'][0]['y'] < eng_trans[0]['bounding'][0]['y']:
            kanjiAdd = kanji.popleft()['text']
        else:
            kanjiAdd = ''
        japAdd = jap_sen.popleft()['text']
        engTransAdd = eng_trans.popleft()['text']
        engExSenAdd = eng_ex_sen.popleft()['text'].replace('\n', ' ')

        card = [
            kanaAdd,
            kanjiAdd,
            japAdd,
            engTransAdd,
            engExSenAdd
        ]
        cards.append(card)

    return cards


# Google Cloud Vision
def google_cloud_vision(filepath):
    client = vision.ImageAnnotatorClient()

    def detectText(img):
        with io.open(img, 'rb') as image_file:
            content = image_file.read()

        image = vision_v1.types.Image(content = content)
        response = client.text_detection(image = image)
        texts = response.text_annotations
        print("Texts:")

        df = pd.DataFrame(columns = ['locale', 'description'])
        
    #    for text in texts:
    #        df = df._append(
    #            dict(
    #                local = text.locale,
    #                description = text.description
    #            ),
    #            ignore_index = True
    #        )
    #    return df
        
        for text in texts:
            print(f'\n"{text.description}"')

            vertices = [
                f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
            ]

            print("bounds: {}".format(",".join(vertices)))

        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )

   # FILE_NAME = 'images/test_image1.jpg'
    FILE_NAME = filepath
    FOLDER_PATH = r'./'

    print(detectText(FILE_NAME))


# Google Document AI
def google_document_ai(filepath):
    # TODO(developer): Uncomment these variables before running the sample.
    project_id = "japaneseocr-1"
    location = "us" # Format is "us" or "eu"
    processor_id = "eaf216b404f6b455" # Create processor before running sample
   # file_path = "images/test_image3.jpg"
    file_path = filepath
    # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
    file_extension = filepath.rsplit('.', 1)[1]
    match file_extension:
            case "pdf":
                mime_type = "application/pdf"
            case "jpg" | "jpeg":
                mime_type = "image/jpeg"
            case "png":
                mime_type = "image/png"
            case _:
                mime_type = "image/jpeg"
            
    field_mask = "text,entities"  #,pages.pageNumber"  # Optional. The fields to return in the Document object.
    # processor_version_id = "YOUR_PROCESSOR_VERSION_ID" # Optional. Processor version to use
    process_data = True

    def process_document_sample(
        project_id: str,
        location: str,
        processor_id: str,
        file_path: str,
        mime_type: str,
        field_mask: Optional[str] = None,
        processor_version_id: Optional[str] = None,
    ) -> None:
        # You must set the `api_endpoint` if you use a location other than "us".
        opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

        client = documentai.DocumentProcessorServiceClient(client_options=opts)

        if processor_version_id:
            # The full resource name of the processor version, e.g.:
            # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
            name = client.processor_version_path(
                project_id, location, processor_id, processor_version_id
            )
        else:
            # The full resource name of the processor, e.g.:
            # `projects/{project_id}/locations/{location}/processors/{processor_id}`
            name = client.processor_path(project_id, location, processor_id)

        # Read the file into memory
        with open(file_path, "rb") as image:
            image_content = image.read()

        # Load binary data
        raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

        # For more information: https://cloud.google.com/document-ai/docs/reference/rest/v1/ProcessOptions
        # Optional: Additional configurations for processing.
        process_options = documentai.ProcessOptions(
            # Process only specific pages
            individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
                pages=[1]
            )
        )

        # Configure the process request
        request = documentai.ProcessRequest(
            name=name,
            raw_document=raw_document,
            field_mask=field_mask,
            process_options=process_options,
        )

        result = client.process_document(request=request)

        # For a full list of `Document` object attributes, reference this page:
        # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
        document = result.document

        # Read the text recognition output from the processor
    #    print("The document contains the following text:")
    #    print(document.text)
        
        # Write document to data.json
        json_string = documentai_v1.Document.to_json(document)
        dict_obj = json.loads(json_string)

        if process_data:
            filtered_data = []
        #   filtered_data["text"] = (dict_obj["text"])   # Uncomment if you want the first line of the json to contain all the text
            for e in dict_obj["entities"]:
                data = {
                    "type": e["type"],
                    "mentionText": e["mentionText"],
                    "pageAnchor": e["pageAnchor"],
                    "id": e["id"],
                }
                filtered_data.append(data)
                
            final_data = format_anki(filtered_data)
                
            with open("data.json", mode='w') as my_file:
                json.dump(final_data, my_file)
        else:
            with open("data.json", mode='w') as my_file:
                json.dump(dict_obj, my_file)

    process_document_sample(
        project_id,
        location,
        processor_id,
        file_path,
        mime_type,
        field_mask
    )
