# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = backgammon
SOURCEDIR     = docs
BUILDDIR      = build


backgammon.pot: src/dice_frame.py src/backgammon_frame.py main.py
	pybabel extract -o $@ $^

ru: translations/ru/LC_MESSAGES/backgammon.mo

translations/ru/LC_MESSAGES/backgammon.po: backgammon.pot
	pybabel update -D backgammon -i $^ -d translations -l ru

translations/ru/LC_MESSAGES/backgammon.mo: translations/ru/LC_MESSAGES/backgammon.po
	pybabel compile -D backgammon -i $^ -o $@

clean:
	rm -rf backgammon.pot translations/ru/LC_MESSAGES/backgammon.mo build *.bak *.orig env .coverage

git-clean:
	git clean -fd

check:
	flake8 .
	pydocstyle src

test:
	coverage run -m unittest tests/*.py
	coverage report

env: requirements.txt
	pip3 install virtualenv
	python3 -m venv env; . env/bin/activate; pip3 install -r requirements.txt

# Put it first so that "make" without argument is like "make help".
help:
	$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# # Catch-all target: route all unknown targets to Sphinx using the new
# # "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
html: Makefile
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

