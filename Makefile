.PHONY: help
help:  # from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: check-lint
check-lint:  ## Lint the code
	mypy todo_txt
	flake8 todo_txt

.PHONY: check-format
check-format:  ## Check formatting
	isort --check --diff todo_txt
	black --check --diff todo_txt

.PHONY: check-test
check-test:  ## Run unit tests
	pytest --exitfirst

.PHONY: check
check: check-format check-lint check-test  ## Run all checks

.PHONY: format
format:  ## Format all files
	isort todo_txt
	black todo_txt
