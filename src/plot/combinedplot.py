from src.plot.baseplot import BasePlot
from src.plot.lineplot import LinePlot
from typing import Optional
import numpy as np
import pandas as pd


class CombinedPlot(BasePlot):
    def transform_data(self, data: dict[str, pd.DataFrame]) -> list[tuple[str, list[float], list[float], Optional[int]]]:
        """
        Transforms the data in to a horserace representation.

        Parameters:
        data (dict[str, pd.DataFrame]): A dictionary of all zummarys that are loaded in pandas DataFrames.
        The key of the dictionary is the name of the folder that contains the zummary.

        Returns:
        list[tuple[str, list[float], list[float], Optional[int]]]: A list of tuples of the 0: name of the folder, 1: x-values, 2: y-values, 3: The solved count in the legend
        """

        folder_names = list(data.keys())

        self.validate_combined_options(folder_names)

        # merge tables on common benchmarks
        dfs = [data[folder_name] for folder_name in folder_names]

        # this only works if solvers are correct
        if "--sat" in self.cfg.zummarize_cli:
            dfs = [df[df["result"].isin([1, 2, 10])] for df in dfs]
        elif "--unsat" in self.cfg.zummarize_cli:
            dfs = [df[df["result"].isin([1, 2, 20])] for df in dfs]

        common = set.intersection(*(set(df["Unnamed: 0"]) for df in dfs))
        merged = [df[df["Unnamed: 0"].isin(common)].copy() for df in dfs][0]

        for i, df in enumerate(dfs[1:], start=1):
            merged = merged.merge(df, on="Unnamed: 0", suffixes=(None, f"_{i}"))

        # calculate number in label
        cols = ["result"] + [f"result_{i}" for i in range(1, len(folder_names))]
        sota_label_num = (merged[cols].isin([10, 20]).any(axis=1)).sum()
        label_nums = []
        for i in range(len(folder_names)):
            label_nums.append(len(dfs[i][dfs[i]['result'].isin([10, 20])]))

        # initialization
        events = [[] for _ in range(len(folder_names))]
        sota_events = []
        kbest_events = []
        kbest_label_number = 0

        base_idx = -1
        if self.cfg.atr["horse"] and self.cfg.atr["base"] is not None and self.cfg.atr["base"] in folder_names:
            base_idx = folder_names.index(self.cfg.atr["base"])

        for _, row in merged.iterrows():

            # extract the time of all zummarys that solved the benchmark and store them in invalid if not
            invalid = []
            valid = []
            base = None
            for i in range(len(folder_names)):
                time_label = f"time_{i}" if i >= 1 else "time"
                status_label = f"result_{i}" if i >= 1 else "result"
                if row[status_label] in [10, 20]:
                    valid.append((i, float(row[time_label])))
                    if i == base_idx:
                        base = float(row[time_label])
                else:
                    invalid.append((i, float(row[time_label])))

            if not valid:
                continue

            if self.cfg.atr["kbest"] is not None and self.cfg.atr["kbest"] <= len(valid):
                kbest_label_number += 1

            times = [t for _, t in valid]
            best = min(times)
            worst = max(times)
            if not (self.cfg.atr["horse"] and (self.cfg.atr["base"] is not None and self.cfg.atr["base"] in folder_names or self.cfg.atr["kbest_base"] is not None)):
                base = best
            sorted_times = sorted(times)
            second = (sorted_times[1] if len(sorted_times) > 1 else None)
            # only strictly best solvers get credit in unique:
            best_solvers = [(i, t) for i, t in valid if t == best]

            # --kbest-base
            if self.cfg.atr["kbest_base"] is not None and self.cfg.atr["kbest_base"] <= len(sorted_times) and self.cfg.atr["kbest_base"] >= 1:
                base = sorted_times[self.cfg.atr["kbest_base"] - 1]

            # stable: every solver gets a point until the virtual worst solver (vws) finished the benchmark
            if self.cfg.atr["stable"]:
                for i, t in valid:
                    events[i].append((t, +1))
                    if len(valid) == len(folder_names):
                        events[i].append((worst, -1))
                # stable + sota
                sota_events.append((best, +1))
                if len(valid) == len(folder_names):
                    sota_events.append((worst, -1))
                # stable + kbest
                if self.cfg.atr["kbest"] is not None and self.cfg.atr["kbest"] <= len(sorted_times):
                    kbest_events.append((sorted_times[self.cfg.atr["kbest"] - 1], +1))
                    if len(sorted_times) == len(folder_names):
                        kbest_events.append((worst, -1))

            # unique: only the best solver gets credited until the second best finishes
            elif self.cfg.atr["unique"]:
                for i, t in valid:
                    if t == best and len(best_solvers) == 1:
                        events[i].append((t, +1))
                        if second is not None:
                            events[i].append((second, -1))
                    elif self.cfg.atr["zeros"]:
                        events[i].append((t, 0))
                # unique + sota
                sota_events.append((best, +1))
                if second is not None:
                    sota_events.append((second, -1))
                # unique + kbest
                if self.cfg.atr["kbest"] is not None and self.cfg.atr["kbest"] == 1:
                    kbest_events.append((best, +1))
                    if second is not None:
                        kbest_events.append((second, -1))

            # horse: compare relative to the base solver which usually is best
            elif self.cfg.atr["horse"]:
                for i, t in valid:
                    events[i].append((t, +1))
                    events[i].append((base, -1))
                for i, t in invalid:
                    if i != base_idx:
                        events[i].append((base, -1))
                # horse + sota
                sota_events.append((best, +1))
                sota_events.append((base, -1))
                # horse + kbest
                if self.cfg.atr["kbest"] is not None:
                    if self.cfg.atr["kbest"] <= len(sorted_times):
                        kbest_events.append((sorted_times[self.cfg.atr["kbest"] - 1], +1))
                    kbest_events.append((base, -1))

        # compute the individual curves from the events
        res = []
        for i, evs in enumerate(events):
            xs, ys = self.event_to_curve(evs)
            if not (self.is_base_curve(ys) or self.cfg.atr["no_clean"]):
                xs, ys = self.clean_up_curves(xs, ys)
            res.append((folder_names[i], xs, ys, label_nums[i]))

        sota_xs, sota_ys = self.event_to_curve(sota_events)
        if not (self.is_base_curve(sota_ys) or self.cfg.atr["no_clean"]):
            sota_xs, sota_ys = self.clean_up_curves(sota_xs, sota_ys)

        kbest_xs, kbest_ys = self.event_to_curve(kbest_events)
        if not (self.is_base_curve(kbest_ys) or self.cfg.atr["no_clean"]):
            kbest_xs, kbest_ys = self.clean_up_curves(kbest_xs, kbest_ys)

        if self.cfg.atr["sota"]:
            label = "sota"
            if self.cfg.atr["sota_label"] is not None:
                label = self.cfg.atr["sota_label"]
            res.append((label, sota_xs, sota_ys, sota_label_num))

        if self.cfg.atr["kbest"] is not None:
            label = f"{self.cfg.atr['kbest']}. best"
            if self.cfg.atr["kbest_label"] is not None:
                label = self.cfg.atr["kbest_label"]
            res.append((label, kbest_xs, kbest_ys, kbest_label_number))

        # remove NaNs:
        cleaned = []
        for curve in res:
            x = np.asarray(curve[1], dtype=float)
            y = np.asarray(curve[2], dtype=float)
            mask = ~(np.isnan(x) | np.isnan(y))
            cleaned.append((curve[0], x[mask], y[mask], *curve[3:]))
        res = cleaned

        # sort curves by area under curve
        res = sorted(res, key=lambda c: np.trapezoid(c[2], c[1]))

        # create curves relative to the sota curve
        if self.cfg.atr["relative"]:
            res = self.relative_result(res, sota_xs, sota_ys)

        return res

    def is_base_curve(self, ys: list[float]) -> bool:
        """
        Checks if a computed curve is base curve (a curve that only contains 0s as y values)

        Parameters:
        ys (list[float]): The y values that are checked

        Returns:
        bool: is the curve a base curve?
        """
        for y in ys:
            if y != 0:
                return False
        return True

    def relative_result(self, res, sota_xs, sota_ys):
        """
        Computes curves relative to sota.

        Parameters:
        res (list[tuple[str, list[float], list[float], Optional[int]]]): The curves.
        sota_xs (list[float]): The x-values of the sota curve.
        sota_ys (list[float]). The y-values of the sota curve.

        Returns:
        list[tuple[str, list[float], list[float], Optional[int]]]: The transformed curves.
        """
        relative_res = []

        sota_xs_np = np.asarray(sota_xs, dtype=float)
        sota_ys_np = np.asarray(sota_ys, dtype=float)

        for label, xs, ys, solved_count in res:

            if label == "sota":
                continue

            xs_np = np.asarray(xs, dtype=float)
            ys_np = np.asarray(ys, dtype=float)
            all_x = np.union1d(xs_np, sota_xs_np)
            solver_y = self.eval_step(xs_np, ys_np, all_x)
            sota_y = self.eval_step(sota_xs_np, sota_ys_np, all_x)
            relative_y = np.divide(solver_y, sota_y, out=np.zeros_like(solver_y, dtype=float), where=sota_y != 0)
            relative_res.append((label, all_x.tolist(), relative_y.tolist(), solved_count))

        return relative_res

    def event_to_curve(self, events: list[tuple[float, float]]) -> tuple[list[float], list[float]]:
        """
        Creates the curves as a stepwise function.

        Parameters:
        events (list[tuple[float, float]]): List of events.

        Returns:
        tuple[list[float], list[float]]: The x and y-values of the computed curve.
        """
        evs = np.asarray(events, dtype=float).reshape(-1, 2)
        times = evs[:, 0]
        deltas = evs[:, 1]
        order = np.argsort(times)
        times = times[order]
        deltas = deltas[order]
        xs, idx = np.unique(times, return_index=True)
        summed_deltas = np.add.reduceat(deltas, idx)
        ys = np.cumsum(summed_deltas)
        return (xs.tolist(), ys.tolist())

    def clean_up_curves(self, xs: list[float], ys: list[float]) -> tuple[list[float], list[float]]:
        """
        Removes points on the curve that don't change the y-value of the curve.

        Parameters:
        xs: The x-values of the curve.
        ys: The y-values of the curve.

        Returns:
        tuple[list[float], list[float]]: The compressed curve.
        """
        res_xs = []
        res_ys = []
        last_value = None
        for i, value in enumerate(ys):
            if last_value is not None and value == last_value:
                continue
            last_value = value
            res_xs.append(xs[i])
            res_ys.append(value)
        return (res_xs, res_ys)

    def eval_step(self, xs: np.ndarray, ys: np.ndarray, query: np.ndarray) -> np.ndarray:
        """
        Evaluates a stepwise (right-continuous, previous-value-hold) function defined by
        xs and ys at the given query points.

        Parameters:
        xs (np.ndarray): The x-values of the step function, assumed to be sorted ascending.
        ys (np.ndarray): The y-values of the step function, corresponding to xs.
        query (np.ndarray): The x-values at which to evaluate the step function.

        Returns:
        np.ndarray: The y-values of the step function at the query points. Query points
        before the first x-value are evaluated to zero.
        """
        if len(xs) == 0:
            return np.zeros_like(query, dtype=float)
        idx = np.searchsorted(xs, query, side="right") - 1
        idx = np.clip(idx, 0, len(ys) - 1)
        return ys[idx]

    def validate_combined_options(self, folder_names):
        """
        Ensures that the used combination of options is valid.

        Parameters:
        folder_names (list[str]): The names of the folders that contain a zummary file.
        """
        if self.cfg.atr["stable"] is False and self.cfg.atr["unique"] is False and self.cfg.atr["horse"] is False:
            self.cfg.atr["horse"] = True
        elif self.cfg.atr["stable"] + self.cfg.atr["unique"] + self.cfg.atr["horse"] >= 2:
            opts = [[self.cfg.atr["stable"], "--stable"], [self.cfg.atr["unique"], "--unique"], [self.cfg.atr["horse"], "--horse"]]
            strs = [opt[1] for opt in opts if opt[0] is True]
            if len(strs) == 2:
                print(f"Cannot combine {strs[0]} and {strs[1]}")
            else:
                print(f"Cannot combine {strs[0]}, {strs[1]} and {strs[2]}")
        if self.cfg.atr["base"] is not None and not self.cfg.atr["horse"]:
            print("--base has no effect without, --horse")
        if self.cfg.atr["kbest_base"] is not None and not self.cfg.atr["horse"]:
            print("--kbest-base has no effect without, --horse")
        if self.cfg.atr["base"] is not None and self.cfg.atr["base"] not in folder_names:
            print("--base has to match the name of a folder in --logpaths or --rlogpaths")
        if self.cfg.atr["kbest"] is not None and (self.cfg.atr["kbest"] < 0 or self.cfg.atr["kbest"] > len(folder_names)):
            print(f"Invalid input for --kbest: {self.cfg.atr['kbest']}, use values between (inclusive) 1 and {len(folder_names)}")
        if self.cfg.atr["kbest_base"] is not None and (self.cfg.atr["kbest_base"] < 0 or self.cfg.atr["kbest_base"] > len(folder_names)):
            print(f"Invalid input for --kbest-base: {self.cfg.atr['kbest_base']}, use values between (inclusive) 1 and {len(folder_names)}")
        if self.cfg.atr["kbest_base"] is not None and self.cfg.atr["base"] is not None:
            print("--kbest-base and --base can not be combined, using --kbest-base as default (--base has no effect)")
        if self.cfg.atr["zeros"] and not self.cfg.atr["unique"]:
            print("--zeros has no effect if --unique is not used")

    def create_plot(self, data: list[tuple[str, list[float], list[float], Optional[int]]]):
        """
        This function is responsible for creating and styling the plot.

        Parameters:
        data (list[tuple[str, list[float], list[float], Optional[int]]]): the output of transform_data.
        """
        # combinedplot is a lineplot
        lineplot = LinePlot(self.cfg)
        lineplot.create_plot(data)
