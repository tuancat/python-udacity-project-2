"""Represent models for near-Earth objects and their close approaches."""
import random
import string
import textwrap
from abc import ABC, abstractmethod
from typing import List

import PyPDF2
import pandas as pd
import docx
from PIL import Image, ImageDraw, ImageFont


class QuoteModel:
    """_summary_."""

    def __init__(self, body, author):
        """_summary_.

        Args:
            body (_type_): _description_.
            author (_type_): _description_.
        """
        self.body = body
        self.author = author

    def __str__(self):
        """_summary_.

        Returns:
            _type_: _description_.
        """
        return f"body:{self.body} and, Author: {self.author}."


class IngestorInterface(ABC):
    """_summary_.

    Args:
        ABC (_type_): _description_.

    Returns:
        _type_: _description_.
    """

    allowExtendsion = ['csv', 'txt', 'pdf', 'doc']

    @classmethod
    def canIngest(cls, path):
        """_summary_.

        Args:
            path (_type_): _description_.

        Returns:
            _type_: _description_.
        """
        ext = path.split('.')[-1]
        return ext in cls.allowExtendsion

    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """_summary_.

        Args:
            path (str): _description_.

        Returns:
            List[QuoteModel]: _description_.
        """
        pass


class CSVIngestor(IngestorInterface):
    """_summary_.

    Args:
        IngestorInterface (_type_): _description_.
    """

    def parse(cls, path: str) -> List[QuoteModel]:
        """_summary_.

        Args:
            path (str): _description_.

        Returns:
            List[QuoteModel]: _description_.
        """
        result = []
        df = pd.read_csv(path)
        # print(df['body'].head())
        for row in df.index:
            q = QuoteModel(df['body'][row], df['author'][row])
            result.append(q)
        return result


class DocxInvestor(IngestorInterface):
    """_summary_.

    Args:
        IngestorInterface (_type_): _description_.
    """

    def parse(cls, path: str) -> List[QuoteModel]:
        """_summary_.

        Args:
            path (str): _description_.

        Returns:
            List[QuoteModel]: _description_.
        """
        result = []
        doc = docx.Document(path)
        for i in doc.paragraphs:
            strData = i.text
            strData = strData.replace('"', ' ')
            if (len(strData) > 0):
                dataArr = strData.split('-')
                q = QuoteModel(dataArr[0], dataArr[1])
                result.append(q)

        return result


class TXTIngestor(IngestorInterface):
    """_summary_.

    Args:
        IngestorInterface (_type_): _description_.
    """

    def parse(cls, path: str) -> List[QuoteModel]:
        """_summary_.

        Args:
            path (str): _description_.

        Returns:
            List[QuoteModel]: _description_.
        """
        result = []
        f = open(path, "r")
        arrStr = f.readlines()
        for str in arrStr:
            dataArr = str.split('-')
            q = QuoteModel(dataArr[0], dataArr[1])
            result.append(q)

        return result


class PDFIngestor(IngestorInterface):
    """_summary_.

    Args:
        IngestorInterface (_type_): _description_.
    """

    def parse(self, path: str) -> List[QuoteModel]:
        """_summary_.

        Args:
            path (str): _description_.

        Returns:
            List[QuoteModel]: _description_.
        """
        # creating a pdf reader object
        result = []
        reader = PyPDF2.PdfReader(path)

        # print the number of pages in pdf file

        # print the text of the first page
        data = reader.pages[0].extract_text()
        for line in data.splitlines():
            if len(line) > 2:
                arr = line.split('-')
                quote = QuoteModel(arr[0], arr[1])
                result.append(quote)
        return result


