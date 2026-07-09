# pytarize

pandas, pathlib, typer, pyyaml

pipeline: 
1. argument Parsing: 
> read default values -> read config -> overwrite with cli
2. TODO

## arguments
<div style="overflow-x:auto;">
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Name in config</th>
            <th>Type</th>
            <th>Description</th>
            <th>Usable in</th>
            <th>Config example</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <code style="white-space: nowrap;">--zummarizepath</code><br>
                <code>--zrp</code>
            </td>
            <td><code>zummarize_path</code></td>
            <td><code>path</code></td>
            <td style="min-width:350px">
                Path to zummarize executable.<br>
                Should ideally be specified in the highest order config.<br>
                This argument is needed when a folder in <code>--logpaths</code> or <code>--rlogpaths</code> does not contain a zummary file but logfiles or if this script is called with arguments that are handled by the zummarize script.<br>Internaly this argument is a string which is interpreted by bash.
            </td>
            <td style="min-width:100px">All config types</td>
            <td style="white-space: nowrap">
                <code>zummarize_path: "/path/to/zummarize"</code>
            </td>
        </tr>
        <tr>
            <td><code>--logpaths</code><br>
            <code>--lps</code></td>
            <td><code>log_paths</code></td>
            <td><code>list[path]<code></td>
            <td>List of paths that lead to folders containing the logfiles.<br>
            Duplicate paths are removed.<br> If a folder does not contain a zummary file but logfiles the <code>--zummarizepath</code> argument is required.<br>
            Internaly this argument is a string which is interpreted by bash.</td>
            <td>All config types</td>
            <td><pre><code>log_paths:
  - "path1"
  - "path2"</code></pre></td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;"></code></td>
            <td><code></code></td>
            <td><code><code></td>
            <td></td>
            <td></td>
            <td><pre><code></code></pre></td>
        </tr>
    </tbody>
</table>
</div>