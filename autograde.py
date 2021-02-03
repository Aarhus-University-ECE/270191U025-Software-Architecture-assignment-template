import argparse
from os import makedirs
from pathlib import Path
from subprocess import CalledProcessError, Popen, PIPE
import logging
import os
import subprocess
from typing import Tuple
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)


class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def build():

    build_path = Path("build")

    makedirs(build_path, exist_ok=True)

    with cd(build_path):
        Popen(["cmake", "configure", ".."]).wait()
        Popen(["cmake", "--build", "."]).wait()


def grade(
    test_passed_fraction: float, memory_check_passed: bool, static_analysis_passed: True
) -> Tuple[int, str]:

    grade = (
        test_passed_fraction * 70
        + memory_check_passed * 20
        + static_analysis_passed * 10
    )

    report = f"""
#######################################################################################################
Final grade is: {grade}

grade = test_passed_fraction* 70 + memory_check_passed * 20 + static_analysis_passed * 10
{grade} = {test_passed_fraction}% * 70 + {memory_check_passed} * 20 + {static_analysis_passed} * 10
#######################################################################################################
"""
    return grade, report


def run_unittests() -> float:

    precentage_passing = r"([0-9]+)% tests passed, [0-9]+ tests failed out of [0-9]+."

    with cd(Path("build")):

        out, err = Popen(["ctest", "--verbose"], stdout=PIPE, stderr=PIPE).communicate()
        out = out.decode()
        print(out)

        matches = re.findall(precentage_passing, out, flags=re.DOTALL,)

        if len(matches) != 1:
            raise ValueError(
                f"Unable to extract precentage of passed tests from output. Found {len(matches)} but expected exactly 1"
            )

        fraction_passed = int(matches[0]) / 100
        assert fraction_passed <= 1.0
        return fraction_passed


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        "autograde",
        description="Utility program for grading code handins based on unit-tests and static analysis.",
    )

    parser.add_argument(
        "--unittest",
        action="store_true",
        default=True,
        help="run unit test against compiled program",
    )

    args = parser.parse_args()

    logger.info("Compiling code")
    try:
        build()
    except Exception:
        logger.warning(
            "The code did not compile, correct the compilation error and run the grading script again",
            exc_info=True,
        )

    logger.info("Code compiled successfully")

    test_passed_fraction = 0

    if args.unittest:
        logger.info("Running unittests")
        fraction_ok = run_unittests()
        logger.debug(f"Finished running unittests, {fraction_ok*100}% passed")

    grade, report = grade(test_passed_fraction, False, False)

    logger.info(report)