class Ingestor(IngestorInterface):
    """_summary_.

    Args:
        IngestorInterface (_type_): _description_.

    Returns:
        _type_: _description_.
    """

    ingestors = [CSVIngestor, PDFIngestor, TXTIngestor, DocxInvestor]

    @classmethod
    def parse(cls, path: str, ) -> List[QuoteModel]:
        """_summary_.

        Args:
            path (str): _description_.

        Returns:
            List[QuoteModel]: _description_.
        """
        result = []
        for ingestor in cls.ingestors:
            ext = path.split('.')[-1]
            if ext == 'csv':
                csv = CSVIngestor()
                result.extend(csv.parse(path))
            elif ext == 'pdf':
                pdf = PDFIngestor()
                result.extend(pdf.parse(path))
            elif ext == 'docx':
                docx = DocxInvestor()
                result.extend(docx.parse(path))
            elif ext == 'txt':
                txt = TXTIngestor()
                result.extend(txt.parse(path))
        return result


class QuoteEngine:
    """_summary_."""

    def __init__(self) -> None:
        """_summary_."""
        super().__init__()


class MemeEngine:
    """_summary_."""

    def __init__(self, folderPath: str):
        """_summary_.

        Args:
            folderPath (str): _description_.
        """
        self.folderPath = folderPath

    @property
    def folder(self):
        """_summary_.

        Returns:
            _type_: _description_.
        """
        """Return a representation of the full name of this NEO."""
        return self.folderPath

    def make_meme(self, img, body, author):
        """_summary_.

        Args:
            img (_type_): _description_.
            body (_type_): _description_.
            author (_type_): _description_.

        Returns:
            _type_: _description_.
        """
        im = Image.open(img)
        path = f'{self.folderPath}/{random.random()}.jpg'
        mew = MemeGenerator(im, path)
        newIm = mew.insertText(quote)
        mew.saveImage(newIm)
        return path


class MemeGenerator:
    """_summary_."""

    def __init__(self, originImg, savePath):
        """_summary_.

        Args:
            originImg (_type_): _description_.
            savePath (_type_): _description_.
        """
        super().__init__()
        self.originImg = originImg
        self.savePath = savePath

    @property
    def ratio(self):
        """_summary_.

        Returns:
            _type_: _description_.
        """
        width, height = self.originImg.size
        return width / height

    def resize(self) -> Image:
        """_summary_.

        Returns:
            Image: _description_.
        """
        width, height = self.originImg.size
        newWidth = 500
        newHeight = int(self.ratio * height)
        self.originImg.resize((newWidth, newHeight))
        return self.originImg

    @property
    def getResizeImg(self) -> Image:
        """_summary_.

        Returns:
            Image: _description_.
        """
        return self.resize()

    def insertText(self, quote: QuoteModel) -> Image:
        """_summary_.

        Args:
            quote (QuoteModel): _description_.

        Returns:
            Image: _description_.
        """
        newImg = self.originImg
        font = ImageFont.truetype("arial_bold.ttf", size=18)
        dataText = f'{quote.body} - {quote.author}'
        lines = textwrap.wrap(dataText, width=20)
        draw = ImageDraw.Draw(newImg)
        w, h = newImg.size
        xOfText = random.randrange(w / 2 - 20)
        hOfText = random.randrange(10)
        for line in lines:
            height = 18
            draw.text((xOfText, hOfText), line, fill=(255, 0, 0), font=font)
            hOfText += height
            if hOfText >= h - 20:
                break
        return newImg

    def saveImage(self, img):
        """_summary_.

        Args:
            img (_type_): _description_.
        """
        img.save(self.savePath, "JPEG", quality=80, optimize=True, progressive=True)

# def randStr(chars=string.ascii_uppercase + string.digits, N=10):
#     return ''.join(random.choice(chars) for _ in range(N))

# if __name__ == "__main__":
#     im = Image.open('./_data/photos/dog/xander_1.jpg')
#     body = randStr('asdasdasdasd', 1000)
#     author = randStr('asdasasd', 100)
#     quote = QuoteModel(body, author)
#     mew = MemeGenerator(im)
#     mew.insertText(quote)
