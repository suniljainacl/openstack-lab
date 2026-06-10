import argparse
import openstack


def instance_snapshot(args):
    print(f"Connecting to OpenStack...")
    conn = openstack.connect()
    print(f"Connected!")
    print(f"Looking for instance: {args.name}")
    server = conn.compute.find_server(args.name)
    if not server:
        print(f"Error: Instance '{args.name}' not found.")
        return
    print(f"Found it! ID: {server.id}, Status: {server.status}")
    print(f"Creating snapshot '{args.snapshot_name}'...")
    image = conn.compute.create_server_image(server.id, args.snapshot_name)
    print(f"Snapshot created! Image ID: {image.id}")


def instance_restore(args):
    print(f"Connecting to OpenStack...")
    conn = openstack.connect()
    print(f"Connected!")
    print(f"Looking for snapshot image: {args.snapshot_name}")
    image = conn.compute.find_image(args.snapshot_name)
    if not image:
        print(f"Error: Snapshot '{args.snapshot_name}' not found.")
        return
    print(f"Found snapshot! ID: {image.id}")
    print(f"Finding flavor...")
    flavor = conn.compute.find_flavor("m1.tiny")
    print(f"Using flavor: {flavor.name}")
    print(f"Launching new instance '{args.name}' from snapshot...")
    server = conn.compute.create_server(
        name=args.name,
        image_id=image.id,
        flavor_id=flavor.id,
        networks=[{"uuid": conn.network.find_network("test-net").id}]
    )
    print(f"Instance created! ID: {server.id}, Status: {server.status}")
    print(f"Note: Check status with: openstack server list")


def volume_snapshot(args):
    print(f"Connecting to OpenStack...")
    conn = openstack.connect()
    print(f"Connected!")
    print(f"Looking for volume: {args.name}")
    volume = conn.block_storage.find_volume(args.name)
    if not volume:
        print(f"Error: Volume '{args.name}' not found.")
        return
    print(f"Found it! ID: {volume.id}, Status: {volume.status}")
    print(f"Creating snapshot '{args.snapshot_name}'...")
    snapshot = conn.block_storage.create_snapshot(
        volume_id=volume.id,
        name=args.snapshot_name,
        force=True
    )
    print(f"Snapshot created!")
    print(f"  Snapshot ID : {snapshot.id}")
    print(f"  Size        : {snapshot.size}GB")
    print(f"  Status      : {snapshot.status}")


def volume_restore(args):
    print(f"Connecting to OpenStack...")
    conn = openstack.connect()
    print(f"Connected!")
    print(f"Looking for snapshot: {args.snapshot_name}")
    snapshot = conn.block_storage.find_snapshot(args.snapshot_name)
    if not snapshot:
        print(f"Error: Snapshot '{args.snapshot_name}' not found.")
        return
    print(f"Found snapshot! ID: {snapshot.id}, Size: {snapshot.size}GB")
    print(f"Creating new volume '{args.name}' from snapshot...")
    volume = conn.block_storage.create_volume(
        name=args.name,
        snapshot_id=snapshot.id,
        size=snapshot.size
    )
    print(f"Volume restored!")
    print(f"  Volume ID : {volume.id}")
    print(f"  Size      : {volume.size}GB")
    print(f"  Status    : {volume.status}")


# ── Argparse setup ──

parser = argparse.ArgumentParser(description="OpenStack Snapshot/Restore CLI")
subparsers = parser.add_subparsers(dest="resource", help="Resource type")
subparsers.required = True

# ── instance subcommand ──
instance_parser = subparsers.add_parser("instance", help="Instance operations")
instance_sub = instance_parser.add_subparsers(dest="action", help="Action")
instance_sub.required = True

snap = instance_sub.add_parser("snapshot", help="Snapshot an instance")
snap.add_argument("--name", required=True, help="Instance name")
snap.add_argument("--snapshot-name", required=True, help="Snapshot name")
snap.set_defaults(func=instance_snapshot)

restore = instance_sub.add_parser("restore", help="Restore an instance")
restore.add_argument("--snapshot-name", required=True, help="Snapshot to restore from")
restore.add_argument("--name", required=True, help="New instance name")
restore.set_defaults(func=instance_restore)

# ── volume subcommand ──
volume_parser = subparsers.add_parser("volume", help="Volume operations")
volume_sub = volume_parser.add_subparsers(dest="action", help="Action")
volume_sub.required = True

vol_snap = volume_sub.add_parser("snapshot", help="Snapshot a volume")
vol_snap.add_argument("--name", required=True, help="Volume name")
vol_snap.add_argument("--snapshot-name", required=True, help="Snapshot name")
vol_snap.set_defaults(func=volume_snapshot)

vol_restore = volume_sub.add_parser("restore", help="Restore a volume from snapshot")
vol_restore.add_argument("--snapshot-name", required=True, help="Snapshot to restore from")
vol_restore.add_argument("--name", required=True, help="New volume name")
vol_restore.set_defaults(func=volume_restore)

# ── Run ──
args = parser.parse_args()
args.func(args)
