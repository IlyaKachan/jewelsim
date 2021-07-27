def add_click_commands(*args):
    def decorator(click_group):
        for cmd in args:
            click_group.add_command(cmd)
        return click_group

    return decorator
