pip install --user pre-commit
git init
git add .
pre-commit install
pre-commit run -a
git add .