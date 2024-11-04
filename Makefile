pre-commit:	# Run precommit
	pre-commit run --all-files

setup:	# Setup project
	pip install -r requirements/dev.txt

test: # Run tests
	pytest --create-db
