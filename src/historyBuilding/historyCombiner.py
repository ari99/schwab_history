from os import walk
import csv
import datetime
from typing import List

from configs.configValues import ConfigValues


class HistoryCombiner:
    """
        Combines the rows we made from the pdf statements with the history csv we can download
        from Schwab.
    """

    historyDateFormat = "%Y-%m-%d"

    def run(self) -> None:
        for account in ConfigValues.createValues():
            resultLines: List[List[str]] = self.__createCombined(account.textStatementsDir, account.originalHistoryCsvPath)
            self.__writeRows(account.combinedCsvPath, resultLines)



    def __createCombined(self, inputDirStatements: str, inputCsvPath: str) -> List[List[str]]:

        csvLines: List[List[str]] = self.__readLines(inputCsvPath)
        csvLines = self.__fixCsvLines(csvLines)
        csvLines = self.__fixDate(csvLines)
        csvLines.sort(key=lambda x: x[0])

        statementsLines: List[List[str]] = self.__createCombinedStatementsLines(inputDirStatements)
        statementsLines = self.__fixDate(statementsLines)
        statementsLines.sort(key=lambda x: x[0])

        csvStartDate: str = csvLines[0][0]
        # Get statement rows up to the first date in the history csv, then the
        # rest of the data comes from the history csv
        firstOccurance: int = self.__firstOccuranceOfDate(csvStartDate, statementsLines)
        result: List[List[str]] = statementsLines[:firstOccurance]
        result.extend(csvLines)

        result = self.__fixAmount(result)
        result = self.__fixQuantity(result)
        result = self.__addId(result)

        return result

    def __addId(self, rows: List[List[str]]) -> List[List[str]]:
        fixedRows: List[List[str]] = []
        for index, row in enumerate(rows):
            row.insert(0, str(index))
            fixedRows.append(row)
        return fixedRows

    def __fixAmount(self, rows: List[List[str]]) -> List[List[str]]:
        fixedRows: List[List[str]] = []
        for row in rows:
            row[7] = row[7].replace('$','')
            fixedRows.append(row)
        return fixedRows

    def __fixQuantity(self, rows: List[List[str]]) -> List[List[str]]:
        fixed: List[List[str]] = []
        for row in rows:
            action = row[1]
            if action == "Sell":
                print("Is Sell")
                row[4] = "-"+row[4]
            else:
                print(" Is '" +row[2] + "'" )
            fixed.append(row)
        return fixed

    def __firstOccuranceOfDate(self, date: str, rows: List[List[str]]) -> int:
        for index, row in enumerate(rows):
            if row[0] == date:
                return index

    def __fixCsvLines(self, csvLines: List[List[str]]) -> List[List[str]]:
        csvLines: List[List[str]] = csvLines[2:-1]
        return csvLines

    def __fixDate(self, rows: List[List[str]]) -> List[List[str]]:
        for row in rows:
            if "as of" in row[0]:
                splitDate: List[str] = row[0].split(" as of ")
                row[0] = splitDate[0]
            newDate: str = datetime.datetime.strptime(row[0], "%m/%d/%Y").strftime("%Y-%m-%d")
            row[0]= newDate
        return rows


    def __createCombinedStatementsLines(self, inputDirStatements: str) -> List[List[str]]:
        allLines: List[List[str]] = []
        filenames: List[str]|None = next(walk(inputDirStatements), (None, None, []))[2]  # [] if no file
        for fname in filenames:
            print("================= fname is " + fname)
            if fname != ".DS_Store":
                statementLines: List[List[str]] = self.__readLines(inputDirStatements+fname)
                allLines.extend(statementLines)
        return allLines

    def __readLines(self, inputPath: str) -> List[List[str]]:
        allRows: List[List[str]] =[]
        with open(inputPath, newline='') as csvfile:
            reader = csv.reader(csvfile)#, delimiter=' ', quotechar='|')
            for row in reader:
                allRows.append(row)
            return allRows



    def __writeRows(self, outputPath: str, rows: List[List[str]]) -> None:
        out = open(outputPath, "w")  # open text output
        writer = csv.writer(out)

        for row in rows:
            writer.writerow(row)

    '''
        def getLastRow(self, inputCsv):
            with open(inputCsv, 'r') as f:
                lastLine = f.readlines()[-2]
                return lastLine
    '''
