import csv
from typing import List

from configs.configValues import ConfigValues
from historyTransaction import Transaction


class CombinedFilter():
    """
        Filters combined tranaction csv to create a csv of only buys/sells.
    """

    def run(self) -> None:
        for account in ConfigValues.createValues():
            self.__makeTransactionsFromCsv(account.combinedCsvPath, account.combinedFilteredCsvPath)

    def __makeTransactionsFromCsv(self, inputCsv: str, outputCsv: str) -> None:
        transactions: List[Transaction] = self.__readTransactions(inputCsv)
        transactions = self.__doTransactionFilter(transactions)

        self.__writeRows(outputCsv, transactions)

    def __doTransactionFilter(self, transactions: List[Transaction]) -> List[Transaction]:
        transactions: List[Transaction] = self.__doBuySellFilter(transactions)
        return transactions

    def __doBuySellFilter(self, transactions: List[Transaction]) -> List[Transaction]:
        filteredTransactions: List[Transaction] = []
        for transaction in transactions:
            if transaction.action == "Buy" or transaction.action == "Sell":
                filteredTransactions.append(transaction)
            else:
                print(transaction.action)

        return filteredTransactions


    def __readTransactions(self, inputCsv: str) -> List[Transaction]:
        allRows: List[Transaction] = []
        with open(inputCsv, newline='') as csvfile:
            reader = csv.reader(csvfile) #, delimiter=' ', quotechar='|')
            for row in reader:
                transaction: Transaction = Transaction.createFromCombinedHistoryRow(row)
                allRows.append(transaction)
            return allRows

    def __writeRows(self,outputPath: str, transactions: List[Transaction]):
        out = open(outputPath, "w")  # open text output
        writer = csv.writer(out)
        for transaction in transactions:
            writer.writerow(transaction.convertToCombinedHistoryRow())


