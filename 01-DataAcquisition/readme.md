This folder contains the data acquisition program--standalone\front\side\sideLow\back

IDE：Qt Creator 4.6.2 Based on Qt 5.9.6 (MSVC 2015, 32 bit) 

Kit:MSVC 2015 64bit

## interface.png
the interface of program.
##  DLL.rar
the dynamically linked library required for program operation. Decompress to this folder. Copy to the corresponding folder after the program is built.

![dll](https://user-images.githubusercontent.com/92310945/146881176-5fa548b9-4a85-4e0b-97d1-5912cc4d4709.png)

"common DLL" is required for both versions Debug and Release.

"Debug DLL" is required for version Debug.

"Release DLL" is required for version Release.
## 3rdparty.rar
the 3rdparty required for program operation, including "Azure Kinect SDK" and "OpenCV(3.4.1)". Only decompress to this folder. 
## FMS_data_acquisition_standalone
the program can run independently.
## FMS_data_acquisition_front
the program is the master program.
## FMS_data_acquisition_side
the program is the subordinate1 program. 
## FMS_data_acquisition_sideLow
the program is the subordinate2 program. 
## FMS_data_acquisition_back
the program is the subordinate3 program. 

![dll](https://docs.microsoft.com/en-us/azure/kinect-dk/media/multicam-sync-daisychain.png)

More information about the master and subordinate programs refer to the Azure Kinect documentation website (https://docs.microsoft.com/en-us/azure/kinect-dk/multi-camera-sync).
