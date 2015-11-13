test:
	PYTHONPATH="$(PYTHONPATH):." py.test

inotify_test:
	while true; do inotifywait -r -emodify,move,create .; make test; done

.PHONY: test inotify_test

