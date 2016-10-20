.PHONY: help
help:
	@echo "make help\n	Print this message\n"
	@echo "make test\n	Perform automatic tests on test instances\n"
	@echo "make download\n	Download task instances and td-validate\n"
	@echo "make runtask\n	Translate and validate taks instances\n"
	@echo "make cleanall\n	Removes downloaded and test files\n"
	@echo "make clean\n	Removes test output files\n"

TESTDIR = test
TESTOBJS = $(wildcard $(TESTDIR:=/*.uai))
TDVALIDATE = ./td-validate/td-validate

.PHONY: test
test:
	@make download
	@if [ ! -e "td-validate/td-validate" ]; then \
		cd td-validate; \
		make; \
		cd ..; \
	fi
	@./run_test.sh

.PHONY: runtask
runtask:
	@make download
	@if [ ! -e "td-validate/td-validate" ]; then \
		cd td-validate; \
		make; \
		cd ..; \
	fi
	@./run_task.sh

.PHONY: download
download:
	@if [ ! -d "input" ]; then \
		mkdir input ;\
	fi
	@if [ ! -e "input/input1.tgz" ]; then \
		echo "Downloading instances ... (1/3)"; \
		wget http://www.hlt.utdallas.edu/~vgogate/uai14-competition/files/MMAP_UAI2014.tar.gz -O input/input1.tgz; \
	fi
	@if [ ! -e "input/input2.tgz" ]; then \
		echo "Downloading instances ... (2/3)"; \
		wget http://www.hlt.utdallas.edu/~vgogate/uai14-competition/files/PR_prob.tar.gz -O input/input2.tgz; \
	fi
	@if [ ! -e "input/input3.tgz" ]; then \
		echo "Downloading instances ... (3/3)"; \
		wget http://www.hlt.utdallas.edu/~vgogate/uai14-competition/files/MAR_prob.tar.gz -O input/input3.tgz; \
	fi
	@if [ ! -d "input/input1" ]; then \
		echo "Extracting instances ... (1/3)"; \
		tar -xzf input/input1.tgz -C input; \
		mv input/MMAP input/input1; \
	fi
	@if [ ! -d "input/input2" ]; then \
		echo "Extracting instances ... (2/3)"; \
		mkdir input/input2; \
		tar -xzf input/input2.tgz -C input/input2; \
	fi
	@if [ ! -d "input/input3" ]; then \
		echo "Extracting instances ... (3/3)"; \
		mkdir input/input3; \
		tar -xzf input/input3.tgz -C input/input3; \
	fi
	@if [ ! -d "td-validate" ]; then \
		echo "Downloading td-validate ..."; \
		git clone https://github.com/holgerdell/td-validate td-validate; \
	fi

.PHONY: cleanall
cleanall:
	@echo "Removing downloaded and test files ..."
	@rm -rf td-validate
	@rm -rf input

.PHONY: clean
clean:
	@echo "Removing test output ..."
	@rm test/*.out.gr

