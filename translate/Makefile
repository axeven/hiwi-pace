.PHONY: help
help:
	@echo "make help\n	Print this message\n"
	@echo "make test\n	Perform automatic tests on test instances\n"
	@echo "make download\n	Download test instances and td-validate\n"
	@echo "make cleanall\n	Removes downloaded and test files\n"
	@echo "make clean\n	Removes test files\n"

DIRS = test
OBJS = $(wildcard $(DIRS:=/*.uai))

.PHONY: test
test:
	@make download
	@for file in $(OBJS); do \
		$(b = $(basename $$file); \
		echo $(DIRS:=test/$b.gr); \	
	done
	#python3 translate.py testbed/instances/pace16/100/BlanusaSecondSnarkGraph.gr

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
	@rm -rf test

