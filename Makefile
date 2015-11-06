all: buildenv makedoc

buildenv: 
	sudo ./system-setup
	virtualenv . --python=python2.7
	bin/pip install -r requirements.txt


makedoc: html pdf

html: 
	. bin/activate; cd docs; make html

pdf: 
	. bin/activate; cd docs; make latexpdf

clean:
	rm -rf .installed.cfg bin develop-eggs eggs parts 
	rm -rf *.tar.gz 
	rm -rf lib lib64 include share var etc tmp man local
	find . -name '*.pyc' | awk '{print "rm -f "$$1}' | sh
