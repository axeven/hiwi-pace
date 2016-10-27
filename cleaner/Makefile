.PHONY: help
help:
	@echo "make help\n	Print this message\n"
	@echo "make test\n	Perform automatic tests on test instances\n"
	@echo "make runtask\n	Perform BFS on task instances\n"
	@echo "make download\n	Download task instances and td-validate\n"
	@echo "make cleanall\n	Removes downloaded and test files\n"
	@echo "make clean\n	Removes test files\n"

.PHONY: test
test:
	@make download
	@if [ ! -e "td-validate/td-validate" ]; then \
		cd td-validate; \
		make; \
		cd ..; \
	fi
	@./run_test.sh

.PHONY: download
download:
	@if [ ! -d "td-validate" ]; then \
		git clone  https://github.com/holgerdell/td-validate.git td-validate; \
	else \
		echo "Directory td-validate exists, not downloading ..."; \
	fi

.PHONY: cleanall
cleanall:
	@echo "Removing downloaded and test files ..."
	@rm -rf td-validate
	@rm -f test/clean/*.out.gr
	@rm -f test/dirty/*.out.gr
	@rm -f test/clean/*.gr.out
	@rm -f test/dirty/*.gr.out

.PHONY: clean
clean:
	@echo "Removing test files ..."
	@rm -f test/clean/*.out.gr
	@rm -f test/dirty/*.out.gr
	@rm -f test/clean/*.gr.out
	@rm -f test/dirty/*.gr.out

