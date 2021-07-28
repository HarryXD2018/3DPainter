# 3D Painter

A monocular 3D Painter based on Python. 

### Installation

You need the following Python packages:

- matplotlib
- opencv-python
- mediapipe
- open3d-python

Or run `pip install -r requirements.txt` in your command line. 

*Please note that you need to download [hand landmark](https://github.com/google/mediapipe/tree/master/mediapipe/modules/hand_landmark) model that suits your PC and put it at the root folder.*

### Tutorials

Run

~~~ cmd
python 3DPainter.py
~~~

3D Painter supports following modes:

- Brush
- Sphere (Circle)
- Dot
- Cuboid

You can choose 3D mode or only 2D mode. 

#### Interactions

##### Brush

| Function     | Hand Gesture                                                 |
| ------------ | ------------------------------------------------------------ |
| Brush        | Index ![finger](https://github.com/HarryXD2018/3DPainter/blob/master/demo/brush.gif) |
| Eraser       | Index and middle finger (2d mode only)![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/eraser.gif) |
| Switch color | Spider-man gesture (choose a color randomly)![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/color.gif) |

##### Sphere

| Function      | Hand Gesture                                       |
| ------------- | -------------------------------------------------- |
| Choose center | Index finger                                       |
| Set radius    | The radius will increase during Spider-man gesture |

The sphere (circle) will be painted when you switch Spider-man gesture to index finger gesture. 

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/sphere.gif)

##### Dot

Dot function works just like sphere. 

##### Line 

Spider-man gesture to determine the location of each end of the line. Please wait for 2 seconds between ploting 2 lines. 

##### Cuboid

Similar to line. Two points are recorded as diagonal points. 

#### Frameworks

There are four bottoms in the `image` window:

**Switch**: The top left one is for switching the painter mode, you can click the bottom with your mouse, or point to it with your index finger. If you use your finger to switch, please note that the bottom will freeze for 5 seconds to make sure that your finger leave that area (to avoid swiching mode frequently). 

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/switch_mode.gif)

**Clear**: The top right one is for clearing the plot. It will clear up both 2D and 3D results. Just as the **Switch** bottom, you can click the bottom with your mouse, or point to it with your index finger. 

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/clear.gif)

**Save**: Save the `jpg` file of the current window. 

**Exit**: The bottom right one is for exiting the program **without saving your work**. This bottom can only be activated by clicking. The final 3d `ply` file will be saved if variable `GEN3D` is `True`. 

| Interaction | Mouse clicking     | Finger Pointing    |
| ----------- | ------------------ | ------------------ |
| Switch      | :heavy_check_mark: | :heavy_check_mark: |
| Clear       | :heavy_check_mark: | :heavy_check_mark: |
| Save        | :heavy_check_mark: | :x:                |
| Exit        | :heavy_check_mark: | :x:                |

#### Activate/ deactivate 3D mode

Set variable `MODE3D` in  `3DPainter.py` to `False` will deactivate the syn 3d mode. 

#### Generate and View the ply File

Set variable `GEN3D` in  `3DPainter.py` to `True` will generate the 3d file in `ply` format. You can view the file by running `view3d.py`. (Please change the file name)

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/3dresult.png)

### API Introduction

Please checkout repo's [wiki](https://github.com/HarryXD2018/3DPainter/wiki/Document). 

### New Features

[2021/07/27]

- Add dot, line and cuboid mode. 
- Synchronize the brush color in 2d and 3d display window

[2021/07/28]

- I just add the 3d point cloud function, you can now output the result in `.ply` file!

### TODO

- [x] Save Bottom
- [x] Switch color in 3d mode
- [x] More painting modes
- [ ] Usage demo
- [x] Save 3d results