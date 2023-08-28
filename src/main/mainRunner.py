from historyBuilding.combinedFilter import CombinedFilter
from historyBuilding.historyCombiner import HistoryCombiner
from historyBuilding.statementFilenameFixer import StatementFilenameFixer
from historyBuilding.statementProcessor import StatementProcessor

def run():
    # Uncomment 1 step at a time to check the output

    # 1 - Convert the original statement pdfs filenames to a more usable format
    fixer = StatementFilenameFixer()
    fixer.run()

    # 2 - Convert the fixed filenames statement pdfs to text csv documents
    #statementProcessor = StatementProcessor()
    #statementProcessor.run()

    # 3 - Combine downloadable Schwab history with data csv's from statements.
    #historyCombiner = HistoryCombiner()
    #historyCombiner.run()

    # 4 - Filter transactions for only buys/sells
    #combinedFilter = CombinedFilter()
    #combinedFilter.run()



if __name__ == '__main__':
    run()


