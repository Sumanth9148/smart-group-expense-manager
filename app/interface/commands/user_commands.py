from app.bootstrap.container import build_services


def register(subparsers):
    user_parser = subparsers.add_parser("user")
    user_sub = user_parser.add_subparsers()

    create = user_sub.add_parser("create")
    create.add_argument("--name", required=True)
    create.set_defaults(func=create_user)


def create_user(args):
    services = build_services()
    user = services["user"].create_user(args.name)
    print(f"User created: {user.id} | {user.name}")
