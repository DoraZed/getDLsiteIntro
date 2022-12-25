import requests
from PIL import Image
from io import BytesIO
import logging
from bs4 import BeautifulSoup
import re
import json
import os
import time
# UA设置
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                          AppleWebKit/537.36 (KHTML, like Gecko) \
                          Chrome/102.0.0.0 \
                          Safari/537.36'}
# 代理设置
proxies = {"http": "http://127.0.0.1:12345", "https": "http://127.0.0.1:12345"}
# 是否创建存储MP3的文件夹
create_MP3_folder = True

def change_webp_to_jpg(webp_content):
    """
    将webp图片格式转换为jpg格式
    :param webp_content: webp图片字节流
    :return jpg_content: jpg图片字节流
    """
    jpg_content = ""
    try:
        if webp_content.upper().startswith(b"RIF"):
            im = Image.open(BytesIO(webp_content))
            if im.mode == "RGBA":
                im.load()
                background = Image.new("RGB", im.size, (255, 255, 255))
                background.paste(im, mask=im.split()[3])
                im = background
            img_byte = BytesIO()
            im.save(img_byte, format='JPEG')
            jpg_content = img_byte.getvalue()
    except Exception as err:
        logging.error(err)
    return jpg_content if jpg_content else webp_content

def strQ2B(ustring):
    """
    将全角字符格式转换为半角
    :param  ustring: 全角字符串
    :return rstring: 半角字符串
    """
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:                            # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:                   # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring

def format_name(origin_name):
    """
    去除【】及中间内容，去除windows文件命名非法字符
    :param origin_name: 原始字符串
    :return new_name: 处理后字符串
    """
    # 【****】
    new_name = re.sub('【.*?】', '', origin_name)

    # "（双引号）、*（星号）、<（小于）、>（大于）、?（问号）、\（反斜杠）、|（竖线）、/ (正斜杠)、 : (冒号)
    new_name = re.sub(r'[:/\\?*"<>|]', ' ', new_name)

    return new_name

def getIntro(RJ_number, folderPath):
    """
    获取作品页面上的图册、简介，
    简介存储到作品文件夹
    构建子文件夹img用于存储图片
    :param RJ_number: 作品编号
    :param folderPath: 作品文件夹目录
    :return title_re: 格式化后的作品名，不含编号
    """
    url = 'https://www.dlsite.com/maniax/work/=/product_id/%s.html'%RJ_number
    html = requests.get(url, headers = headers, proxies = proxies)
    soup = BeautifulSoup(html.text, features="lxml")
    del html

    # title  h1
    title_tag = soup.find('h1') # title / id = "work_name"
    title = title_tag.get_text()
    title = strQ2B(title)
    title_re = format_name(title)
    print('origin title: ' + RJ_number + title)
    print('custom title: ' + RJ_number + title_re)
    del title_tag, title

    # intro   <div class="work_parts_container" itemprop="description">
    intro_tag = soup.find(itemprop="description")
    intro = intro_tag.get_text()
    intro = intro.replace('\r','')
    intro_re = re.sub('\n\n\n+', '\n', intro)
    del intro

    fp = open('%s\\%s_intro.txt'%(folderPath, RJ_number), 'w', encoding = 'utf-8')
    fp.write(intro_re)
    fp.close()
    print(RJ_number+' intro is written succeessfully')

    # img
    img_urls = []
    img_intro_urls = []
    slider_tag = soup.find(ref="product_slider_data")
    img_smp_tag = slider_tag.find_all('div')
    for img in img_smp_tag:
        img_urls.append('https:'+img['data-src'])
#    img_intro_tag = intro_tag.find_all('img')
#    for img in img_intro_tag:
#        img_intro_urls.append('https:'+img['src'])
    print('get img list succeessfully')

    del slider_tag, img_smp_tag, intro_tag
#    del img_intro_tag

    imgFolderPath = folderPath + '\\intro_img'
    try:
        os.makedirs(imgFolderPath)
        print('img folder is created succeessfully')
        for url in img_urls:
            # 'https://img.dlsite.jp/modpub/images2/work/doujin/RJ392000/RJ391733_img_smp1.webp'
            # 'https://img.dlsite.jp/modpub/images2/work/doujin/RJ01006000/RJ01005461_img_main.webp'
            name = re.search('RJ\d{6,8}_img_(main|smp\d*)',url).group()
            img = requests.get(url, headers = headers, proxies = proxies)
            jpg_binary = change_webp_to_jpg(img.content)
            f = open('%s\\%s.jpg'%(imgFolderPath, name),'wb')
            f.write(jpg_binary) #写入二进制内容
            f.close()
            print(name + ' download succeessfully')
            time.sleep(1)
        # i = 0
        # for url in img_intro_urls:
        #     # "https://img.dlsite.jp/modpub/images2/parts/RJ392000/RJ391733/c8dceae1147ffe6f6f80709ba50a9625.jpg"
        #     img = requests.get(url, headers = headers, proxies = proxies)
        #     i += 1
        #     f = open('%s\\%s_img_intro%d.jpg'%(imgFolderPath, RJ_number, i),'wb')
        #     f.write(img.content) #写入二进制内容
        #     f.close()
        #     print('%s_img_intro%d download succeessfully'%(RJ_number, i))
        #     time.sleep(1)
    except FileExistsError:
        print('img folder exist')
        pass

    return title_re

def getPath():
    """
    获取当前文件夹路径，调用其他函数
    """
    rootPath = os.getcwd()
    MP3Path = 'E:\\Voice MP3'   # MP3文件夹地址
    dir_list = []
    for root, dirs, files in os.walk(rootPath):
        dir_list = dirs
        break
    #print(dir_list)
    for folder in dir_list:
        print('\n=============================================\n'+folder+'\n')
        try:
            RJ_number = re.search('RJ\d{6,8}', folder).group()
        except AttributeError:
            continue
        folderPath = rootPath + '\\' + folder
        title = getIntro(RJ_number, folderPath)
        newFolderPath = rootPath + '\\' + RJ_number + ' ' + title
        MP3FolderPath = MP3Path + '\\' + RJ_number + ' ' + title
        os.rename(folderPath, newFolderPath)
        print('folder renamed successfully')
        if create_MP3_folder:
            try:
                os.makedirs( MP3FolderPath)
                print('MP3 folder is created succeessfully')
            except FileExistsError:
                print('MP3 folder exist')
                pass
        time.sleep(5)
    os.system("pause")

getPath()
