### Python工具使用说明

### 目录
1. [SplitByRowCol(图片分割[按行列数])](#SplitByRowCol)  
2. [SplitByPx(图片分割[按固定尺寸])](#SplitByPx) 
3. [Thumbnail（生成缩略图）](#Thumbnail)
4. [ImageDownload（图片批量下载）](#ImageDownload)


### 具体说明
<a name="SplitByRowCol"></a>  
#### 1. SplitByRowCol(图片分割[按行列数])  

>1.输入分割的原图片路径  
>2.输入分割的行列数  

<a name="SplitByPx"></a>  
#### 2. SplitByPx(图片分割[按固定尺寸])  

>1.输入分割的原图片路径  
>2.输入分割后的图片尺寸，输入图片定位方式 `N E S W`，1或2个字母进行定位  
>3.输入保存后的图片格式。注：`png|gif格式的才有透明度，直接改图片后缀并不能改变图片透明度的保存方式，要通过画图工具另存为`  

  
<a name="Thumbnail"></a>  
#### 2.Thumbnail（生成缩略图）  

>1.输入原图所在的目录路径  
>2.输入生成的缩略图尺寸  
>3.输入是否需要复制转换失败的图片  
  
<a name="ImageDownload"></a>  
#### 4.ImageDownload（图片批量下载）

>1.输入url和name保存TXT文件路径，注：`一行一个记录，第一行可以使用[start][end]给之后的每一行拼接前缀或后缀`  
>2.输入保存的文件夹名、图片格式  
>3.输入是否需要必须包含或过滤的字符，等待下载 
  
