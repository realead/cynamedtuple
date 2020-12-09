set -e

ENV_DIR="../p3"
virtualenv -p python3 "$ENV_DIR"

#activate environment
. "$ENV_DIR/bin/activate"


# check clean install:
if [ "$1" = "from-github" ]; then
    echo "Installing setup.py from github..."
    pip install https://github.com/realead/cynamedtuple/zipball/master
elif [ "$1" = "from-test-pypi" ]; then
    pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple cynamedtuple
elif [ "$1" = "from-pypi" ]; then
    pip install cynamedtuple
else
    echo "Installing local setup.py..."
    for dir_name in "build" ".eggs" "dist"
    do
        if [ -d "../$dir_name" ]; then
           echo "clean build, deleting ../$dir_name directory"
           rm -r "../$dir_name"
        fi; 
    done  
    (cd .. && python -m pip install .)
fi;


#install packages needed for testing:
pip install cython

echo "Installed packages:"
pip freeze

#tests:
sh run_unit_tests.sh

#clean or keep the environment
if [ "$2" = "keep" ]; then
   echo "keeping enviroment $ENV_DIR"
else
   rm -r "$ENV_DIR"
fi;
