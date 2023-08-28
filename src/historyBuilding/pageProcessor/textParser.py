from typing import List

from historyBuilding.pageProcessor.transactionProcessor import TransactionProcessor


class TextParser:
    """
        Converts text to rows for a csv.
    """
    def __init__(self, text: str, pageNumber: int, processor: TransactionProcessor):
        self.text: str = text
        self.pageNumber: int = pageNumber
        self.headerStarted: bool = False
        self.headerEnded: bool = False
        self.currentRow: List[str] = []
        self.headers: List[str] = []
        self.rows: List[List[str]] = []
        self.inSection = False
        self.processor: TransactionProcessor = processor

    def processText(self) -> List[List[str]]:

        lines = self.text.splitlines()

        #headerStarts = self.__findHeaderStarts(processor)
        line=""
        for index, line in enumerate(lines):
            self.__processLine(lines, line, index)

        if self.processor.isFullRow(line, self.currentRow):
            print("appending row")
            print(self.currentRow)
            self.rows.append(self.currentRow)
            self.currentRow = []

        print("Rows before normalize ")
        self.printRows(self.rows)
        self.rows = self.processor.normalizeRows(self.rows)
        self.rows = self.processor.convertRowsToHistoryFormat(self.rows)

        print("headers before fix " + str(self.headers))
        self.headers = self.processor.fixHeaders(self.headers)
        print("headers after fix " + str(self.headers))
        self.printRows(self.rows)
        return self.rows


    def __processLine(self, lines: List[str], line: str, index: int):
        lineTwoBefore = self.__getLineTwoBefore(lines, index)
        lineBefore = self.__getLineBefore(lines, index)
        lineAfter = self.__getNextLine(lines, index)

        if self.processor.isHeaderStart(line, lineBefore, lineTwoBefore, lineAfter):
            self.__foundHeaderStart(line)
        elif self.processor.isHeaderEnd(line, lineBefore) and self.headerStarted:
            self.__foundHeaderEnd(line)
        elif self.headerStarted and not self.headerEnded:
            self.headers.append(line)
        elif self.processor.isSectionEnd(line) and self.inSection:
            self.__foundSectionEnd(line)
        elif self.headerStarted and self.headerEnded and self.inSection:
            self.__foundInSection(line)

        print("              '" + line + "'")

    def __foundHeaderStart(self, line: str) -> None:
        print("Start header")
        self.headerStarted = True
        self.inSection = True
        self.headers.append(line)

    def __foundHeaderEnd(self, line: str) -> None:
        print("End header")
        self.headerEnded = True
        self.headers.append(line)

    def __foundSectionEnd(self, line: str) -> None:
        self.inSection = False
        self.headerStarted = False
        self.headerEnded = False
        if self.processor.isFullRow(line, self.currentRow):
            print("appending row")
            print(self.currentRow)
            self.rows.append(self.currentRow)
            self.currentRow = []

    def __foundInSection(self, line: str) -> None:
        if self.processor.isFullRow(line, self.currentRow):
            print("appending row")
            print(self.currentRow)
            self.rows.append(self.currentRow)
            self.currentRow = []

        self.currentRow.append(line)

    def __getLineBefore(self, lines: List[str], index: int) -> str:
        if index == 0:
            return ""
        else:
            return lines[index-1]

    def __getLineTwoBefore(self, lines: List[str], index: int) -> str:
        if index == 0 or index == 1:
            return ""
        else:
            return lines[index-2]

    def __getNextLine(self, lines: List[str], index: int) -> str:
        if index == len(lines)-1:
            return ""
        else:
            return lines[index + 1]

    def printRows(self, rows: List[List[str]]) -> None:
        print("ROWS page " + str(self.pageNumber))
        for row in (rows or []):
            print(str(len(row)) + "  " + str(row))

    '''
        def __findHeaderStarts(self, processor: TransactionProcessor) -> List:
            lines = self.text.splitlines()
            headerStarts = []
            for index, line in enumerate(lines):
                lineBefore = self.__getLineBefore(lines, index)
                lineTwoBefore = self.__getLineTwoBefore(lines, index)
                lineAfter = self.__getNextLine(lines, index)
                if processor.isHeaderStart(line, lineBefore, lineTwoBefore, lineAfter):
                    headerStarts.append(index)
    
            return headerStarts
    '''

    '''
        def isDate(text):
            r = re.compile('.{2}/.{2}/.{2}')
            if r.match(line) is not None:
                return True
            else:
                return False
    '''

