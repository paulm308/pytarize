# pytarize

pandas, pathlib, typer, pyyaml

pipeline: 
1. argument Parsing: 
> read default values -> read config -> overwrite with cli
2. TODO

## Path arguments
All of the following arguments take paths or whitespace separated lists of paths as input. Internally the input is treated as a string which is interpreted by bash. These arguments can be used in all config types but should ideally be used in the highest order config since they're not dependent on the type of the plot.
<table>
    <thead>
        <tr>
            <th width="10%">Name</th>
            <th width="14%">Name in config</th>
            <th width="8%">Type</th>
            <th width="48%">Description</th>
            <th width="20%">Config example</th>
        </tr>
    </thead>
    <tbody>
        <tr valign="top">
            <td valign="top">
                <code>--zummarizepath</code><br>
                <code>--zrp</code>
            </td>
            <td valign="top"><code>zummarize_path</code></td>
            <td valign="top"><code>path</code></td>
            <td valign="top">
                Path to zummarize executable.<br>
                Should ideally be specified in the highest order config.<br>
                This argument is needed when a folder in <code>--logpaths</code> or <code>--rlogpaths</code> does not contain a zummary file but logfiles or if this script is called with arguments that are handled by the zummarize script.
            </td>
            <td valign="top"><pre><code>zummarize_path: "path"</code></pre></td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--logpaths</code><br>
            <code>--lps</code></td>
            <td valign="top"><code>log_paths</code></td>
            <td valign="top"><code>list[path]</code></td>
            <td valign="top">List of paths that lead to folders containing the logfiles.<br>
            Duplicate paths are removed.<br> If a folder does not contain a zummary file but logfiles the <code>--zummarizepath</code> argument is required.
            </td>
            <td valign="top"><pre><code>log_paths:
  - "path1"
  - "path2"</code></pre></td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--rlogpaths</code><br>
            <code>--rlps</code></td>
            <td valign="top"><code>r_log_paths</code></td>
            <td valign="top"><code>list[path]</code></td>
            <td valign="top">List of root paths that are recursively searched for folders containing logfiles.<br>
            Duplicate paths are removed.<br> If a folder does not contain a zummary file but logfiles the <code>--zummarizepath</code> argument is required.</td>
            <td valign="top"><pre><code>r_log_paths:
  - "path1"
  - "path2"</code></pre></td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--configpaths</code><br>
            <code>--cps</code></td>
            <td valign="top"><code>config_paths</code></td>
            <td valign="top"><code>list[path]</code></td>
            <td valign="top">List of paths that lead to configfiles.<br>Configs are additively combined:<ul><li><code>dict</code> are merged</li><li><code>list</code>, <code>int</code> and <code>float</code> are overwritten</li><li><code>bool</code> are combined using OR</li></ul>If this argument only contains a single path that leads to a "base config" (a config that only specifies path arguments like <code>zummarize_path</code>) the <code>config_path</code> given in the config is applied. After the configs are combined the cli arguments are applied discriminatively, which for the most part is the same as the combination of configs except that bools are combined using XOR.<br>The representation in the config is not the same as the cli version! The config version maps config_paths to each plot type and therefore has the type: <code>dict[str, list[path]]</code>.</td>
            <td valign="top"><pre><code>config_paths:
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
        <tr valign="top">
            <td valign="top"><code>--save-config</code><br>
            <code>--sc</code></td>
            <td valign="top">None</td>
            <td valign="top"><code>path</code></td>
            <td valign="top">Path to the output config.<br> The created config contains the current state of all plot-specific arguments (state after combining defaults, all configs and cli arguments).</td>
            <td valign="top">None</td>
        </tr>
    </tbody>
</table>

## zummarize arguments
All of the following arguments are not processed by pytarize. If any of the following arguments are used, the zummarize script is called using `--zummarizepath` with the paths given in `--logpaths`, the resolved paths from `--rlogpaths` and the specified zummarize arguments. These arguments can't be used in any config type.

