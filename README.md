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
    * 
