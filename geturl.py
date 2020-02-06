#!/usr/bin/env python3
# coding=utf-8
import json
import requests

# 定义常量
referer = "https://cmpebooks.s3.cn-north-1.amazonaws.com.cn/pdfReader/generic/build/pdf.worker.js"
catgories_filename = "categories.json"
downloads_filename = "downloads.txt"


def get_books(code: str):
    try:
        response = requests.post(
            "http://ebooks.cmanuf.com/getBookCategoryInfo",
            data={"code": code, "page": 1, "limit": 1000, "px": "desc"},
            timeout=15
        )
    except requests.exceptions.RequestException:
        print("[ERR] request timeout")
        exit(0)
    try:
        books = response.json()["module"]
    except json.decoder.JSONDecodeError:
        print("[ERR] response can not json decode")
        print(response.content)
        exit(0)

    for bookInfo in books:
        cover = bookInfo["img"]
        if len(cover) <= 55 or "cmpebooks.s3.cn-north-1.amazonaws.com.cn" not in cover:
            continue
        pdf_link = (
            cover.replace("/Cover/", "/PDF/")
            .replace("/cover/", "/pdf/")
            .replace("Cover1.jpg", "2.pdf")
            .replace("Cover2.jpg", "2.pdf")
            .replace("Cover2.JPG", "2.pdf")
            .replace("cover_front.jpg", "L.pdf")
            .replace("cover_front_L.jpg", "L.pdf")
        )
        filename = (
            bookInfo["name"]
            .strip()
            .replace("  ", " ")
            .replace("/", "_")
            .replace(" ", "_")
        )
        yield pdf_link, "%s.pdf" % filename


def get_catgories(filename: str):
    catgories = {}
    f = None
    try:
        f = open(filename, 'r', encoding='utf-8')
        catgories = json.load(f)
    except FileNotFoundError:
        print("[ERR] %s not found" % (filename))
        exit(0)
    except LookupError:
        print("[ERR] %s encoding is not utf-8" % (filename))
        exit(0)
    except UnicodeDecodeError:
        print("[ERR] can not decode %s" % (filename))
        exit(0)
    except json.decoder.JSONDecodeError:
        print("[ERR] can not decode %s as a json file" % (filename))
        exit(0)
    finally:
        if f:
            f.close()
    return catgories


def main():
    catgories = get_catgories(catgories_filename)
    for category_code, category_name in catgories.items():
        if category_code[0] == "#":
            continue
        for pdf_link, filename in get_books(category_code):
            saved_path = "downloads/%s-%s/%s" % (
                category_code, category_name, filename)
            print("%s\n\treferer=%s\n\tout=%s" %
                  (pdf_link, referer, saved_path))


if __name__ == "__main__":
    main()
