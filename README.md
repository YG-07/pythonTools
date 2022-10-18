### Python 工具使用说明

### 目录

1. [SplitByRowCol(图片分割[按行列数])](#SplitByRowCol)
2. [SplitByPx(图片分割[按固定尺寸])](#SplitByPx)
3. [Thumbnail（生成缩略图）](#Thumbnail)
4. [ImageDownload（图片批量下载）](#ImageDownload)
5. [Rename（批量重命名）](#Rename)

### 具体说明

<a name="SplitByRowCol"></a>

#### 1. SplitByRowCol(图片分割[按行列数])

> 1.输入分割的原图片路径  
> 2.输入分割的行列数

<a name="SplitByPx"></a>

#### 2. SplitByPx(图片分割[按固定尺寸])

> 1.输入分割的原图片路径  
> 2.输入分割后的图片尺寸，输入图片定位方式 `N E S W`，1 或 2 个字母进行定位  
> 3.输入保存后的图片格式。注：`png|gif格式的才有透明度，直接改图片后缀并不能改变图片透明度的保存方式，要通过画图工具另存为`

<a name="Thumbnail"></a>

#### 2.Thumbnail（生成缩略图）

> 1.输入原图所在的目录路径  
> 2.输入生成的缩略图尺寸  
> 3.输入是否需要复制转换失败的图片

<a name="ImageDownload"></a>

#### 4.ImageDownload（图片批量下载）

> 1.输入 url 和 name 保存 TXT 文件路径，注：`一行一个记录，第一行可以使用[start][end]给之后的每一行拼接前缀或后缀`  
> 2.输入保存的文件夹名、图片格式  
> 3.输入是否需要必须包含或过滤的字符，等待下载

<a name="Rename"></a>

#### 5.Rename（批量重命名）

> 1.在程序同级目录创建`config.txt`文件, 参数如下  
> 2.运行本程序即可

| 参数   | 默认值 | 可选值                                     | 说明                                                          |
| ------ | ------ | ------------------------------------------ | ------------------------------------------------------------- |
| option | -      | number,datetime,size,start,end,mid         | 重命名的方式                                                  |
|        |        | number 时，[,1 1 1 3 x,1,5...]             | (开始数，步长，增减顺序， 不足几位，不足前补充 x 字符)        |
|        |        | datetime 时,[0 %Y-%m-%d-%H-%M-%S, 1 10...] | 日期时间格式化的参数(日期字符串/时间戳， 格式/保留位数(3-13)) |
| data   |        | size:[,KB,MB 1...]                         | （单位，是否显示单位）                                        |
|        |        | end:[xxxx]                                 | 后缀字符串                                                    |
|        |        | start:[xxxx]                               | 前缀字符串                                                    |
|        |        | mid:[xxxx,xxxx 5...]                       | 中间字符串（插入字符串，第几个字符后）                        |
| copy   | 0      | 1 D:\xxxx                                  | 是否另存为                                                    |
| origin | 0      | 1                                          | 是否保留原名称                                                |
