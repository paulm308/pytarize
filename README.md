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
            <th width="15%">Name</th>
            <th width="15%">Name in config</th>
            <th width="10%">Type</th>
            <th width="10%">Plot type</th>
            <th width="50%">Config example</th>
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
            <td valign="top">All</td>
            <td valign="top"><pre><code>zummarize_path: "path"</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Path to zummarize executable.<br>
                Should ideally be specified in the highest order config.<br>
                This argument is needed when a folder in <code>--logpaths</code> or <code>--rlogpaths</code> does not contain a zummary file but logfiles or if this script is called with arguments that are handled by the zummarize script.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--logpaths</code><br>
            <code>--lps</code></td>
            <td valign="top"><code>log_paths</code></td>
            <td valign="top"><code>list[path]</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>log_paths:
  - "path1"
  - "path2"</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">List of paths that lead to folders containing the logfiles.<br>
            Duplicate paths are removed.<br> If a folder does not contain a zummary file but logfiles the <code>--zummarizepath</code> argument is required.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--rlogpaths</code><br>
            <code>--rlps</code></td>
            <td valign="top"><code>r_log_paths</code></td>
            <td valign="top"><code>list[path]</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>r_log_paths:
  - "path1"
  - "path2"</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">List of root paths that are recursively searched for folders containing logfiles.<br>
            Duplicate paths are removed.<br> If a folder does not contain a zummary file but logfiles the <code>--zummarizepath</code> argument is required.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--configpaths</code><br>
            <code>--cps</code></td>
            <td valign="top"><code>config_paths</code></td>
            <td valign="top"><code>list[path]</code></td>
            <td valign="top">All</td>
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
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">List of paths that lead to configfiles.<br>Configs are additively combined:<ul><li><code>dict</code> are merged</li><li><code>list</code>, <code>int</code> and <code>float</code> are overwritten</li><li><code>bool</code> are combined using OR</li></ul>If this argument only contains a single path that leads to a "base config" (a config that only specifies path arguments like <code>zummarize_path</code>) the <code>config_path</code> given in the config is applied. After the configs are combined the cli arguments are applied discriminatively, which for the most part is the same as the combination of configs except that bools are combined using XOR.<br>The representation in the config is not the same as the cli version! The config version maps config_paths to each plot type and therefore has the type: <code>dict[str, list[path]]</code>.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--save-config</code><br>
            <code>--sc</code></td>
            <td valign="top">None</td>
            <td valign="top"><code>path</code></td>
            <td valign="top">All</td>
            <td valign="top">None</td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Path to the output config.<br> The created config contains the current state of all plot-specific arguments (state after combining defaults, all configs and cli arguments).
            </td>
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
These arguments are processed by pytarize. Using these arguments alone will not result in a call to the zummarize script, but if any of the above arguments is used as well, zummarize is called including the arguments from below.

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
            <td><code>bool</code></td>
            <td>report goes over unsatisfiable instances only
            </td>
        </tr>
    </tbody>
</table>
</div>

## other global options
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
            <td><code style="white-space: nowrap;">--time</code>
            <td><code>bool</code></td>
            <td>Use process time</td>
        </tr>
        <tr>
            <td><code style="white-space: nowrap;">--real</code>
            <td><code>bool</code></td>
            <td>Use real time (default)
            </td>
        </tr>
    </tbody>
