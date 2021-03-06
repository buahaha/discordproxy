appname = discord-bridge
package = discordbridge
help:
	@echo "Makefile for $(appname)"

coverage:
	coverage run -m unittest discover && coverage html && coverage report

generate:
	python -m grpc_tools.protoc -I discordproxy/protobufs --python_out=discordproxy/grpc_sync --grpc_python_out=discordproxy/grpc_sync discord_api.proto
	sed -i -E 's/^import.*_pb2/from . \0/' discordproxy/grpc_sync/*.py
	python -m grpc_tools.protoc -I discordproxy/protobufs --python_out=discordproxy/grpc_async --grpclib_python_out=discordproxy/grpc_async discord_api.proto
	sed -i -E 's/^import.*_pb2/from . \0/' discordproxy/grpc_async/*.py

pylint:
	pylint $(package)

check_complexity:
	flake8 $(package) --max-complexity=10

flake8:
	flake8 $(package) --count
