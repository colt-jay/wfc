import defopt
import structlog

from wfc.wfc_2d import wfc_2d


def main():
    """Light wrapper around defopt.run to run the WFC Algorithm."""
    structlog.configure(logger_factory=structlog.PrintLoggerFactory())
    defopt.run(wfc_2d)


if __name__ == "__main__":
    main()
