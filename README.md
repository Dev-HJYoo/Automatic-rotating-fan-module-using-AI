#  Automatic rotating fan module using AI
> if you have a fan and install the module, you will use Automatic rotating fan.


 This project is the 2019 1st Semester Converged Capstone Design Project. 

 We learned AI in the first semester of 2019. we thought to use AI. And, we thought it would be all right if we made a fan to follow people in the hot summer. so, we made Automatic rotating fan module using object detection.

![](Image/device.png)



[![Video Label](https://img.youtube.com/vi/eMBiMkDRgPI/0.jpg)]((https://youtu.be/eMBiMkDRgPI?t=0s) 



## Component

Device

- Raspberry pi 3B+
- Stepper Motor
- Touch Monitor
- Web cam
- PC

![](Image/Component.png)


## H/W

#### Outline Map
![](Image/Outline_map.jpg)

#### H/W Circuit

![](Image/H-W_circuit.png) 

#### 3D Model
![](Image/model.png)

![](Image/model2.png)




## S/W

#### Object Detection

we used SSD-MobileNet-V1 model because we used Raspberry Pi( single board ). 

#### Algorithm

![](Image/Algorithm.jpg)

#### Socket Transport

![](Image/Socket.jpg)




## Object Detection

#### Gather Data

using Capture/capture_from_webcam.py.

![](Image/Data.jpg)

#### Anotation

using [[3b.](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10#3b-label-pictures)]

![](Image/Anotation.png)



#### Training

using [[4.Generate training data ~7. Export inference Graph](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10#4-generate-training-data)]

![](Image/Training.png)





## How To Use?

See [[Object Detection](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10)] for preferences 

- Object_detection_webcam_server.py : Install PC
- Wifi.py : Installed Raspberry Pi



first, Run Object_detection_webcam_server.py.

second, Run Wifi.py.



## Team members

- 유형준(Yoo Hyeong Jun) - Software Development [[Github](https://github.com/cocopambag)] [jhdf1234@naver.com]

- 김진호(Kim Jin Ho) - 3D Modeling [[Github](https://github.com/hiptoo1)] [hiptoo1@naver.com]

- 이대건  - Hardware Development [longchim@naver.com]

- 이정훈 - Software Development [[Github](https://github.com/foonia)] [ljh9032a@naver.com]

- 전주하 - Paperwork [[Github](https://github.com/LetsBee)] [hwe1123@naver.com]

![](Image/Team.jpg)

## Reference Materials

- Object Detection - [[EdjeElectronics](https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10)]
- Socket Transport - [[brownbears](https://brownbears.tistory.com/207)]
- Motor Control - [[Chandong83](https://m.blog.naver.com/chandong83/221156273595)]
