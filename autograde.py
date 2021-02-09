import argparse
from os import makedirs, system
from pathlib import Path
from subprocess import PIPE
import logging
import os
import subprocess
from typing import Tuple
from shutil import which
import re
import sys


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)


from enum import Enum


class ToolStatus(Enum):
    NOT_FOUND = 0
    FAILED = 1
    PASSED = 2
    FATAL = 3


class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def grade(
    test_passed_fraction: float,
    memory_check_status: ToolStatus,
    static_analysis_status: ToolStatus,
) -> Tuple[int, str]:

    return grade, report


def cmd_exists(cmd):
    return which(cmd) is not None


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        "autograde",
        description="Utility program for grading code handins based on unit-tests and static analysis.",
    )

    args = parser.parse_args()

    ################### CHECK FOR MISSING DEPENDENCIES #########################
    missing_cmds = [cmd for cmd in ["cmake", "ctest"] if not cmd_exists(cmd)]
    if missing_cmds:
        raise RuntimeError(
            f"Unable to run, the following commands could not be located: {missing_cmds}. "
            "Please ensure they are installed and added to the systems path."
        )

    ################### COMPILE CODE #########################
    logger.info("Compiling code")
    try:
        build_path = Path("build")
        makedirs(build_path, exist_ok=True)

        with cd(build_path):
            if subprocess.run(["cmake", "configure", ".."]).returncode != 0:
                logger.error("Unable to configure CMake project")
                sys.exit(1)

            if subprocess.run(["cmake", "--build", "."]).returncode != 0:
                logger.error("Configured CMake project, but failed during compilation")
                sys.exit(1)

    except Exception:
        logger.error(
            "An unexpected error was encountered during compilation", exc_info=True,
        )
        system.exit(1)

    logger.info("Code compiled successfully")

    ################### TEST SUITE #########################
    logger.info("Running unittests")
    try:
        precentage_passing = (
            r"([0-9]+)% tests passed, [0-9]+ tests failed out of [0-9]+."
        )

        with cd(Path("build")):

            result = subprocess.run(["ctest", "--verbose"], stdout=PIPE)
            print(result.stdout.decode())
            matches = re.findall(
                precentage_passing, result.stdout.decode(), flags=re.DOTALL,
            )

            if not matches:
                raise ValueError(
                    f"Unable to extract precentage of passed tests from output using the regular expression: '{precentage_passing}'. Found {len(matches)} but expected exactly 1"
                )

            test_ok_fraction = int(matches[0]) / 100
            assert test_ok_fraction <= 1.0

    except Exception:
        logger.error(
            "An fatal error was encountered during the execution of test cases.",
            exc_info=True,
        )
        test_ok_fraction = 0.0

    logger.info(f"Finished running unittests")

    ################### MEMORY CHECKER #########################
    logger.info("Running Memory Checker")
    try:
        expr = r"Memory checker \(MemoryCheckCommand\) not set, or cannot find the specified program\."
        result = subprocess.run(
            ["ctest", "--verbose", "-T", "memcheck"], stderr=subprocess.PIPE
        )
        print(result.stderr.decode())

        if re.findall(expr, result.stderr.decode()):
            mem_check_status = ToolStatus.NOT_FOUND
        else:
            mem_check_status = (
                ToolStatus.PASSED if result.returncode == 0 else ToolStatus.FAILED
            )

    except Exception:
        mem_check_status = ToolStatus.FATAL
        logger.error(
            f"A fatal error was encountered during memory check", exc_info=True
        )

    logger.info("Memory checker finished")

    ################### STATIC ANALYSIS ##########################
    checkers = [
        (
            "cppcheck",
            "CMAKE_CXX_CPPCHECK",
            "cppcheck;--inconclusive;--error-exitcode=1;",
        ),
        (
            "clang-tidy",
            "CMAKE_CXX_CLANG_TIDY",
            "clang-tidy;-header-filter=.;-checks=*;-warnings-as-errors=*;",
        ),
    ]
    checker_results = []
    with cd(Path("build", "")):

        for cmd, key, value in checkers:

            if cmd_exists(cmd):

                os.environ[key] = value
                result = subprocess.run(["cmake", "--build", "."])
                del os.environ[key]

                checker_results.append(
                    ToolStatus.PASSED if result.returncode == 0 else ToolStatus.FAILED
                )
            else:
                checker_results.append(ToolStatus.NOT_FOUND)

    cppcheck_status, clang_tidy_status = checker_results

    ################### PRINT GRADE REPORT #########################

    grade = test_ok_fraction * 70

    if mem_check_status == ToolStatus.PASSED:
        grade += 20

    if cppcheck_status == ToolStatus.PASSED:
        grade += 10

    report = f"""
#######################################################################################################

Summary:
- test passed: {test_ok_fraction*100}%
- memory check: {mem_check_status}
- static analysis (cppcheck): {cppcheck_status}
- static analysis (clang-tidy): {clang_tidy_status}

Grading Scheme:
grade = test_passed_fraction * 70 + memory_check_passed * 20 + static_analysis_passed * 10

Final grade is: {grade}

#######################################################################################################
"""

    logger.info(report)
