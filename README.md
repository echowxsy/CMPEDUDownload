# CMPEDUDownload

机械工业出版社 PDF 下载器

> 各位读者，非常抱歉，因工程技术图书馆免费开放阅读后访问量过大，服务器超载，暂不能提供服务。现正在紧急升级扩容中。感谢大家的支持，扩容完毕即恢复开放，请各位读者谅解。

**目前已经关闭了书籍查询接口和图书CDN，无法获取到书籍信息也无法下载书籍。**

## 使用方法

如果你想下载，可以直接使用 `downloads.txt` 。
如果你想自己抓取地址，请参考以下命令：

```bash
pip3 install requests
# 获得 aria2 input file
python3 geturl.py | tee downloads.txt
# 使用 aria2 进行下载
aria2c -i downloads.txt
```

## 感谢

~~分片下载已经取消<https://www.cnblogs.com/owasp/p/6413480.html>~~

更多资源请关注此 Repo:[PythonShell/study-resource](https://github.com/PythonShell/study-resource)
