generate:
	python -m grpc_tools.protoc -I discordproxy/protobufs --python_out=discordproxy/grpc_sync --grpc_python_out=discordproxy/grpc_sync discord_api.proto
	sed -i -E 's/^import.*_pb2/from . \0/' discordproxy/grpc_sync/*.py
	python -m grpc_tools.protoc -I discordproxy/protobufs --python_out=discordproxy/grpc_async --grpclib_python_out=discordproxy/grpc_async discord_api.proto
	sed -i -E 's/^import.*_pb2/from . \0/' discordproxy/grpc_async/*.py
