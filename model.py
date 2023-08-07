import random
from abc import ABC, abstractmethod
from typing import List

import PyPDF2
import pandas as pd
import docx
from PIL import Image, ImageDraw, ImageFont


class QuoteModel:
    """_summary_
    """
    def __init__(self, body, author):
        """_summary_

        Args:
            body (_type_): _description_
            author (_type_): _description_
        """
        self.body = body
        self.author = author

    def __str__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return f"body:{self.body} and, Author: {self.author}."


class IngestorInterface(ABC):
    """_summary_

    Args:
        ABC (_type_): _description_

    Returns:
        _type_: _description_
    """
    allowExtendsion = ['csv', 'txt', 'pdf', 'doc'];

    @classmethod
    def canIngest(cls, path):
        """_summary_

        Args:
            path (_type_): _description_

        Returns:
            _type_: _description_
        """    
        ext = path.split('.')[-1];
        return ext in cls.allowExtendsion;

    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """_summary_

        Args:
            path (str): _description_

        Returns:
            List[QuoteModel]: _description_
        """     
        pass


class CSVIngestor(IngestorInterface):
    def parse(cls, path: str) -> List[QuoteModel]:
        """_summary_

        Args:
            path (str): _description_

        Returns:
            List[QuoteModel]: _description_
        """
        result = [];
        df = pd.read_csv(path);
        # print(df['body'].head());
        for row in df.index:
            q = QuoteModel(df['body'][row], df['author'][row]);
            result.append(q);
        return result
class DocxInvestor(IngestorInterface):
    """_summary_

    Args:
        IngestorInterface (_type_): _description_
    """
    
    def parse(cls, path: str) -> List[QuoteModel]:
        """_summary_

        Args:
            path (str): _description_

        Returns:
            List[QuoteModel]: _description_
        """
        result = [];
        doc = docx.Document(path)
        for i in doc.paragraphs:
            strData = i.text;
            strData = strData.replace('"', ' ');
            if(len(strData) >0):
                dataArr = strData.split('-');
                q = QuoteModel(dataArr[0], dataArr[1]);
                result.append(q)

        return result;


class TXTIngestor(IngestorInterface):
    """_summary_

    Args:
        IngestorInterface (_type_): _description_
    """
    def parse(cls, path: str) -> List[QuoteModel]:
        """_summary_

        Args:
            path (str): _description_

        Returns:
            List[QuoteModel]: _description_
        """        
        result = [];
        f = open(path, "r")
        arrStr = f.readlines()
        for str in arrStr:
            dataArr = str.split('-');
            q = QuoteModel(dataArr[0], dataArr[1]);
            result.append(q)

        return result;


class PDFIngestor(IngestorInterface):
    """_summary_

    Args:
        IngestorInterface (_type_): _description_
    """    
    def parse(self, path: str) -> List[QuoteModel]:
        """_summary_

        Args:
            path (str): _description_

        Returns:
            List[QuoteModel]: _description_
        """        
        # creating a pdf reader object
        result = [];
        reader = PyPDF2.PdfReader(path)

        # print the number of pages in pdf file

        # print the text of the first page
        data = reader.pages[0].extract_text();
        for line in data.splitlines():
            if len(line) > 2:
                arr = line.split('-');
                quote = QuoteModel(arr[0], arr[1]);
                result.append(quote);
        return result;

class Ingestor(IngestorInterface):
    """_summary_

    Args:
        IngestorInterface (_type_): _description_

    Returns:
        _type_: _description_
    """
    ingestors = [CSVIngestor, PDFIngestor, TXTIngestor, DocxInvestor]
    @classmethod
    def parse(cls, path: str, ) -> List[QuoteModel]:
        """_summary_

        Args:
            path (str): _description_

        Returns:
            List[QuoteModel]: _description_
        """        
        result = [];
        for ingestor in cls.ingestors:
            ext = path.split('.')[-1];
            if ext == 'csv':
                csv = CSVIngestor();
                result.extend(csv.parse(path))
            elif ext == 'pdf':
                pdf = PDFIngestor();
                result.extend(pdf.parse(path))
            elif ext == 'docx':
                docx = DocxInvestor();
                result.extend(docx.parse(path))
            elif ext == 'txt':
                txt = TXTIngestor();
                result.extend(txt.parse(path))
        return result;


class QuoteEngine:
    """_summary_
    """
    def __init__(self) -> None:
        """_summary_
        """        
        super().__init__()

class MemeEngine:
    """_summary_
    """
    def __init__(self, folderPath: str):
        """_summary_

        Args:
            folderPath (str): _description_
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
        """_summary_

        Args:
            img (_type_): _description_
            body (_type_): _description_
            author (_type_): _description_

        Returns:
            _type_: _description_
        """        
        im = Image.open(img);
        width, height = im.size
        newSize = (500, height);
        im.resize(newSize);
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype("arial_bold.ttf", size=18)
        str = f'{body} - {author}'
        draw.text((20,height/2), str, fill=(255, 0, 0), font=font)
        path = f'{self.folderPath}/{random.random()}.jpg';
        im.save(path, "JPEG", quality=80, optimize=True, progressive=True)
        return path

