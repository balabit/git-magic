test:
	#PYTHONPATH="$(PYTHONPATH):." py.test
	python3 -m unittest discover gitmagic/tests

inotify_test:
	while true; do inotifywait -r -emodify,move,create .; make test; done

.PHONY: test inotify_test

