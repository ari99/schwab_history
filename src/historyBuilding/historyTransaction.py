import csv
from typing import List


class Transaction:
    """
        Class to hold transaction data.
    """

    def __init__(self):
        self.id = 0
        self.date = ""
        self.action = ""
        self.symbol = ""
        self.description = ""
        self.quantity = ""
        self.price = ""
        self.fees = ""
        self.amount = ""

    @classmethod
    def createFromHistoryRow(cls, row: List[str]):
        transaction = Transaction()
        transaction.date = row[0]
        transaction.action = row[1]
        transaction.symbol = row[2]
        transaction.description = row[3]
        transaction.quantity = row[4]
        transaction.price = row[5]
        transaction.fees = row[6]
        transaction.amount = row[7]
        return transaction

    @classmethod
    def createFromCombinedHistoryRow(cls, row: List[str]):
        transaction = Transaction()
        transaction.id = row[0]
        transaction.date = row[1]
        transaction.action = row[2]
        transaction.symbol = row[3]
        transaction.description = row[4]
        transaction.quantity = row[5]
        transaction.price = row[6]
        transaction.fees = row[7]
        transaction.amount = row[8]
        return transaction

    def convertToCombinedHistoryRow(self):
        row = ["" for i in range(9)]
        row[0] = self.id
        row[1] = self.date
        row[2] = self.action
        row[3] = self.symbol
        row[4] = self.description
        row[5] = self.quantity
        row[6] = self.price
        row[7] = self.fees
        row[8] = self.amount
        return row

    def convertToHistoryRow(self) -> List[str]:
        row = ["" for i in range(8)]
        row[0] = self.date
        row[1] = self.action
        row[2] = self.symbol
        row[3] = self.description
        row[4] = self.quantity
        row[5] = self.price
        row[6] = self.fees
        row[7] = self.amount
        return row


    def readTransactions(self, inputPath) -> List:
        allRows: List[Transaction] = []
        with open(inputPath, newline='') as csvfile:
            reader = csv.reader(csvfile)#, delimiter=' ', quotechar='|')
            for row in reader:
                transaction: Transaction = Transaction.createFromCombinedHistoryRow(row)
                allRows.append(transaction)
            return allRows

    def writeRows(self, outputPath: str, transactions: List) -> None:
        out = open(outputPath, "w")  # open text output
        writer = csv.writer(out)
        for transaction in transactions:
            writer.writerow(transaction.convertToCombinedHistoryRow())


'''    def convertTransactionToHistoryRow(self, transaction):
        row = ["" for i in range(8)]
        row[0] = transaction.date
        row[1] = transaction.action
        row[2] = transaction.ticker
        row[3] = transaction.description
        row[4] = transaction.quantity
        row[5] = transaction.price
        row[6] = transaction.fees
        row[7] = transaction.amount
        return row
'''