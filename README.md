# getDLsiteIntro
Download album and introduction in the page of works, format names of works forders. Support 6-digi and 8-digi RJ-code<br>
获取DLsite作品页面的相册与文字介绍，并重命名作品文件夹。支持6位和8位RJ号。

## 使用说明
1 安装python 3.8以上环境（只测试过3.8以上版本）<br>
2 更新`pip`，安装`requests`，`pillow`，`bs4`，`lxml`库<br>
3 下载`getDLsiteIntro.py`文件，并放到待处理文件夹目录<br>
4 打开文件按照需求修改代理端口`proxies`，修改是否需要创建MP3文件夹`create_MP3_folder`（仅创建文件夹，程序并不会自动提取MP3文件）<br>
5 双击运行，或使用`python getDLsiteIntro.py`运行

## Instructions
1 Install python 3.8 or above (only tested 3.8 or above)<br> 
2 Update pip, install requests, pillow, bs4, lxml library<br> 
3 Download getDLsiteIntro.py file and put it in the folder directory containing "RJxxxxxx" folders <br> 
4 Open the .py file and modify the proxy port "proxies" according to the requirements, and modify whether to create an MP3 folder `create_MP3_folder` (only create a folder, the program will not automatically extract MP3 files)<br> 
5 Double-click to run, or use `python getDLsiteIntro.py` to run
