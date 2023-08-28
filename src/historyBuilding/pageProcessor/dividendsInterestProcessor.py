from typing import List

from .transactionProcessor import TransactionProcessor


class DividendsInterestProcessor(TransactionProcessor):
    """
        Class to process dividends/interest section of statements.
    """

    # history format
    # "11/26/2021","Qual Div Reinvest","SBUX","STARBUCKS CORP","","","","$25.30"
    # "11/26/2021","Qual Div Reinvest","OPY","OPPENHEIMER HLDGS CLASS A","","","","$16.95"
    # "11/16/2021 as of 11/15/2021","Bank Interest","","BANK INT xx SCHWAB BANK","","","","$0.05"

    #original row format
    # headers ['Transaction Date', 'Process Date', 'Activity', 'Description', 'Credit/(Debit)']
    # 5['03/05/21', '03/05/21', 'Qual Div Reinvest', 'PFIZER INC: PFE', '27.45']
    # 5['03/05/21', '03/05/21', 'Qual Div Reinvest', 'STARBUCKS CORP: SBUX', '18.50']
    # 5['03/15/21', '03/16/21', 'Bank Interest X,Z', 'BANK INT xx', '0.02']

    def convertRowToHistoryFormat(self, row: List[str]) -> List[str]:
        newRow: List[str] = ["" for _ in range(8)]
        newRow[0] = row[0]  # date
        newRow[1] = self.convertAction(row[2])  # TODO convert? #  action
        newRow[2] = self.getSymbol(row[3])
        newRow[3] = self.getDescription(row[3])
        newRow[4] = ""  # quantity
        newRow[5] = ""  # price
        newRow[6] = ""  # fees
        newRow[7] = self.convertTotal(row[4])
        return newRow

    def convertAction(self, action: str) -> str:
        if action == "Bank InterestX,Z" or action == "Bank Interest X,Z":
            return "Bank Interest"
        elif action == "Div For Reinvest":
            return "Qual Div Reinvest"
        elif action == "PrYr Div Reinvest":
            return "Pr Yr Div Reinvest"
        else:
            return action

    def fixHeaders(self, headers: List[str]) -> List[str]:
        # headers before fix ['Transaction', 'Date', 'Process', 'Date', 'Activity', 'Description', 'Credit/(Debit)']
        newHeaders = [headers[0]+" " + headers[1], headers[2]+" " + headers[3], headers[4], headers[5], headers[6]]
        return newHeaders

    def getProcessorName(self) -> str:
        return "DividendsInterestProcessor"

    def isHeaderStart(self, line: str, lineBefore: str, lineTwoBefore: str, lineAfter: str) -> bool:
        if line == "Transaction" \
                and ("Transaction Detail - Dividends & Interest" in lineBefore
                    or ("Transaction Detail - Dividends & Interest" in lineTwoBefore and
                     lineBefore.strip() == "...")) and \
         lineAfter == "Date":
            return True
        else:
            return False


    def isHeaderEnd(self, line: str, lineBefore: str) -> bool:
        if line == "Credit/(Debit)":
            return True
        else:
            return False

    def isFullRow(self, nextLine: str, currentRow: List[str]) -> bool:
        if len(currentRow) == 5:
            return True
        else:
            return False

    def normalizeRow(self, row: List[str]) -> List[str]:
        return row

    def isSectionEnd(self, line: str) -> bool:
        if "Total Dividends & Interest" in line:
            return True
        else:
            return False
