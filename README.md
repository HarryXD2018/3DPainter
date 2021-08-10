# 3D Painter

[简体中文](https://github.com/HarryXD2018/3DPainter/blob/master/README_CN.md)

A monocular 3D Painter based on Python, which can export as `ply` file. 

### Installation

Check installation [wiki](https://github.com/HarryXD2018/3DPainter/wiki/Installation) for more details. 

Powered by: 

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
- **Infinite canvas**

#### Interactions
While running the program, there will be 3 windows on the screen, 2d, 3d and full canvas real time results respectively. The 3d window is powered by `matplotlib` and it is only a 3d preview of the project. The final result is generated after exiting the program. 

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

##### Text (Signature)

You can add your signature with spider-man gesture in text mode. Signature will be asked at the beginning of execution.

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/Signature.png)

##### Move

In move mode, you can create or view any details in the canvas.  You need reach the move panel in the mode with your index finger. 

#### Frameworks

There are four bottoms in the `image` window:

**Switch**: The top left one is for switching the painter mode, you can click the button with your mouse, or point to it with your index finger. If you use your finger to switch, please note that the button will freeze for 5 seconds to make sure that your finger leave that area (to avoid swiching mode frequently). 

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/switch_mode.gif)

**Clear**: The top right one is for clearing the plot. It will clear up both 2D and 3D results. Just as the **Switch** button, you can click the button with your mouse, or point to it with your index finger. 

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/clear.gif)

**Save**: Save the `jpg` file of the current window. 

**Exit**: The button right one is for exiting the program **without saving your work**. This button can only be activated by clicking. The final 3d `ply` file will be saved if variable `GEN3D` is `True`. 

| Interaction | Mouse clicking     | Finger Pointing    |
| ----------- | ------------------ | ------------------ |
| Switch      | :heavy_check_mark: | :heavy_check_mark: |
| Clear       | :heavy_check_mark: | :heavy_check_mark: |
| Save        | :heavy_check_mark: | :x:                |
| Exit        | :heavy_check_mark: | :x:                |

#### Display options
There are 3 boolean variables: `opt.preview3d`, `opt.view3d` and `opt.export3d` namely. They respectively in charge of:
- matplotlib 3d preview while running the program,
- the point cloud result after running,
- if the point cloud result export to `ply` file. 

You can view the file by running `view3d.py`. (Please change the file name)

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/3dresult.png)

### API Introduction

Please checkout repo's [wiki](https://github.com/HarryXD2018/3DPainter/wiki/Document). 

### New Features

[2021/07/27]

- Add dot, line and cuboid mode. 
- Synchronize the brush color in 2d and 3d display window

[2021/07/28]

- I just add the 3d point cloud function, you can now output the result in `.ply` file!

[2021/07/29]

- You can add your signature in text mode!

[2021/08/05]

- Infinite canvas! Try in `move` mode!

### TODO

- [x] Save button
- [x] Switch color in 3d mode
- [x] More painting modes
- [ ] Usage demo
- [x] Save 3d results