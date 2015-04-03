.PHONY: all sl_builder builder

all: builder sl_builder

builder:
	docker build -t onedata/builder:v8 -f builder .

sl_builder:
	docker build -t onedata/sl_builder:v2 -f sl_builder .


