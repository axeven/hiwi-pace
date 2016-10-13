.PHONY: help
help:
	@echo "make help\n	Print this message\n"
	@echo "make test\n	Perform automatic tests on test instances\n"
	@echo "make download\n	Download test instances and td-validate\n"
	@echo "make cleanall\n	Removes downloaded and test files\n"
	@echo "make clean\n	Removes test files\n"

.PHONY: test
test:
	@make download

.PHONY: download
download:
	@if [ ! -d "td-validate" ]; then \
		git clone  https://github.com/holgerdell/td-validate.git td-validate; \
	else \
		echo "Directory td-validate exists, not downloading ..."; \
	fi
	@if [ ! -d "testbed" ]; then \
		git clone  https://github.com/holgerdell/PACE-treewidth-testbed.git testbed; \
	else \
		echo "Directory testbed exists, not downloading ..."; \
	fi


.PHONY: cleanall
cleanall:
	@echo "Removing downloaded and test files ..."
	@rm -rf td-validate
	@rm -rf testbed
	@rm -rf test

.PHONY: clean
clean:
	@echo "Removing test files ..."
	@rm -rf test

