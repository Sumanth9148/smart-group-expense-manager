from uuid import UUID
from app.bootstrap.container import build_services


def register(subparsers):
    group_parser = subparsers.add_parser("group")
    group_sub = group_parser.add_subparsers()

    create = group_sub.add_parser("create")
    create.add_argument("--name", required=True)
    create.set_defaults(func=create_group)

    add_member_cmd = group_sub.add_parser("add-member")
    add_member_cmd.add_argument("--group-id", required=True)
    add_member_cmd.add_argument("--user-id", required=True)
    add_member_cmd.set_defaults(func=add_member)


def create_group(args):
    services = build_services()
    group = services["group"].create_group(args.name)
    print(f"Group created: {group.id} | {group.name}")


def add_member(args):
    services = build_services()
    services["group"].add_member(
        UUID(args.group_id),
        UUID(args.user_id)
    )
    print("Member added to group")
