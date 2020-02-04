#!/usr/bin/env python3
# coding=utf-8
import json

import requests

referer = "https://cmpebooks.s3.cn-north-1.amazonaws.com.cn/pdfReader/generic/build/pdf.worker.js"


def get_books(code: str):
    try:
        response = requests.post(
            "http://ebooks.cmanuf.com/getBookCategoryInfo",
            data={"code": code, "page": 1, "limit": 1000, "px": "desc"},
            timeout=15
        )
    except requests.exceptions.RequestException:
        print("Request timeout")
        exit(0)
    books = response.json()["module"]
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


def main():
    catgories = {}
    with open("categories.json", encoding='utf-8') as fp:
        catgories = json.load(fp)
        fp.close()
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
