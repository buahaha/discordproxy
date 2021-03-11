appname = discord-bridge
package = discordbridge
help:
	@echo "Makefile for $(appname)"

coverage:
	coverage run -m unittest discover && coverage html && coverage report

generate:
	python -m grpc_tools.protoc -I protobufs --python_out=discordproxy --grpc_python_out=discordproxy discord_api.proto
	sed -i -E 's/^import.*_pb2/from . \0/' discordproxy/*_pb2*.py
	protoc -I protobufs --doc_out=./docs --doc_opt=markdown,protobufs.md discord_api.proto
	make -C docs html

pylint:
	pylint $(package)

check_complexity:
	flake8 $(package) --max-complexity=10

flake8:
	flake8 $(package) --count