</table>

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
        <tr valign="top">
            <td valign="top"><code>--hollow</code></td>
            <td valign="top"><code>hollow</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>hollow: true</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Option that that creates hollow markers. Only markers that have an inner surface and are not specificaly set to hollow by the <code>markers</code> option are affected.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--cactus</code></td>
            <td valign="top"><code>cactus</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">lineplot</td>
            <td valign="top"><pre><code>cactus: true</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Generates cactus plot (cdf is default).
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--show-solved</code></td>
            <td valign="top"><code>show_solved</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>show_solved: true</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Shows solved count in legend.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--center</code></td>
            <td valign="top"><code>center</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>center: true</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Centers the legend vertically.<br>
            The default is the right center, but if <code>--cactus</code> is used the legend is centered to the left side.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--legendloc</code></td>
            <td valign="top"><code>legendloc</code></td>
            <td valign="top"><code>str</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>center: true</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Set the location of the legend. Input is limited to the following options: 'upper left', 'upper center', 'upper right', 'center left', 'center', 'center right', 'lower left', 'lower center', 'lower right'.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--ymin</code></td>
            <td valign="top"><code>ymin</code></td>
            <td valign="top"><code>float | int</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>ymin: 42</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Set the minimum y-axis value.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--xmin</code></td>
            <td valign="top"><code>xmin</code></td>
            <td valign="top"><code>float | int</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>xmin: 42</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Set the minimum x-axis value.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--ymax</code></td>
            <td valign="top"><code>ymax</code></td>
            <td valign="top"><code>float | int</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>ymax: 42</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Set the maximum y-axis value.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--xmax</code></td>
            <td valign="top"><code>xmax</code></td>
            <td valign="top"><code>float | int</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>xmax: 42</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Set the maximum x-axis value.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--xlegend</code></td>
            <td valign="top"><code>xlegend</code></td>
            <td valign="top"><code>float</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>xlegend: 0.42</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Set the x-value of the position of the top left corner of the legend. Only use values between 0.0 and 1.0.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--ylegend</code></td>
            <td valign="top"><code>ylegend</code></td>
            <td valign="top"><code>float</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>ylegend: 0.42</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Set the y-value of the position of the top-left corner of the legend. Only use values between 0.0 and 1.0.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--limit</code></td>
            <td valign="top"><code>limit</code></td>
            <td valign="top"><code>(float | int) | bool</code></td>
            <td valign="top">All*</td>
            <td valign="top"><pre><code>limit: true</code></pre>
            <pre><code>limit: 42</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Plots a limit line at the given y-value (only for <code>lineplot</code> and <code>combinedplot</code>). If the <code>scatterplot</code> command is used, this option (<code>bool</code>) plots lines at the timeout values given in the zummarys.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--lines</code></td>
            <td valign="top"><code>lines</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>lines: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Plot the indicator lines specified by <code>indicator_lines</code> in the config
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--line-segments</code></td>
            <td valign="top"><code>line_segments</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>line_segments: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Plot the indicator line segments specified by <code>indicator_line_segments</code> in the config. This can also be used to create small plots.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--grid</code></td>
            <td valign="top"><code>grid</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>grid: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Plot the grid specified by <code>grid_kwargs</code> in the config.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--xlog</code></td>
            <td valign="top"><code>xlog</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>xlog: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Changes x-scale from linear to logarithmic.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--ylog</code></td>
            <td valign="top"><code>ylog</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>ylog: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Changes y-scale from linear to logarithmic.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--xlabel</code></td>
            <td valign="top"><code>xlabel</code></td>
            <td valign="top"><code>str</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>xlabel: "\textbf{test}"</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Set the label of the x-axis. If the <code>--latex</code> option is active, the text is interpreted by latex and the output of the example is <b>test</b> in standard latex font.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--ylabel</code></td>
            <td valign="top"><code>ylabel</code></td>
            <td valign="top"><code>str</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>ylabel: "\textbf{test}"</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Set the label of the y-axis. If the <code>--latex</code> option is active, the text is interpreted by latex and the output of the example is <b>test</b> in standard latex font.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--plain</code></td>
            <td valign="top"><code>plain</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>plain: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Disables the scientific notation for major ticks. The default is: <code>10<sup>3</sup></code> but if this option is used: <code>1000</code>.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--square-box</code></td>
            <td valign="top"><code>square_box</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>square_box: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Set equal aspect ratio. <b>This only works if both axis have the same scale!</b>
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--output</code><br>
            <code>-o</code></td>
            <td valign="top"><code>output</code></td>
            <td valign="top"><code>path</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>output: "path"</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Set the location, name and type of the output. Matplotlib supports a lot of types, see <a href="https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html">savefig documentation</a>.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--title</code><br>
            <code>-t</code></td>
            <td valign="top"><code>title</code></td>
            <td valign="top"><code>str</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>title: "\textbf{test}"</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Set the label of the title of the plot. If the <code>--latex</code> option is active, the text is interpreted by latex and the output of the example is <b>test</b> in standard latex font.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--latex</code></td>
            <td valign="top"><code>latex</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>latex: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Enable latex text rendering for all text displayed in the plot. Documentation: <a href=https://matplotlib.org/stable/users/explain/customizing.html>rcParams documentation</a> and search for <code>usetex</code>.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--font-family</code></td>
            <td valign="top"><code>font_family</code></td>
            <td valign="top"><code>str</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>font_family: "serif"</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Change latex font-family, default is 'serif', options: 'serif', 'sans-serif', 'monospace', 'cursive', 'fantasy'. Documentation: <a href=https://matplotlib.org/stable/users/explain/customizing.html>rcParams documentation</a> and search for <code>font.family</code>.
            </td>
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--latex-preamble</code></td>
            <td valign="top"><code>latex_preamble</code></td>
            <td valign="top"><code>str</code></td>
            <td valign="top">All</td>
            <td valign="top"><pre><code>latex_preamble:
