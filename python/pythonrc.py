try:
    import readline
except ImportError:
    try:
        import pyreadline as readline
    except ImportError:
        print("Module readline not available.")
else:
    # tab completion
    import rlcompleter
    readline.parse_and_bind("tab: complete")

    # version()
    from platform import python_version as version

    # apropos()
    from pydoc import apropos

    # history()
    def history():
        for i in range(readline.get_current_history_length()):
            print(readline.get_history_item(i))
