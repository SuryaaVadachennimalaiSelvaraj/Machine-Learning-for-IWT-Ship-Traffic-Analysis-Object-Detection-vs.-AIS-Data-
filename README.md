# Machine Learning for IWT Ship Traffic Analysis Object Detection vs AIS Data
## Description
The main goal of this research study is to look into how object detection algorithms could be used with video surveillance to deal with problems caused by Automatic Identification System (AIS) data that overlaps or is spoofed in maritime settings. The first step in this project was acquiring the videos for analysis, this was done using the AWS servers to simplify the process. Then the next step involved creating the dataset, for this process Roboflow was used. The execution of the project was carried on in Google Colabarotary, where the model is trained and the detections are tested. Then the algorithm to count and compare is created and 
This file will discuss steps to execute the code for object identification, the results of which would be compared with the existing AIS data to test for anomalies.

### Procedure
The steps below will guide the user from installing the dependencies until running the code,
#### Step 1 - Downloading the Video
* To be able to download a video in the background, You start off by creating an account on the [Amazon Webservers](https://aws.amazon.com/?nc2=h_lg)
    * A New instance is created with __Ubuntu__ as the Operating system and the other options such that they complement the free tier services.
    * The key file is downloaded in the .ppk 
version to be able to access the server.
    * The security constraints:
        * These security conditions or constraints are important and depend on the intended use of the web servers.
        * For our use, the constraints are set up when creating the instance or could be adjusted once the instance is created by accessing the "Actions ➡️ Security groups" in the instance console.
        * The Following constraints are added:   
    ![Screenshot 2023-08-06 162458](https://github.com/SuryaaVadachennimalaiSelvaraj/Machine-Learning-for-IWT-Ship-Traffic-Analysis-Object-Detection-vs.-AIS-Data-/assets/141555542/1f33ca0c-c9f5-4c5c-8286-098f8a25b4e4)    
     ![Screenshot 2023-08-15 120253](https://github.com/SuryaaVadachennimalaiSelvaraj/Machine-Learning-for-IWT-Ship-Traffic-Analysis-Object-Detection-vs.-AIS-Data-/assets/141555542/f849aeb2-4ed6-4a5e-8317-c11e6788ec2d)
    * The instance is thus created. 
* Accessing the AWS key
    * Open PuTTYgen, which is also a part of the package with [PuTTY](https://www.putty.org/).
    * Click on the "Load" button and browse your existing AWS key file with a ".pem/.ppk" extension.
    * PuTTYgen will automatically detect the key and display its details.
    * Click on the " Save private key" button to save the key in the PuTTY Private Key (PPK) format.
* PuTTY
    * Open the PuTTY configuration window.
    * Navigate to "Connection ➡️ SSH ➡️ Auth".
    * Click on the "Browse" button next to "Private key file for authentication" and select the PPK file you created in the previous step.
    * In the PuTTY Configuration window, go back to the "Session" category.
    * Enter the IP address or hostname of your AWS Ubuntu instance in the "Host Name (or IP address)" field.
    * To save this configuration for future use, enter a name for the session in the "Saved Sessions" field and click the 
    "Save" button.
    * With the key file loaded and the SSH connection settings configured, click the "Open" button in the PuTTY 
    configuration window.
* Setting up a VNC server:
    * PuTTY will establish an SSH connection to your AWS Ubuntu instance using the loaded key file.
    * First check if the packages are updated using the following block,
      ```
      sudo apt update
      sudo apt upgrade
      ```
    * To install a desktop environment in order to have a GUI interface,
      ```
      sudo apt install xfce4
      ```
    * Install VNC server software.
      ```
      sudo apt install tigervnc-standalone-server
      ```
    * Set up the VNC server.
      ```
      vncserver :1 -geometry 1280x720 -depth 24
      ```
      The (:1) denotes the display number of the server 
    * Next step is setting up the VNC password and confirming the same.
    * Stop the VNC server.
      ```
      vncserver -kill :1
      ```
    * Open the VNC Server settings in a text editor using  the following command:
      ```
      nano ~/.vnc/xstartup
      ```
      Delete the existing text and replace it with the following:
      ```
      #!/bin/bash
      xrdb $HOME/.Xresources
      startxfce4 &
      ```
      To save the text in the editor use the __ctrl+O__, which prompts you to enter the file name. Once that is confirmed, you exit the editor using the shortcut __ctrl+X__.
    * Restart the VNC server
      ```
      vncserver :1 -geometry 1280x720 -depth 24
      ```

      Now you have completed the creation of the VNC server in PuTTY.
* Accessing the GUI
    * __The Following Process could also be done in the PuTTY, the following step is additional to create an interface for the webserver__. 
    * Download the app of your choice. In this case, I have used [VNC Viewer](https://downloads.realvnc.com/download/file/viewer.files/VNC-Viewer-7.6.0-Windows.exe).
    * Copy your Public __IPv4 DNS__ from the AWS  instance portal.
    * The above is entered into the app, with an extension of the display number. In this case, it is __:1__.
* Running the code to download the video
    * Open the terminal and run the following snippets, to download the required dependencies and to download the video successfully.
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
   * Run the following syntax to be able to see the available formats:
      ```
      yt-dlp -F [URL...]
      ```
   * From the provided list choose the desired format and select the code.
   * Run the following snippet to start the download:
     ```
     yt-dlp [code] [URL...]
     ```
* Accessing the Video
    * Download the WinSCP application.
    * Once it's set up, open the application and load the private key of the AWS server.
    * Once logged in, the two panes show the folders from your computer and the files from the web servers.
    * Here, you can copy the files to your computer.      
#### Step 2 - Creating a Dataset
* This step is to create a dataset to be able to train the yolov5 model.
* The dataset is created in [Roboflow] {https://roboflow.com/}.
* You could also use the preexisting datasets under the universe tab.
* Once you sign-up to Roboflow you'd be able to create a dataset by clicking the create new dataset option.
* The first step is to upload pictures of ships.
    * The number of pictures directly influences the confidence level of the detection.
    * Also to be considered is the number of classes you want to detect in the model (i.e. Ships, people).
* The next step is where Roboflow assigns the uploaded images to the training set, validation and test sets.
* The next step is the annotation of the uploaded images where you have to identify the objects in the image and give it a class name(s).
* Database generation step provides you with the option of adding preprocessing and Augmentation steps to the dataset, to be able to train your model better.
    * I added the preprocessing steps of Auto-Orient and Static crop.
    * Augmentation: Noise, bounding shear and Exposure to help with the not-so-clear detections.
* Then by clicking generate, you have the dataset!
* You then copy the private key of the dataset, which would be used in the next step to import the database.


**_NOTE:_** 
* The Dataset that was used for the said project is also attached to the Repository.
    * The test, train and validation files consist of images, which are distinguished to yield better results with the model.
    * The data.yaml file is a key file where you provide the path to the above three image files and the path of this data.yaml file is then added to the train command.

#### Step 3 - Training and Detection
* The training and the execution of the code are performed on google collab because it is a cloud-based Jupyter Notebook platform favoured for its free access to GPUs and TPUs, requiring no local setup. It integrates common libraries, supports real-time collaboration, and connects to Google Drive. With Python support and educational resources, it's a powerful tool for data science and machine learning practice and learning. However, users should be aware of session timeouts and resource limitations for more complex tasks.
* You create an account on Google Colab and open a new colabarotary.
* Mount your google drive to be able to train and run the model, the following dependencies are executed:
   ```
   !git clone https://github.com/ultralytics/yolov5  
   %cd yolov5
   %pip install -qr requirements.txt # install dependencies
   %pip install -q roboflow
   
   import torch
   import os
   from IPython.display import Image, clear_output  # to display images
   ```
* The Next step would be to install Roboflow to be able to import the dataset. 
  ```
  !pip install roboflow
  [Private Key to your dataset]
  ```
* Next step is training the Yolov5 model.

  ```
  !python train.py --img 416 --batch 16 --epochs 150 --data          
  [path to .yaml file] --weights [path_to_pretrained_weights] --cache
  ```
   * Epochs could be altered based on usage; a high epoch would make the detections monotonous and would make          the model only detect objects that are similar to the pictures uploaded.
   * Once the epochs are run, the weights file is generated, using which the detection could be performed.

* Torchvision and opencv-python are downloaded. 
  ```
  !pip install torch torchvision
  !pip install opencv-python-headless
   ```
* Ultralytics is downloaded.
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
  Confidence threshold ] --source [Path to the video file]
  ```
* You can access the detected file in the runs part of the Yolov5 folder
    * Yolov5 ➡️ runs ➡️ detect ➡️ exp.
    * 
    
**_NOTE:_** 
* I have attached a copy of the google colab document in the repository as AIS_detection.ipynb
      
#### Step 4 - Coding to detect, count and compare the data to the AIS data
* This code will be attached as a Python file, and the explanation for the logic behind it will be explained as comments in the same.
* The Algorithm developed is attached under the name __Main.py__.

**_Note:_**
* The code for the above execution is present in Google Colab, and a copy of the same is attached in the repository as AIS_detection.ipynb.
