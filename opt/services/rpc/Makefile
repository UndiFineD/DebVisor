PROTO_DIR := proto
GEN_DIR := gen
PROTO_SRC := $(PROTO_DIR)/debvisor.proto

PYTHON ?= python3

.PHONY: all clean python

all: python

python: $(GEN_DIR)/debvisor_pb2.py $(GEN_DIR)/debvisor_pb2_grpc.py

$(GEN_DIR)/debvisor_pb2.py $(GEN_DIR)/debvisor_pb2_grpc.py: $(PROTO_SRC)
	@mkdir -p $(GEN_DIR)
	$(PYTHON) -m grpc_tools.protoc \
		-I$(PROTO_DIR) \
		--python_out=$(GEN_DIR) \
		--grpc_python_out=$(GEN_DIR) \
		$(PROTO_SRC)

clean:
	rm -rf $(GEN_DIR)
