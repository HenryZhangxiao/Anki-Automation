## Introduction

A program to automatically create Anki flashcards from an image.

The inspiration for this project comes from the tiresome process of manually creating Anki flashcards, especially in batches.<br>
This program leverages Google Document AI to perform OCR on a given image.


[Watch a Demo here](https://www.youtube.com/watch?v=YgO4WUwoPPU)

![image](https://github.com/HenryZhangxiao/Anki-Automation/assets/44578113/fd07bdd5-9565-49f0-b1f1-7804f0831e34)
![image](https://github.com/HenryZhangxiao/Anki-Automation/assets/44578113/7e9b3da1-0651-41cb-b987-615a2357c0fe)
![image](https://github.com/HenryZhangxiao/Anki-Automation/assets/44578113/c215ae66-06cf-4a90-9ef0-53e00dbfa029)
<img src="https://github.com/HenryZhangxiao/Anki-Automation/assets/44578113/51160a12-f440-480b-9358-40097bec57dc" height="116">
![image](https://github.com/HenryZhangxiao/Anki-Automation/assets/44578113/31739e97-fcec-44a4-b08a-3f6110a8f991)
![image](https://github.com/HenryZhangxiao/Anki-Automation/assets/44578113/c297a8ee-040c-48ea-91cd-30f7baab15f5)


#### Table of Contents
- [Technologies Used ](#technologies)
- [How to Run ](#run)


<br></br>
## Technologies Used <a name="technologies"></a>
- Python3
- OpenCV
- NumPy
- scikit-image
- ipykernel
- genanki
- tkinter
- Matplotlib
- Google Document AI


<br></br>

## How to Run <a name="run"></a>
- Pre-requisites
  - python3
  - `pip install -r requirements.txt`
  - tkinter
    - For Windows: Should be included within your Python installation by default
    - For Ubuntu: sudo apt-get install python3-tk
    - For Fedora: sudo dnf install python3-tkinter
    - For MacOS: brew install python-tk
  - Google Cloud Credentials json file
    - You must open an issue
- To run
  - `python3 main.py`
  - Alternatively you can just run main.py in your code editor
  - This project also has a branch `exe`
    - /dist/main/main.exe can be run without downloading additional libraries
