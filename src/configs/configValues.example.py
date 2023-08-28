from typing import List

from .fileConfig import FileConfig


class ConfigValues:
    """
        This class contains the paths which will be used. Create one FileConfig per account.
    """

    @classmethod
    def createValues(cls):
        accountsConfigs: List[FileConfig] = []

        originalStatementsDirAccount1: str = "./schwab_statements/original/account1"
        fixedFilenamesStatementsDirAccount1: str = "./schwab_statements/fixedFilenames/account1"
        textStatementsDirAccount1 = "./output/docs/account1/"
        originalHistoryCsvPathAccount1 = "./schwab_statements/historyCsvs/account1_history.csv"
        combinedCsvPathAccount1 = "./output/combined/account1/combinedAccount1.csv"
        combinedFilteredCsvPathAccount1: str = "./output/combined/account1/filtered/transactionsFilteredAccount1.csv"

        account1 = FileConfig(originalStatementsDirAccount1, fixedFilenamesStatementsDirAccount1,
                                textStatementsDirAccount1, originalHistoryCsvPathAccount1,
                                combinedCsvPathAccount1, combinedFilteredCsvPathAccount1)


        originalStatementsDirAccount2: str = "./schwab_statements/original/account2"
        fixedFilenamesStatementsDirAccount2: str = "./schwab_statements/fixedFilenames/account2"
        textStatementsDirAccount2 = "./output/docs/account2/"
        originalHistoryCsvPathAccount2 = "./schwab_statements/historyCsvs/account2_history.csv"
        combinedCsvPathAccount2 = "./output/combined/account2/combinedAccount2.csv"
        combinedFilteredCsvPathAccount2: str = "./output/combined/account2/filtered/transactionsFilteredAccount2.csv"

        account2 = FileConfig(originalStatementsDirAccount2, fixedFilenamesStatementsDirAccount2,
                                textStatementsDirAccount2, originalHistoryCsvPathAccount2,
                                combinedCsvPathAccount2, combinedFilteredCsvPathAccount2)


        accountsConfigs.append(account1)
        accountsConfigs.append(account2)

        return accountsConfigs

