#!/bin/bash

protoc --python_out="." ./*.proto

# fix relative imports
sed -i 's\import customer_pb2\from . import customer_pb2\g' *.py
