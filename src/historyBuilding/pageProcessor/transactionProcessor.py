from abc import ABC, abstractmethod
from typing import List
import datetime


class TransactionProcessor(ABC):
    """
        Abstract class for other classes which process sections in Schwab statements.
    """

    @abstractmethod
    def getProcessorName(self) -> str:
        pass

    @abstractmethod
    def isHeaderStart(self, line: str, lineBefore: str, lineTwoBefore: str, lineAfter: str) -> bool:
        pass

    @abstractmethod
    def isHeaderEnd(self, line: str,  lineBefore: str) -> bool:
        pass

    @abstractmethod
    def isSectionEnd(self, line: str) -> bool:
        pass

    @abstractmethod
    def isFullRow(self, nextLine: str, currentRow) -> bool:
        pass

    @abstractmethod
    def normalizeRow(self, row: List[str]) -> List[str]:
        pass

    @abstractmethod
    def convertRowToHistoryFormat(self, row: List[str]) -> List[str]:
        pass

    @abstractmethod
    def fixHeaders(self, headers: List[str]):
        pass

    def convertRowsToHistoryFormat(self, rows: List[List[str]]) -> List[List[str]]:
        newRows: List[List[str]] = []
        for row in rows:
            newRow: List[str] = self.convertRowToHistoryFormat(row)
            newRow[0] = datetime.datetime.strptime(newRow[0], "%m/%d/%y").strftime("%m/%d/%Y")
            newRows.append(newRow)

        return newRows

    def normalizeRows(self, rows: List[List[str]]) -> List[List[str]]:
        newRows: List[List[str]] = []
        for row in rows:
            newRow: List[str] = self.normalizeRow(row)
            newRows.append(newRow)

        return newRows

    def removeExtraWhitespace(self, row: List[str]) -> List[str]:
        for index, item in enumerate(row):
            row[index] = " ".join(item.split())

        return row

    def convertTotal(self, total: str) -> str:
        neg: str = ""
        if "(" in total:
            neg += "-"
        result: str = neg + "$" + self.removeParens(total)
        return result

    def removeParens(self, val: str) -> str:
        return val.replace('(', '').replace(')', '')

    def getSymbol(self, description: str) -> str:
        if ":" in description:
            splits: List[str] = description.split(":")
            return splits[1].strip()
        else:
            return ""

    def getDescription(self, description: str) -> str:
        if ":" in description:
            splits: List[str] = description.split(":")
            return splits[0].strip()
        else:
            return description

