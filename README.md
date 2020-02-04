# CMPEDUDownload

机械工业出版社 PDF 下载器

## 使用方法

如果你想下载，可以直接使用 `downloads.txt` ，如果你想自己抓去地址，请参考以下命令：

```bash
pip3 install requests
# 获得 aria2 input file
python3 download.py | tee downloads.txt
# 使用 aria2 进行下载
aria2c -i downloads.txt
```

## 感谢

~~分片下载已经取消<https://www.cnblogs.com/owasp/p/6413480.html>~~

更多资源请关注此[repo](https://github.com/PythonShell/study-resource)