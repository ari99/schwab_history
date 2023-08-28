from typing import TextIO, List

import fitz
import csv

from configs.configValues import ConfigValues
from .pageProcessor.pageProcessor import PageProcessor
from os import walk

class StatementProcessor:
    """
        Converts pdf brokerage statements to csv text files.
    """

    def run(self) -> None:
        print("--starting to convert pdf to texts")
        # To process a single file:
        #fname = "BrokerageStatement2015103115xxxx.pdf"
        #self.__processDoc(inputDir, outputDir, fname)
        for account in ConfigValues.createValues():
            self.__processFolder(account.fixedFilenamesStatementsDir, account.textStatementsDir)


    def __processFolder(self, inputDir: str, outputDir: str) -> None:
        filenames = next(walk(inputDir), (None, None, []))[2]  # [] if no file
        for fname in filenames:
            print("================= fname is " + fname)
            if fname != ".DS_Store":
                self.__processDoc(inputDir, outputDir, fname)

    def __processDoc(self, inputDir: str, outputDir: str, fname: str) -> None:
        outputPath: str = outputDir + fname + ".txt"
        inputPath: str = inputDir + fname
        doc = fitz.open(inputPath)  # open document
        out: TextIO = open(outputPath, "w")  # open text output
        writer = csv.writer(out)

        pageNumber: int = 1
        for page in doc:  # iterate the document pages
            text: str = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
            text: str = text.decode("utf-8")
            pageProcessor: PageProcessor = PageProcessor(text, out, pageNumber, fname)
            print("----------------=============== Page number is " + str(pageNumber))
            pageRows: List[List[str]] = pageProcessor.processPage()
            self.__writeRows(pageRows, writer)
            pageNumber += 1

        out.close()

    def __writeRows(self, rows: List[List[str]], writer) -> None:
        for row in rows:
            writer.writerow(row)
