# CMPEDUDownload

机械工业出版社 PDF 下载器

## 使用方法

```bash
pip3 install requests
# 获得 aria2 input file
python3 download.py | tee downloads.txt
# 使用 aria2 进行下载
aria2c -i downloads.txt
```

## 感谢

<https://www.cnblogs.com/owasp/p/6413480.html>
