from typing import List

from .transactionProcessor import TransactionProcessor


class DepositsWithdrawalsProcessor(TransactionProcessor):
    """
        Class to handle the deposits/withdrawals section of statements.
    """

    def fixHeaders(self, headers: List[str]) -> List[str]:
        # headers before fix ['Transaction', 'Date', 'Process', 'Date', 'Activity', 'Description ', 'Location', 'Credit/(Debit)']
        newHeaders = [headers[0] + " " + headers[1], headers[2] + " " + headers[3], headers[4], headers[5], headers[7]]
        # the above removes location because it is always missing
        return newHeaders

    # headers['Transaction Date', 'Process Date', 'Activity', 'Description ', 'Credit/(Debit)']
    # rows before normalize - LOCATION ALWAYS MISSING
    # 5  ['03/11/21', '03/11/21', 'Journaled Funds', 'JOURNAL FRM xxxx', '5,000.00']

    # row in history file
    #     "Date", "Action", "Symbol", "Description", "Quantity", "Price", "Fees & Comm", "Amount"
    # "07/13/2022","MoneyLink Transfer","","Tfr BANK OF ANTARTICA NA, xxxx","","","","-$2000.00"
    # "05/31/2022","Wire Sent","","WIRED FUNDS DISBURSED","","","","-$1391.52"
    # "03/21/2022","Journal","","JOURNAL TO xxxxx","","","","-$6000.00"
    # "12/13/2021","Journal","","TRANSFER FUNDS TO SCHWAB BANK - xxxxx","","","","-$2000.00"
    # "11/22/2021","Journal","","TRANSFER FUNDS FROM SCHWAB BANK - xxxxx","","","","$3000.00"
    # "09/24/2021","Journal","","JOURNAL TO xxxxx","","","","-$1500.00"

    def convertRowToHistoryFormat(self, row: List[str]) -> List[str]:
        newRow = ["" for _ in range(8)]
        newRow[0] = row[0]  # date
        newRow[1] = self.convertAction(row[2])
        newRow[2] = ""
        newRow[3] = row[3]  # decsription
        newRow[4] = ""  # quantity
        newRow[5] = ""  # price
        newRow[6] = ""  # fees
        newRow[7] = self.convertTotal(row[4])

        return newRow

    def convertAction(self, action: str) -> str:
        if action == "Journaled Funds":
            return "Journal"
        if action == "MoneyLink Txn":
            return "MoneyLink Transfer"
        else:
            return action

    def getProcessorName(self) -> str:
        return "DepositsWithdrawalsProcessor"

    def isHeaderStart(self, line: str, lineBefore: str, lineTwoBefore: str, lineAfter: str) -> bool:

        if line == "Transaction" and \
                (self.checkForTransactionDetail(lineBefore)
                 or (lineBefore.strip() == "..." and
                     self.checkForTransactionDetail(lineTwoBefore))) and \
                lineAfter == "Date":
            return True
        else:
            return False

    def checkForTransactionDetail(self, text: str) -> bool:
        if text == "Transaction Detail - Deposits & Withdrawals" or \
                text.strip() == "Transaction Detail - Deposits & Withdrawals (continued)":
            return True
        else:
            return False

    def isHeaderEnd(self, line: str, lineBefore: str) -> bool:
        if line == "Credit/(Debit)":
            return True
        else:
            return False

    def isFullRow(self, nextLine: str, currentRow: List[str]) -> bool:
        if len(currentRow) == 5 and currentRow[4].isnumeric() \
                and len(currentRow[4]) > 9 \
                and ("." == nextLine[-3] or "." == nextLine[-4]):  # if theres parens it will be -4
            return False
        elif len(currentRow) == 5:
            return True
        elif len(currentRow) == 6:
            return True
        else:
            return False

    def isSectionEnd(self, line: str) -> bool:
        if line == "Total Deposits & Withdrawals":
            return True
        else:
            return False

    def normalizeRow(self, row: List[str]) -> List[str]:
        if len(row) == 6:
            row[3] = row[3] + " " + row[4]
            row[4] = row[5]
            del row[5]  # pop not used for code clarity
        return row
