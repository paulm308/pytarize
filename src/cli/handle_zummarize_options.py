
def create_zummarize_options(opts):
    """
    Creates a option string --option for all options in opts.

    Parameters:
    opts: The zummarize specific options.

    Returns:
    list[str]: The option strings.
    """
    zummarize_cli = []
    for opt in opts.keys():
        if opt == "verbose" and opts[opt] is not None:
            zummarize_cli += ["-v", str(opts[opt])]
        elif opts[opt] is True:
            zummarize_cli += ["--" + opt]
    return zummarize_cli
