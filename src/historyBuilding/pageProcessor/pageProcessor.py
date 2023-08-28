from typing import List, TextIO


from .dividendsInterestProcessor import DividendsInterestProcessor
from .depositsWithdrawalsProcessor import DepositsWithdrawalsProcessor
from .purchasesSalesProcessor import PurchasesSalesProcessor
from .textParser import TextParser
from .transactionProcessor import TransactionProcessor
from typing import Final

class PageProcessor():
    """
        Converts text from a pdf to columns/rows for a csv using TextParser class
    """
    def __init__(self, text: str, out: TextIO, pageNumber: int, filename: str):
        self.text: str = text
        self.out: TextIO = out
        self.pageNumber: int = pageNumber
        self.filename: str = filename

    def __createProcessors(self) -> List[TransactionProcessor]:
        dividendsInterestStr: Final[str] = "Transaction Detail - Dividends & Interest"
        purchasesSalesStr: Final[str] = "Transaction Detail - Purchases & Sales"
        depositsWithdrawalsStr: Final[str] = "Transaction Detail - Deposits & Withdrawals"
        processors: List[TransactionProcessor] = []
        if purchasesSalesStr in self.text:
            processors.append(PurchasesSalesProcessor())

        if dividendsInterestStr in self.text:
            processors.append(DividendsInterestProcessor())

        if depositsWithdrawalsStr in self.text:
            processors.append(DepositsWithdrawalsProcessor())

        return processors

    def processPage(self) -> List[List[str]]:
        processors: List[TransactionProcessor] = self.__createProcessors()
        allRows: List[List[str]] = []
        for processor in processors:
            print("Starting processor: " + processor.getProcessorName() +
                  " Page: " + str(self.pageNumber) + " filename " + self.filename)
            textProcessor: TextParser = TextParser(self.text, self.pageNumber, processor)
            rows: List[List[str]] = textProcessor.processText()
            allRows.extend(rows)

        return allRows



