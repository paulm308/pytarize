# pytarize

pandas, pathlib, typer, pyyaml

pipeline: 
1. argument Parsing: 
> read default values -> read config -> overwrite with cli
2. TODO

## Path arguments
All of the following arguments take paths or whitespace separated lists of paths as input. Internally the input is treated as a string which is interpreted by bash. These arguments can be used in all config types but should ideally be used in the highest order config since they're not dependent on the type of the plot.
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
    <tbody style="vertical-align: top;">
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
                This argument is needed when a folder in <code>--logpaths</code> or <code>--rlogpaths</code> does not contain a zummary file but logfiles or if this script is called with arguments that are handled by the zummarize script.
            </td>
            <td style="min-width:100px">All config types</td>
            <td><pre>
                <code style="white-space: nowrap;">zummarize_path: "/path/to/zummarize"</code>
            </pre></td>
        </tr>
        <tr>
            <td><code>--logpaths</code><br>
            <code>--lps</code></td>
            <td><code>log_paths</code></td>
            <td><code>list[path]<code></td>
            <td>List of paths that lead to folders containing the logfiles.<br>
            Duplicate paths are removed.<br> If a folder does not contain a zummary file but logfiles the <code>--zummarizepath</code> argument is required.
            </td>
            <td>All config types</td>
            <td><pre><code>log_paths:
  - "path1"
  - "path2"</code></pre></td>
        </tr>
        <tr>
            <td><code>--rlogpaths</code><br>
            <code>--rlps</code></td>
            <td><code>r_log_paths</code></td>
            <td><code>list[path]<code></td>
            <td>List of root paths that are recursively searched for folders containing logfiles.<br>
            Duplicate paths are removed.<br> If a folder does not contain a zummary file but logfiles the <code>--zummarizepath</code> argument is required.</td>
            <td>All config types</td>
            <td><pre><code>r_log_paths:
  - "path1"
  - "path2"</code></pre></td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--configpaths</code><br>
            <code>--cps</code></td>
            <td><code>config_paths</code></td>
            <td><code>list[path]<code></td>
            <td>List of paths that lead to configfiles.<br>Configs are additively combined:<ul><li><code>dict</code> are merged</li><li><code>list</code>, <code>int</code> and <code>float</code> are overwritten</li><li><code>bool</code> are combined using OR</li></ul>If this argument only contains a single path that leads to a "base config" (a config that only specifies path arguments like <code>zummarize_path</code>) the <code>config_path</code> given in the config is applied. After the configs are combined the cli arguments are applied discriminatively, which for the most part is the same as the combination of configs except that bools are combined using XOR.<br>The representation in the config is not the same as the cli version! The config version maps config_paths to each plot type and therefore has the type: <code>dict[str, list[path]]</code>.</td>
            <td>All config types</td>
            <td><pre><code>config_paths:
  lineplot:
    - "path1"
    - "path2"
  scatterplot:
    - "path1"
    - "path2"
  combinedplot:
    - "path1"
    - "path2"</code></pre></td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--save-config</code><br>
            <code>--sc</code></td>
            <td>None</td>
            <td><code>path<code></td>
            <td>Path to the output config.<br> The created config contains the current state of all plot specific arguments (state after combining defaults, all configs and cli arguments).</td>
            <td>None</td>
            <td>None</td>
        </tr>
    </tbody>
</table>
</div>