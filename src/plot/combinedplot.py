from src.plot.baseplot import BasePlot
from src.plot.lineplot import LinePlot
from typing import Optional
import numpy as np
import pandas as pd


class CombinedPlot(BasePlot):
    def transform_data(self, data: dict[str, pd.DataFrame]) -> list[tuple[str, list[float], list[float], Optional[int]]]:

        folder_names = list(data.keys())

        self.validate_combined_options(folder_names)

        # merge tables on common benchmarks
        dfs = [data[folder_name] for folder_name in folder_names]
        common = set.intersection(*(set(df["Unnamed: 0"]) for df in dfs))
        dfs = [df[df["Unnamed: 0"].isin(common)].copy() for df in dfs]
        merged = dfs[0]

        for i, df in enumerate(dfs[1:], start=1):
            merged = merged.merge(df, on="Unnamed: 0", suffixes=(None, f"_{i}"))

        # calculate number in label
        label_nums = []
        for folder_name in folder_names:
            label_nums.append(len(data[folder_name][data[folder_name]['result'].isin([10, 20])]))

        # initilization
        events = [[] for _ in range(len(folder_names))]
        sota_events = []

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

            times = [t for _, t in valid]
            best = min(times)
            worst = max(times)
            if not (self.cfg.atr["horse"] and self.cfg.atr["base"] is not None and self.cfg.atr["base"] in folder_names):
                base = best
            sorted_times = sorted(set(times))
            second = (sorted_times[1] if len(sorted_times) > 1 else None)
            # only strictly best solvers get credit in unique:
            best_solvers = [(i, t) for i, t in valid if t == best]

            # stable: every solver gets a point until the last one finished the benchmark
            if self.cfg.atr["stable"]:
                for i, t in valid:
                    events[i].append((t, +1))
                    if best != worst:
                        events[i].append((worst, -1))
                sota_events.append((best, +1))
                if best != worst:
                    sota_events.append((worst, -1))

            # unique: only the best solver gets credited until the second best finishes
            elif self.cfg.atr["unique"]:
                for i, t in valid:
                    if t == best and len(best_solvers) == 1:
                        events[i].append((t, +1))
                        if second is not None:
                            events[i].append((second, -1))
                sota_events.append((best, +1))
                if second is not None:
                    sota_events.append((second, -1))

            # horse: campare rellative to the base solver which usualy is best
            elif self.cfg.atr["horse"]:
                for i, t in valid:
                    events[i].append((t, +1))
                    events[i].append((base, -1))
                for i, t in invalid:
                    if i != base_idx:
                        events[i].append((base, -1))
                sota_events.append((best, +1))
                sota_events.append((base, -1))

        # compute the individual curves from the events
        res = []
        for i, evs in enumerate(events):
            xs, ys = self.event_to_curve(evs)
            if i != base_idx:
                xs, ys = self.clean_up_curves(xs, ys)
            res.append((folder_names[i], xs, ys, label_nums[i]))
        sota_xs, sota_ys = self.event_to_curve(sota_events)
        sota_xs, sota_ys = self.clean_up_curves(sota_xs, sota_ys)
        if self.cfg.atr["sota"]:
            res.append(("sota", sota_xs, sota_ys, None))

        # sort curves by average y value
        res = sorted(res, key=lambda c: sum(c[2]) / len(c[2]) if len(c[2]) > 0 else float("-inf"))

        # create curves relative to the sota curve
        if self.cfg.atr["relative"]:
            res = self.relative_result(res, sota_xs, sota_ys)

        return res

    def relative_result(self, res, sota_xs, sota_ys):
        relative_res = []

        sota_xs_np = np.asarray(sota_xs, dtype=float)
        sota_ys_np = np.asarray(sota_ys, dtype=float)

        for label, xs, ys in res:

            if label == "sota":
                continue

            xs_np = np.asarray(xs, dtype=float)
            ys_np = np.asarray(ys, dtype=float)
            all_x = np.union1d(xs_np, sota_xs_np)
            solver_y = self.eval_step(xs_np, ys_np, all_x)
            sota_y = self.eval_step(sota_xs_np, sota_ys_np, all_x)
            relative_y = np.divide(solver_y, sota_y, out=np.zeros_like(solver_y, dtype=float), where=sota_y != 0)
            relative_res.append((label, all_x.tolist(), relative_y.tolist()))

        return relative_res

    def event_to_curve(self, events: list[tuple[float, float]]) -> tuple[list[float], list[float]]:
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
        if len(xs) == 0:
            return np.zeros_like(query, dtype=float)
        idx = np.searchsorted(xs, query, side="right") - 1
        idx = np.clip(idx, 0, len(ys) - 1)
        return ys[idx]

    def validate_combined_options(self, folder_names):
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
        if self.cfg.atr["base"] is not None and self.cfg.atr["base"] not in folder_names:
            print("--base has to match a folder name in --logpaths or --rlogpaths")

    def create_plot(self, data: list[tuple[str, list[float], list[float], Optional[int]]]):
        lineplot = LinePlot(self.cfg)
        lineplot.create_plot(data)