"\usepackage{lmodern}"</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Use this to import latex packages. Documentation: <a href=https://matplotlib.org/stable/users/explain/customizing.html>rcParams documentation</a> and search for <code>text.latex.preamble</code>.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--create-solver-style</code></td>
            <td valign="top"><code>create_solver_style</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">lineplot<br>combinedplot</td>
            <td valign="top"><pre><code>create_solver_style: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Generates the <code>solver_style</code> dictionary in the config. This option utilizes a compressed version of the <code>solver_style</code> dictionary, by combining: <code>colors</code>, <code>markers</code>, <code>universal_solver_style</code> and <code>specific_solver_style</code> arguments in the config to generate the <code>solver_style</code> dictionary. To save the generated <code>solver_style</code> dictionary, <code>--save-config</code> is needed. <code>universal_solver_style</code> and <code>specific_solver_style</code> have no effect if this option is not used.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--order</code></td>
            <td valign="top"><code>order</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">lineplot<br>combinedplot</td>
            <td valign="top"><pre><code>order: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Changes the order of the style cycle created by <code>--create-solver-style</code> from best to worst to the order specified in <code>specific_solver_style</code> in the config. <b>This option is strongly recommended</b> to create the <code>solver_style</code> dictionary, because if this option is not used the <code>solver_style</code> dictionary only contains the runs that are displayed in the plot and not all the runs in <code>specific_solver_style</code>.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--extend</code></td>
            <td valign="top"><code>extend</code></td>
            <td valign="top"><code>float</code></td>
            <td valign="top">scatterplot</td>
            <td valign="top"><pre><code>extend: 0.85</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Enables the extended mode that scales the plot down by the input value and adds a timeout line between the limit line and the axes. Only values between <code>0.0</code> and <code>1.0</code> are allowed and <code>0.85</code> is the recommended value.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--unique</code></td>
            <td valign="top"><code>unique</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">combinedplot</td>
            <td valign="top"><pre><code>unique: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Enable compare option, where only uniquely best runs get credited (the best run has a point advantage until the second best solves the benchmark).
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--stable</code></td>
            <td valign="top"><code>stable</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">combinedplot</td>
            <td valign="top"><pre><code>stable: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Enable compare option, where all runs get credited except the worst (the best runs have a point advantage until the worst solves the benchmark).
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--horse</code></td>
            <td valign="top"><code>horse</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">combinedplot</td>
            <td valign="top"><pre><code>horse: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Enable compare option, where all runs get credited if they are better than the <code>sota</code> (default). If the <code>--base</code> option is active, the specified run will be used to compare the other runs to.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--sota</code></td>
            <td valign="top"><code>sota</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">combinedplot</td>
            <td valign="top"><pre><code>sota: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Plots the best possible solver.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--relative</code></td>
            <td valign="top"><code>relative</code></td>
            <td valign="top"><code>bool</code></td>
            <td valign="top">combinedplot</td>
            <td valign="top"><pre><code>relative: true</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Plot the performance of all runs relative to <code>sota</code>.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>--base</code></td>
            <td valign="top"><code>base</code></td>
            <td valign="top"><code>str</code></td>
            <td valign="top">combinedplot</td>
            <td valign="top"><pre><code>base: "name"</code></pre>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="3" valign="top">Plot against base solver. Use the name of the base solver folder not the path. The path must be included in <code>--logpaths</code> or <code>--rlogpaths</code>.
            </td>
        </tr>
    </tbody>
</table>

## config only arguments


<table>
    <thead>
        <tr>
            <th width="15%">Name in config</th>
            <th width="10%">Type</th>
            <th width="10%">Plot type</th>
            <th width="65%">Config example</th>
        </tr>
    </thead>
    <tbody>
        <tr valign="top">
            <td valign="top"><code>solver_style</code></td>
            <td valign="top"><code>dict[str: dict]</code></td>
            <td valign="top">All*</td>
            <td valign="top"><pre><code>solver_style:
  "folder_name1":
    color: "black"
    label: "\textbf{best solver}"
    marker: "o"
    markeredgecolor: "black"
    markerfacecolor: "none"
    markersize: 5
  "folder_name2":
    color: "#df526b"
    label: "\textbf{second best}"
    marker: "s"
    markersize: 5</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="2" valign="top">Maps a specific styling to the name of a folder. Styling options include all options that change the style of the line in the plot or the name in the legend. Generally all options of <a href="https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html">matplotlib.axes.Axes.plot</a> can be used to create the styling for the folder. The example creates a black hollow circle marker for folder_name1 and a filled pink square marker for folder_name2. Another example would be to change the <code>zorder</code> and <code>linewidth</code> of a single folder to highlight this run. This argument is also usable in scatterplot configs but the script only uses the <code>label</code> to label the axes.
            </td>
        </tr>
        <tr valign="top">
            <td valign="top"><code>sat_style</code></td>
            <td valign="top"><code>dict[str: dict]</code></td>
            <td valign="top">scatterplot</td>
            <td valign="top"><pre><code>sat_style:
  sat:
    color: "purple"
    label: "SAT"
    marker: "x"
  unsat:
    color: "black"
    label: "UNSAT"
    marker: "o"
  unsolved:
    color: "blue"
    label: "UNSOLVED"
    marker: "s"</code></pre></td>
        </tr>
        <tr>
            <td colspan="2" valign="top"><b>Description:</b></td>
            <td colspan="2" valign="top">Maps a specific styling to each state (sat, unsat and unsolved).  Styling options include all options that change the style of the marker in the plot or the name in the legend. Generally all options of <a href="https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html">matplotlib.axes.Axes.scatter</a> can be used to create the styling for the state. The names of the keyword arguments differ from <a href="https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html">matplotlib.axes.Axes.plot</a>. For example, to create a hollow marker in <code>solver_style</code> you need to set <code>markeredgecolor</code> and
            <code>markerfacecolor</code>, but in <code>sat_style</code> the corresponding keyword arguments are <code>edgecolors</code> and <code>facecolors</code>.
            </td>
        </tr>
    </tbody>
</table>
