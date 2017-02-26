try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    # tab completion
    import rlcompleter

    readline.parse_and_bind("tab: complete")

    # history()
    def history():
        for i in range(readline.get_current_history_length()):
            print(readline.get_history_item(i))
