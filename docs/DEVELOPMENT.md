
# For developers

## Running tests:

Call `sh test_install.sh from-github` to check the installation from github.

Call `sh test_install.sh from-test-pypi` to check the installation from  test pypi

Call `sh test_install.sh from-pypi` to check the installation from pypi

Call `sh test_install.sh local keep` to keep the virtual environment after the run.

A less costly alternative is to use `test_in_active_env.sh` which installs the library in developer-mode in the active environment and runs unit tests.

To run only unit tests: `sh run_unit_tests.sh` 
to run only doctests: `sh run_doctests.sh` to
