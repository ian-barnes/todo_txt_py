python_src=todo_txt tests

.PHONY: help
help:  # from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: check-lint
check-lint:  ## Lint the code
	mypy ${python_src}
	flake8 ${python_src}

.PHONY: check-format
check-format:  ## Check formatting
	isort --check --diff ${python_src}
	black --check --diff ${python_src}

.PHONY: check-test
check-test:  ## Run unit tests
	pytest --exitfirst

.PHONY: check
check: check-format check-lint check-test  ## Run all checks

.PHONY: format
format:  ## Format all files
	isort ${python_src}
	black ${python_src}
