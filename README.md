# Machine Learning for IWT Ship Traffic Analysis Object Detection vs AIS Data
## Description
The main goal of this research study is to look into how object detection algorithms could be used with video surveillance and satellite images to deal with problems caused by Automatic Identification System (AIS) data that overlaps or is faked in maritime settings. The first research question focuses on evaluating the accuracy and performance of the object detection algorithm in identifying and localizing ships in diverse maritime conditions and environments. By comparing the algorithm's results with ground-truth data, researchers seek to understand the algorithm's reliability in ship detection. The second research question delves into understanding the discrepancies and variations between the ship detections obtained through the object detection algorithm and the existing AIS data. This step involves quantifying and analyzing the differences to gain insights into potential instances of overlapping or spoofed AIS data. Finally, the third research question explores the potential benefits and challenges of integrating video surveillance and satellite-derived ship detections with the AIS data. The study aims to determine whether this integration can enhance the detection and identification of overlapping or spoofed AIS information while also considering the limitations and obstacles that may arise during the process. By addressing these research questions, the study aims to contribute to the development of more robust and reliable maritime monitoring systems and improve the overall safety and security of maritime operations.
This file will discuss steps to execute the code for object identification, the results of which would be compared with the existing AIS data to test for anomalies.

### Procedure
The steps from downloading the video to executing the code will be explained below
#### Step 1 - Downloading the Video
* To be able to download a video in the background, I started off creating an account in the [amazon webservers](https://aws.amazon.com/?nc2=h_lg)
    * A New instance is created with __Ubuntu__ as the Operating system and the other options such that they complement the free tier services
    * The key file is downloaded in the .ppk version to be able to access the server.
    * The security constraints are added as mentioned below ![Screenshot 2023-08-06 162458](https://github.com/SuryaaVadachennimalaiSelvaraj/-Machine-Learning-for-IWT-Ship-Traffic-Analysis-Object-Detection-vs.-AIS-Data-/assets/141555542/992c489a-ad3e-4d98-a4e5-f1dca0699a5c)
    * The instance is thus created 
* Accessing the AWS key
    * Open PuTTYgen which is also a part of the package with PuTTY
    * Click on the "Load" button and browse your existing AWS key file with a ".pem" extension.
    * PuTTYgen will automatically detect the key and display its details.
    * Click on the " Save private key" button to save the key in the PuTTY Private Key (PPK) format.
* PuTTY
    * Open the PuTTY configuration window
    * In the PuTTY Configuration window, go back to the "Session" category.
    * Enter the IP address or hostname of your AWS Ubuntu instance in the "Host Name (or IP address)" field.
    * To save this configuration for future use, enter a name for the session in the "Saved Sessions" field and click the 
    "Save" button.
    * With the key file loaded and the SSH connection settings configured, click the "Open" button in the PuTTY 
    configuration window.
* Setting up a VNC server:
    * PuTTY will establish an SSH connection to your AWS Ubuntu instance using the loaded key file.
    * First check if the packages are updated
      ```
      sudo apt update
      sudo apt upgrade
      ```
    * To install a desktop enviornment inorder to have a GUI interface.
      ```
      sudo apt install xfce4
      ```
    * Install VNC server software
      ```
      sudo apt install xfce4
      ```
    * Set-up the VNC server
      ```
      vncserver :1 -geometry 1280x720 -depth 24
      ```
      The :1 denotes the display number
    * Next step is setting up vnc password and confirming the same
    * Stop the VNC server
      ```
      vncserver -kill :1
      ```
    * Open the VNC Server settings in a text editor using  the following command
      ```
      nano ~/.vnc/xstartup
      ```
      Delete the existing text and replace it with the following
      ```
      #!/bin/bash
      xrdb $HOME/.Xresources
      startxfce4 &
      ```
      To save the text in the editor use the __ctrl+O__, then it prompts you to enter the file name. once that is confirmed, you exit the editor using the short cut __ctrl+X__.
    * Restart the VNC server
      ```
      vncserver :1 -geometry 1280x720 -depth 24
      ```

      Now you have completed the creation of the VNC server in PuTTY
* Accessing the GUI
    * Download the app of your choice. In this case, I have used __VNC Viewer__
    * Copy your Public __IPv4 DNS__ from the AWS  instance portal
    * The above is entered into the app, with an extension of the display number. In this case its __:1__
* Running the code to download the video
    * Open the terminal and run the follwing snippets, to be able to download the required dependencies and to be able            download the video successfully.
      ```
      sudo apt update
      ```
      ```
      sudo apt upgrade
      ```
      ```
      sudo apt install python3
      ```
      ``` 
      sudo apt install pip
      ```
      ```
      sudo python3 -m pip install -U yt-dlp
      ```
      ```
      sudo apt install ffmpeg
      ```
   * Run the following syntax to be able to see the available formats
      ```
      yt-dlp -F [URL...]
      ```
   * From the provided list choose the desired format and select the code
   * Run the follwing snippet to start the download,
     ```
     yt-dlp [code] [URL...]
     ```
#### Step 2 - Creating a Dataset
* This step is to create a dataset to be able to train the yolov5 model
* The dataset is created in [Roboflow] {https://roboflow.com/}
* You could also use the preexisting datasets under the universe tab
* Once you sign-up to Roboflow you'd be able to create a dataset by clicking the create new dataset option
* The first step is to upload the pictures of ships
    * The number of pictures directly influence the confidence level of the detections
    * Also to be considered is the number of classes you want to detect in the model (i.e. Ships, people)
* The next step is where roboflow assigns the uploaded images into the traning set, validation and the test sets.
* The next step is the annotation of the uploaded images where you have to identify the objects in the image and give it a class name(s).
* Database generation step provides you with the option of adding preprocessing and Augmentation steps to the dataset, to be able to train your model better.
    * I added the preprocessing steps of Auto-Orient and Static crop.
    * Augmentation - Noise, bounding shear and Exposure to help with the not so clear detections.
* Then by clicking generate, you have the dataset!
* You then copy the private key of the dataset, which would be used in the next step to import the database.

#### Step 3 - Training and Detection
* The Traning and the execution of the code is performed on google colab because it is a cloud-based Jupyter Notebook platform favored for its free access to GPUs and TPUs, requiring no local setup. It integrates common libraries, supports real-time collaboration, and connects to Google Drive. With Python support and educational resources, it's a powerful tool for data science and machine learning practice and learning. However, users should be aware of session timeouts and resource limitations for more complex tasks.
* You create an account on google colab and open a new colabarotary
* mount your google drive to be ablt to 
* To be able to train and run the model, the following dependencies are executed,
```
!git clone https://github.com/ultralytics/yolov5  # clone repo
%cd yolov5
%pip install -qr requirements.txt # install dependencies
%pip install -q roboflow

import torch
import os
from IPython.display import Image, clear_output  # to display images
```
* Next step would be install roboflow to be able to import the dataset 
  ```
  !pip install roboflow
  ```
   * importing the database
      ```
      [Private Key]
      ```
* Next step is training the Yolov5 model

  ```
  !python train.py --img 416 --batch 16 --epochs 150 --data          
  [path to .yaml file] --weights [path_to_pretrained_weights] --cache
  ```
   * Epochs could be altered based on the usage, a really high epochs would make the detections monotonous and would make       the model only detect the objects if it is only similar to the pictures uploaded.
   * Once the epochs are run, the weights file is generated using which the detection could be performed.

* Torchvision and opencv-python is downloaded 
  ```
  !pip install torch torchvision
  !pip install opencv-python-headless
   ```
* Ultralytics is downloaded
  ```
  !pip install ultralytics
   ```
* To be able to generate plots,
  ```
  !pip install matplotlib
  ```

* To run a detection, you use the syntax
  ```
  !python detect.py --weights [Path to the weights file (best.pt)] --img-size 640 --conf [Desired
  Confiednce threshold ] --source [Path to the video file]
  ```
* You can access the detected file in the runs part of the Yolov5 folder
    * Yolov5 &rarr; runs &rarr; detect &rarr; exp
      
#### Step 4 - Coding to detect, count and compare the data to the AIS data file
* This code will be attached as a python file and the explanation for the logic behind it would be explained as comments in the same.
