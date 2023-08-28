from dataclasses import dataclass

@dataclass
class FileConfig:
    """
        This holds the directorys and paths to inputs and outputs. One FileConfig per account.
    """
    # Original statements dir
    originalStatementsDir: str
    # Fixed filenames of original statements dir
    fixedFilenamesStatementsDir: str
    # Dir of the converted pdf to text statements, converted to CSV rows
    textStatementsDir: str
    # Original history csv's from schwab
    originalHistoryCsvPath: str
    # Path to the csv which holds the text statements combined with history data
    combinedCsvPath: str
    # Path to the combined csv filtered to hold only Buy and Sell transactions
    combinedFilteredCsvPath: str

