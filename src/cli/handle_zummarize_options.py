
def create_zummarize_options(opts):
    zummarize_cli = []
    for opt in opts.keys():
        if opts[opt] is True:
            zummarize_cli += ["--" + opt]
    return zummarize_cli
