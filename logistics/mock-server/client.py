"""
gRPC Demo Client - Warehouse Robot Telemetry

Demonstrates both a unary RPC (GetRobotStatus) and a bi-directional
streaming RPC (StreamTelemetry) against the warehouse mock server.

Usage:
    python logistics/mock-server/server.py   (in one terminal)
    python logistics/mock-server/client.py   (in another terminal)
"""

import grpc
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import warehouse_pb2
import warehouse_pb2_grpc


def generate_commands():
    """Yields three sample WarehouseCommands for the demo."""
    commands = [
        warehouse_pb2.WarehouseCommand(
            robot_id="ROBOT-P01-A",
            command=warehouse_pb2.COMMAND_MOVE,
            target=warehouse_pb2.Coordinates(x=15.0, y=12.0, z=0.0),
            timestamp_ms=int(time.time() * 1000),
        ),
        warehouse_pb2.WarehouseCommand(
            robot_id="ROBOT-P01-A",
            command=warehouse_pb2.COMMAND_PICK,
            target=warehouse_pb2.Coordinates(x=15.0, y=12.0, z=2.5),
            payload_sku="SKU-JACKET-BLK-L",
            timestamp_ms=int(time.time() * 1000),
        ),
        warehouse_pb2.WarehouseCommand(
            robot_id="ROBOT-P01-A",
            command=warehouse_pb2.COMMAND_CHARGE,
            target=warehouse_pb2.Coordinates(x=0.0, y=0.0, z=0.0),
            timestamp_ms=int(time.time() * 1000),
        ),
    ]

    for cmd in commands:
        cmd_name = warehouse_pb2.CommandType.Name(cmd.command)
        print(f"  [send] {cmd_name} -> target ({cmd.target.x}, {cmd.target.y})")
        yield cmd
        time.sleep(0.5)


def run():
    print("=" * 60)
    print("  OmniChain Retail Mesh - gRPC Warehouse Client")
    print("=" * 60)
    print()

    channel = grpc.insecure_channel("localhost:50051")
    stub = warehouse_pb2_grpc.WarehouseAutomationStub(channel)

    # -- Unary RPC: GetRobotStatus --
    print("  -- Unary RPC: GetRobotStatus --")
    print("  Single request, single response")
    print()

    try:
        response = stub.GetRobotStatus(
            warehouse_pb2.RobotRequest(robot_id="ROBOT-P01-A")
        )
        status_name = warehouse_pb2.RobotStatusEnum.Name(response.status)
        print(f"  Robot    : {response.robot_id}")
        print(f"  Position : ({response.position.x}, {response.position.y}, {response.position.z})")
        print(f"  Battery  : {response.battery_level:.0%}")
        print(f"  Status   : {status_name}")
    except grpc.RpcError as e:
        print(f"  Error: {e.details()}")
        return

    print()

    # -- Bi-directional Streaming: StreamTelemetry --
    print("  -- Bi-directional Streaming: StreamTelemetry --")
    print("  Stream of commands, stream of telemetry")
    print()

    try:
        responses = stub.StreamTelemetry(generate_commands())

        print()
        print("  -- Receiving telemetry stream --")
        print()

        for telemetry in responses:
            status_name = warehouse_pb2.RobotStatusEnum.Name(telemetry.status)
            print(
                f"  [recv] robot={telemetry.robot_id} "
                f"pos=({telemetry.position.x:.1f}, {telemetry.position.y:.1f}, {telemetry.position.z:.1f}) "
                f"battery={telemetry.battery_level:.0%} "
                f"speed={telemetry.speed_mps}m/s "
                f"status={status_name}"
            )

    except grpc.RpcError as e:
        print(f"  Stream error: {e.details()}")

    print()
    print("=" * 60)
    print("  Demo complete.")
    print("=" * 60)

    channel.close()


if __name__ == "__main__":
    run()
