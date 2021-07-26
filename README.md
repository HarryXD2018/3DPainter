# 3D Painter

A monocular 3D Painter based on Python. 

### Installation

You need the following Python packages:

- matplotlib
- opencv-python
- mediapipe

*Please note that you need to download [hand landmark](https://github.com/google/mediapipe/tree/master/mediapipe/modules/hand_landmark) model that suits your PC and put it at the root folder.*

### Tutorials

3D Painter supports two painting modes, *brush* mode and *sphere* mode. You can choose 3D mode or only 2D mode. 

#### Interactions

##### Brush

| Function     | Hand Gesture                                                 |
| ------------ | ------------------------------------------------------------ |
| Brush        | Index ![finger](https://github.com/HarryXD2018/3DPainter/blob/master/demo/brush.gif) |
| Eraser       | Index and middle finger (2d mode only)![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/eraser.gif) |
| Switch color | Spider-man gesture (choose a color randomly, 2d mode only)![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/color.gif) |

##### Sphere

| Function      | Hand Gesture                                       |
| ------------- | -------------------------------------------------- |
| Choose center | Index finger                                       |
| Set radius    | The radius will increase during Spider-man gesture |

The sphere (circle) will be painted when you switch Spider-man gesture to index finger gesture. 

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/sphere.gif)

#### Frameworks

There are four bottoms in the `image` window:

**Switch**: The top left one is for switching the painter mode, you can click the bottom with your mouse, or point to it with your index finger. If you use your finger to switch, please note that the bottom will freeze for 5 seconds to make sure that your finger leave that area (to avoid swiching mode frequently). 

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/switch_mode.gif)

**Clear**: The top right one is for clearing the plot. It will clear up both 2D and 3D results. Just as the **Switch** bottom, you can click the bottom with your mouse, or point to it with your index finger. 

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/clear.gif)

**Save**: Save the 2d painting work. (click only)

**Exit**: The bottom right one is for exiting the program **without saving your work**. This bottom can only be activated by clicking. 

| Interaction | Mouse clicking     | Finger Pointing    |
| ----------- | ------------------ | ------------------ |
| Switch      | :heavy_check_mark: | :heavy_check_mark: |
| Clear       | :heavy_check_mark: | :heavy_check_mark: |
| Save        | :heavy_check_mark: | :x:                |
| Exit        | :heavy_check_mark: | :x:                |

#### Activate/ deactivate 3D mode

Set varable `MODE3D` in  `3DPainter.py` to `False` will deactivate the 3d mode. 

### TODO

- [x] Save Bottom
- [ ] Switch color in 3d mode
- [ ] More painting modes