<div style="overflow-x:auto;">
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody style="vertical-align: top;">
        <tr>
            <td><code style="white-space: nowrap;">-v</code></td>
            <td><code>int</code></td>
            <td>increase verbose level (maximum 3, default 0)</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--force</code>
            <code>-f</code></td>
            <td><code>int</code></td>
            <td>recompute zummaries (do not read dir/zummary files)</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--ignore</code>
            <code>-i</code></td>
            <td><code>bool</code></td>
            <td>ignore mismatching limits and bounds</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--just</code>
            <code>-j</code></td>
            <td><code>bool</code></td>
            <td>assume terminated are just solved (unsat)</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--no-warnings</code>
            <code>-n</code></td>
            <td><code>bool</code></td>
            <td>disables warnings</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--all</code>
            <code>-a</code></td>
            <td><code>bool</code></td>
            <td>report all column and rows (even with zero entries)</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--deep</code>
            <code>-d</code></td>
            <td><code>bool</code></td>
            <td>report goes over unsolved instances only (sorted by deep)</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--rank</code>
            <code>-r</code></td>
            <td><code>bool</code></td>
            <td>print number of times benchmark has been solved</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--unsolved</code></td>
            <td><code>bool</code></td>
            <td>print unsolved (never solved) instances</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--solved</code></td>
            <td><code>bool</code></td>
            <td>print all at least once solved instances</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--filter</code></td>
            <td><code>bool</code></td>
            <td>filter out solved in comparison</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--cmp</code></td>
            <td><code>bool</code></td>
            <td>compare two runs</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--no-write</code></td>
            <td><code>bool</code></td>
            <td>do not write generated zummaries</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--no-bounds</code></td>
            <td><code>bool</code></td>
            <td>do not print bounds</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--force-real</code></td>
            <td><code>bool</code></td>
            <td>force real time zummaries</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--force-time</code></td>
            <td><code>bool</code></td>
            <td>force process time zummaries
            </td>
        </tr>
    </tbody>
</table>
</div>

### Special cases
These arguments are processed by pytarize. Using these arguments alone will not result in a call to the zummarize script, but if any of the above arguments is used as well zummarize is called including the arguments from below.

<div style="overflow-x:auto;">
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody style="vertical-align: top;">
        <tr>
            <td><code style="white-space: nowrap;">--sat</code>
            <code>-s</code></td>
            <td><code>bool</code></td>
            <td>report goes over satisfiable instances only</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--unsat</code>
            <code>-u</code></td>
            <td><code>int</code></td>
            <td>report goes over unsatisfiable instances only
            </td>
        </tr>
    </tbody>
</table>
</div>

## plot-specific arguments


<table>
    <thead>
        <tr>
            <th width="15%">Name</th>
            <th width="15%">Name in config</th>
            <th width="10%">Type</th>
            <th width="10%">Plot type</th>
            <th width="50%">Config example</th>
        </tr>
    </thead>
    <tbody>
        <tr valign="top">
            <td valign="top"><code>--colors</code></td>
            <td valign="top"><code>colors</code></td>
            <td valign="top"><code>list[str]</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>colors:
  - "black"
  - "#ff0042"</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">List of colors given in hex notation or name in color table.<br>The number of <code>--colors</code> and <code>--markers</code> should ideally be coprime.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--markers</code></td>
            <td valign="top"><code>markers</code></td>
            <td valign="top"><code>list[str]</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>markers:
  - "s"
  - - "s"
    - true</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">List of <a href="https://matplotlib.org/stable/api/markers_api.html">matplotlib markers</a><br>The number of <code>--colors</code> and <code>--markers</code> should ideally be coprime. The config representation of markers is <code>list[str | list[str | bool]]</code>, a 2D list, where the first argument in the sublist is the <a href="https://matplotlib.org/stable/api/markers_api.html">marker</a> and the second is an option to create a hollow marker. The example creates a square marker and a hollow square marker.
            </td>
        </tr>
    </tbody>
</table>

