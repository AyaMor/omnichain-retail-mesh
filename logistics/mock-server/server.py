"""
gRPC Mock Server - Warehouse Robot Automation

Implements the WarehouseAutomation service defined in contracts/warehouse.proto.
Returns simulated telemetry data for demonstration purposes.

Stub generation (run once from project root):
    python -m grpc_tools.protoc -Ilogistics/contracts \
        --python_out=logistics/mock-server \
        --grpc_python_out=logistics/mock-server \
        logistics/contracts/warehouse.proto

Run: python logistics/mock-server/server.py
"""

import grpc
from concurrent import futures
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import warehouse_pb2
import warehouse_pb2_grpc


# ---------------------------------------------------------------------------
# Service implementation
# ---------------------------------------------------------------------------

class WarehouseAutomationServicer(warehouse_pb2_grpc.WarehouseAutomationServicer):

    def StreamTelemetry(self, request_iterator, context):
        """
        Bi-directional streaming RPC. For each incoming command, emits
        three telemetry events simulating the robot executing the command.
        """
        print("  [stream] Bi-directional stream opened")

        for command in request_iterator:
            cmd_name = warehouse_pb2.CommandType.Name(command.command)
            print(f"  [recv] {cmd_name} for robot {command.robot_id}")

            for step in range(3):
                telemetry = warehouse_pb2.RobotTelemetry(
                    robot_id=command.robot_id,
                    position=warehouse_pb2.Coordinates(
                        x=command.target.x * (step + 1) / 3.0 if command.target else 0.0,
                        y=command.target.y * (step + 1) / 3.0 if command.target else 0.0,
                        z=command.target.z if command.target else 0.0,
                    ),
                    battery_level=round(0.95 - (step * 0.02), 2),
                    status=(warehouse_pb2.ROBOT_STATUS_MOVING if step < 2
                            else warehouse_pb2.ROBOT_STATUS_IDLE),
                    speed_mps=round(1.5 - (step * 0.5), 1),
                    timestamp_ms=int(time.time() * 1000),
                )

                print(f"  [send] Telemetry [{step+1}/3]: "
                      f"robot={telemetry.robot_id} "
                      f"pos=({telemetry.position.x:.1f}, {telemetry.position.y:.1f}) "
                      f"battery={telemetry.battery_level}")

                yield telemetry
                time.sleep(0.3)

        print("  [stream] Bi-directional stream closed")

    def GetRobotStatus(self, request, context):
        """Unary RPC returning a static telemetry snapshot."""
        print(f"  [status] Request for robot {request.robot_id}")

        return warehouse_pb2.RobotTelemetry(
            robot_id=request.robot_id,
            position=warehouse_pb2.Coordinates(x=12.5, y=3.2, z=0.0),
            battery_level=0.87,
            status=warehouse_pb2.ROBOT_STATUS_PICKING,
            speed_mps=0.0,
            timestamp_ms=int(time.time() * 1000),
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    warehouse_pb2_grpc.add_WarehouseAutomationServicer_to_server(
        WarehouseAutomationServicer(), server
    )

    PORT = 50051
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()

    print("=" * 60)
    print("  RetailSync - gRPC Warehouse Automation")
    print("=" * 60)
    print(f"  gRPC endpoint  : localhost:{PORT}")
    print(f"  Protocol       : gRPC / HTTP/2 / Protobuf")
    print(f"  Service        : WarehouseAutomation")
    print(f"  RPCs           : StreamTelemetry (bi-directional)")
    print(f"                   GetRobotStatus (unary)")
    print("=" * 60)
    print()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n  Server shutting down...")
        server.stop(0)


if __name__ == "__main__":
    serve()
