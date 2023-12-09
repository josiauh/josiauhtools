py -m build
twine upload dist/* -u __token__ -p %PYPITOKEN%