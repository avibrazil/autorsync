pkg:
	-rm dist/*
	python -m build

pypi-test:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi:
	python3 -m twine upload --verbose dist/*

example:
	./obfuscate.sed < autorsync.yaml > autorsync-example.yaml

changelog:
	f1=`mktemp`; \
	f2=`mktemp`; \
	git tag --sort=-committerdate | tee "$$f1" | sed -e 1d > "$$f2"; \
	paste "$$f1" "$$f2" | sed -e 's|	|...|g' | while read range; do echo; echo "## $$range"; git log '--pretty=format:* %s' "$$range"; done; \
	rm "$$f1" "$$f2"

clean:
	-rm -rf auto_remote_sync.egg-info dist build autorsync/__pycache__ *dist-info *pyproject-* .pyproject* .package_note*

tgz: clean
	cd ..; tar --exclude-vcs -czvf autorsync.tgz autorsync

rpm:
	# RPM will be generated in ~/rpmbuild/RPMS/noarch
	rpmbuild -ba --build-in-place autorsync.spec
