# 3D Painter

3D Painter是基于计算机单目摄像头的三维画图软件，它有着基础画图软件的全部功能，并且可以导出为`ply`文件。

### 安装

1. 在命令控制行运行 `pip install -r requirements.txt` 。
2. 根据计算机硬件选择下载相应的[手部特征点](https://github.com/google/mediapipe/tree/master/mediapipe/modules/hand_landmark)文件，并放置在项目文件夹中。

### 教程

运行`python 3DPainter.py`


目前3D Painter支持如下画图功能：

- 画笔
- 圆/球
- 点和直线
- 长方形/长方体

#### 交互
在程序运行期间，屏幕上会显示两个窗口，分别显示实时的二维和三维画面。实时的三维画面是基于`matplotlib`，而最终导出的三维文件是程序结束后生成的。为了提高实时性能，您可以将实时三维画面[关闭](https://github.com/HarryXD2018/3DPainter/wiki/Document#util3dpy)。

##### 画笔

| 功能     | 手势                                                         |
| -------- | ------------------------------------------------------------ |
| 画笔     | 食指![finger](https://github.com/HarryXD2018/3DPainter/blob/master/demo/brush.gif) |
| 橡皮     | 食指与中指（仅在二维模式下）![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/eraser.gif) |
| 更换颜色 | 食指与小拇指 （随机选择新的颜色）![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/color.gif) |

##### 圆与球体

| 功能     | 手势                                       |
| -------- | ------------------------------------------ |
| 选择圆心 | 食指                                       |
| 扩大半径 | 圆的半径会随着食指和小拇指张开的时间而扩大 |

当收回小拇指时绘制球体。

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/sphere.gif)

##### 点

食指选择位置后保持食指不动，张开小拇指释放一个点。

##### 直线 

重复两次点的操作，在第一个端点选中后，会提供粉色的直线进行预览。

##### 长方形与长方体

与直线的操作相同。

##### 盖章

在程序开始运行时，会首先要求输入盖章的内容。同样的，食指选择放置的位置之后，小拇指伸出并收回进行放置。

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/Signature.png)

#### 窗口

在 `image` 窗口中一共有4个按键:

**切换功能**：左上角的按键用于切换绘制功能。您可以使用鼠标点击或是使用您的食指移动到紫色区域完成切换。当使用食指进行切换后，该按键会冻结5秒钟来避免抖动。

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/switch_mode.gif)

**清空屏幕**：右上角的按键可以清空实时画布上的所有内容。（目前并不会清除导出三维文件中）

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/clear.gif)

**保存**：鼠标点击左下角按键保存当前二维窗口下的内容。（画布内容以及摄像头拍摄内容，按键不会被保存）

**退出**：鼠标点击右下角按键用于退出。如果`GEN3D` 为真，则三维`ply`文件将会在摄像头关闭后生成。

| 交互     | 鼠标点击           | 食指触摸           |
| -------- | ------------------ | ------------------ |
| 切换功能 | :heavy_check_mark: | :heavy_check_mark: |
| 清空屏幕 | :heavy_check_mark: | :heavy_check_mark: |
| 保存     | :heavy_check_mark: | :x:                |
| 退出     | :heavy_check_mark: | :x:                |

#### 导出与查看

程序会默认导出`ply`文件，同样您也可以[关闭](https://github.com/HarryXD2018/3DPainter/wiki/Document#gen3dpy)自动导出功能。通过运行`view3d.py`程序可以查看您的成果。（记得修改打开文件名）

![](https://github.com/HarryXD2018/3DPainter/blob/master/demo/3dresult.png)

### 接口

请查看 [wiki](https://github.com/HarryXD2018/3DPainter/wiki/Document)页面。

### 新特性

[2021/07/27]

- 加入了点、线和长方体绘制功能。
- 同步画笔在两窗口下的颜色

[2021/07/28]

- 支持 `.ply` 文件的导出

[2021/07/29]

- 加入盖章功能
