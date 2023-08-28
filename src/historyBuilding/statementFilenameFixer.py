from os import walk
import shutil

from configs.configValues import ConfigValues


class StatementFilenameFixer:
    """
        Converts file names like BrokerageStatement013114xxxx.pdf
        to BrokerageStatement2014013114xxxx.pdf
    """

    def run(self) -> None:
        for account in ConfigValues.createValues():
            self.__processFolder(account.originalStatementsDir, account.fixedFilenamesStatementsDir)

    def __processFolder(self, inputDir: str, outputDir: str) -> None:
        filenames = next(walk(inputDir), (None, None, []))[2]  # [] if no file
        for fname in filenames:
            print("================= fname is " + fname)
            if fname != ".DS_Store":
                self.__processDoc(inputDir, outputDir, fname)


    def __processDoc(self, inputDir: str, outputDir: str, fname: str) -> None:
        newName = self.__createNewName(fname)
        outputPath = outputDir + newName
        inputPath = inputDir + fname
        shutil.copyfile(inputPath, outputPath)

    def __createNewName(self, fname: str) -> str:
        year: str = "20"+fname[-10:-8]
        first: str = fname[0:18] # "BrokerageStatement"
        second: str = fname[18:] #two digit month, two digit day, two digit year,  4 digit account number, and extension
        print("year is " + year)
        print("first is " + first)
        print("second is " + second)
        newName = first+year+second
        print("new name is " + newName)
        return newName