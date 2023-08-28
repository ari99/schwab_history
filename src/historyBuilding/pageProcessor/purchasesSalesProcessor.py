from typing import List

from .transactionProcessor import TransactionProcessor
import re


class PurchasesSalesProcessor(TransactionProcessor):
    '''
        Processes purchase/sales sections in Schwab statements.
    '''

    def __init__(self):
        self.redemptionCount: int = 0

    def getProcessorName(self) -> str:
        return "PurchasesSalesProcessor"

    def isHeaderStart(self, line: str, lineBefore: str, lineTwoBefore: str, lineAfter: str) -> bool:
        if (lineBefore == "Exchange Traded Funds Activity"
            or lineBefore == "Exchange Traded Funds Activity (continued)"
            or lineBefore == "Equity Funds Activity"
            or lineBefore == "Equities Activity"
            or lineBefore == "Equities Activity (continued)"
            or lineBefore == "Other Assets Activity (continued)"
            or lineBefore == "Other Assets Activity") \
                and line == "Settle Date":
            '''next see page 8 we are not getting the second section with
            other assets acitivty because we only check once per processor'''
            return True
        else:
            return False

    def isHeaderEnd(self, line: str, lineBefore: str) -> bool:
        if line == "Total Amount":
            return True
        else:
            return False

    def fixHeaders(self, headers: List[str]) -> List[str]:
        if headers[1] == "Trade Date Transaction":
            headers[1] = "Trade Date"
            headers.insert(2, "Transaction")
        return headers

    def isFullRow(self, nextLine: str, currentRow: List[str]) -> bool:
        rowLength = len(currentRow)
        if rowLength == 5 and \
                ((currentRow[2] == "Stock Merger" and "MERGER:" in nextLine) or
                 ((currentRow[2] == "Stock Split"
                   or currentRow[2] == "Reverse Split"
                   or currentRow[2] == "Cash-In-Lieu"
                   or currentRow[2] == "Redemption"
                   or currentRow[2] == "Spin-off"
                   or currentRow[2] == "Name Change")
                  and self.isEigth(nextLine))):
            return False
        elif rowLength == 5 and \
                (currentRow[2] == "Stock Merger"
                 or currentRow[2] == "Reorganized Issue"
                 or currentRow[2] == "Stock Split"
                 or currentRow[2] == "Reverse Split"
                 or currentRow[2] == "Cash-In-Lieu"
                 or currentRow[2] == "Redemption"
                 or currentRow[2] == "Spin-off"
                 or currentRow[2] == "Name Change"):
            return True
        if rowLength == 6 and \
                (currentRow[2] == "Stock Merger"
                 or currentRow[2] == "Stock Split"
                 or currentRow[2] == "Reverse Split"
                 or currentRow[2] == "Cash-In-Lieu"
                 or currentRow[2] == "Redemption"
                 or currentRow[2] == "Spin-off"
                 or currentRow[2] == "Name Change"):
            return True
        if rowLength == 7 and self.isEigth(nextLine):
            return False
        elif rowLength == 8:
            return True
        elif rowLength == 7 and not self.isEigth(nextLine):
            return True
        else:
            return False

    def isEigth(self, line: str) -> bool:
        foundColon = re.search("^.*: .*$", line)
        # print("line: "+line + " regex " + str(x))

        if foundColon or "UNSPONSORED" in line or "X SHS:" in line or \
                "CLASS" in line or \
                "ETF: " in line or \
                "REIT: " in line or \
                "SPLIT: " in line or \
                "** CALLED **" in line or \
                "SPONSORED ADR:" in line or \
                "NAME CHANGE" in line:
            return True
        else:
            return False

    def normalizeRow(self, row: List[str]) -> List[str]:
        row = super().removeExtraWhitespace(row)
        if len(row) == 8:
            row[3] = row[3] + " " + row[7]
            del row[7]  # pop not used for code clarity

        if len(row) == 6:  # stock merger manditory row
            row[3] = row[3] + " " + row[5]
            del row[5]

        return row

    def isSectionEnd(self, line: str) -> bool:
        if line == "Total Equities Activity" or line == "Total Other Assets Activity" \
                or line == "Total Exchange Traded Funds Activity" or line == "Total Equity Funds Activity":
            print("Section End")
            return True
        else:
            return False

    ''''
    "Date", "Action", "Symbol", "Description", "Quantity", "Price", "Fees & Comm", "Amount"
    "08/11/2022", "Qualified Dividend", "AAPL", "APPLE INC", "", "", "", "$40.31"
    "08/10/2022", "Buy", "EPAM", "EPAM SYSTEMS INC", "8", "$440.1434", "", "-$3521.15"
    "08/10/2022", "Buy", "PANW", "PALO ALTO NETWORKS", "6", "$519.89", "", "-$3119.34"
    "07/19/2022","Buy","GS","GOLDMAN SACHS GROUP","20","$318.7348","","-$6374.70"
    "07/18/2022 as of 07/15/2022","Bank Interest","","BANK INT xxxxx SCHWAB BANK","","","","$11.87"
    "07/18/2022 as of 07/15/2022","Stock Split","GOOG","ALPHABET INC. CLASS C","133","$112.767","",""
    "07/13/2022","MoneyLink Transfer","","Tfr BANK OF ANTARTICA NA, xxxxx","","","","-$2000.00"
    "06/29/2022","Qualified Dividend","GS","GOLDMAN SACHS GROUP","","","","$20.00"
    "06/16/2022","Sell","MA","MASTERCARD INC CLASS A","20","$309.7976","$0.14","$6195.81"
    "06/16/2022 as of 06/15/2022","Bank Interest","","BANK INT xxxx SCHWAB BANK","","","","$1.06"
    "06/13/2022","Sell","CRM","SALESFORCE INC","20","$170.34","$0.08","$3406.72"
    "06/13/2022","Sell","MCHP","MICROCHIP TECHNOLOGY","25","$62.26","$0.04","$1556.46"
    '''

    '''
    headers ['Settle Date', 'Trade Date', 'Transaction', 'Description', 'Quantity', 'Unit Price', 'Total Amount']

    7  ['03/02/21', '02/26/21', 'Sold', 'CD PROJEKT S A F UNSPONSORED ADR: OTGLY', '(100.0000)', '15.8400', '1,583.99']
    7  ['03/02/21', '02/26/21', 'Sold', 'CD PROJEKT S A F UNSPONSORED ADR: OTGLY', '(123.0000)', '15.8000', '1,943.39']
    7  ['03/02/21', '02/26/21', 'Sold', 'VIATRIS INC: VTRS', '(2.0000)', '14.6724', '29.34']
    7  ['03/02/21', '03/02/21', 'Reinvested Shares', 'VISA INC CLASS A: V', '0.0778', '216.0530', '(16.80)']
    7  ['03/02/21', '03/02/21', 'Reinvested Shares', 'ZOETIS INC CLASS A: ZTS', '0.0557', '158.0754', '(8.80)']
    7  ['03/03/21', '03/01/21', 'Bought', 'ACTIVISION BLIZZARD: ATVI', '3.0000', '98.3050', '(294.92)']
    7  ['03/03/21', '03/01/21', 'Bought', 'APPLE INC: AAPL', '2.0000', '125.1700', '(250.34)']
    7  ['03/03/21', '03/01/21', 'Bought', 'DOCUSIGN INC: DOCU', '1.0000', '238.4909', '(238.49)']
    '''

    def convertRowToHistoryFormat(self, row: List[str]) -> List[str]:
        newRow: List[str] = ["" for _ in range(8)]

        # "08/07/2019","Cash In Lieu","CRM","SALESFORCE COM","","","","$84.31"
        # "08/06/2019","Stock Merger","CRM","SALESFORCE COM","38","","",""
        # "08/06/2019","Stock Merger","DATA","TABLEAU SOFTWARE INC XXXMANDATORY MERGER EFF: 08/01/19","-35","","",""
        # "09/02/2020","Reorganized Issue","AAPL","APPLE INC","0.2781","","",""
        # "08/31/2020 as of 08/28/2020","Stock Split","TSLA","TESLA INC","36","$442.68","",""
        # 04/23/2020","Reverse Split","NUGT","DIREXION DAILY GOLD MINERS INDEX BULL 2X SHS","130","","",""
        # "04/23/2020","Reverse Split","25460E844","DIREXION DAILY GOLD XXXREVERSE SPLIT EFF: 04/23/20","-654.9675","","",""

        if len(row) == 5:  # stock merger or Reorganized Issue
            if row[2] == "Redemption":
                self.redemptionCount += 1

            newRow[0] = row[1]
            newRow[1] = self.convertAction(row[2])
            newRow[2] = self.getSymbol(row[3])
            newRow[3] = self.getDescription(row[3])
            if row[2] == "Stock Merger" \
                    or row[2] == "Reorganized Issue" \
                    or row[2] == "Stock Split" \
                    or row[2] == "Reverse Split" \
                    or row[2] == "Spin-off" \
                    or row[2] == "Name Change" \
                    or (row[2] == "Redemption" and self.redemptionCount % 2 == 1):
                newRow[4] = self.removeParensMerger(row[4])  # quantity
            elif row[2] == "Cash-In-Lieu" or (row[2] == "Redemption" and self.redemptionCount % 2 == 0):
                newRow[7] = self.convertTotal(row[4])
        else:
            newRow[0] = row[1]  # trade date
            newRow[1] = self.convertAction(row[2])
            newRow[2] = self.getSymbol(row[3])
            newRow[3] = self.getDescription(row[3])
            newRow[4] = self.removeParens(row[4])  # quantity
            newRow[5] = "$" + row[5]  # price
            newRow[6] = ""
            newRow[7] = self.convertTotal(row[6])

        return newRow

    def convertAction(self, action: str) -> str:
        if action == "Bought":
            return "Buy"
        elif action == "Sold":
            return "Sell"
        elif action == "Reinvested Shares":
            return "Reinvest Shares"
        elif action == "Cash-In-Lieu":
            return "Cash In Lieu"
        return action

    def removeParensMerger(self, val: str)-> str:  # mergers have -, others dont
        if "(" in val:
            return "-" + val.replace('(', '').replace(')', '')
        else:
            return val
