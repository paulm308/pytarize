from src.plot.baseplot import BasePlot
from src.plot.lineplot import LinePlot
import numpy as np
import pandas as pd


class CombinedPlot(BasePlot):
    def transform_data(self, data: dict[str, pd.DataFrame]):

        folder_names = list(data.keys())
        dfs = [data[folder_name] for folder_name in folder_names]

        common = set.intersection(*(set(df["Unnamed: 0"]) for df in dfs))

        dfs = [df[df["Unnamed: 0"].isin(common)].copy() for df in dfs]

        merged = dfs[0]

        for i, df in enumerate(dfs[1:], start=1):
            merged = merged.merge(df, on="Unnamed: 0", suffixes=(None, f"_{i}"))

        events = [[] for _ in range(len(folder_names))]
        sota_events = []

        for _, row in merged.iterrows():

            # determin all solvers that solved the benchmark
            invalid = []
            valid = []
            for i in range(len(folder_names)):
                time_label = f"real_{i}" if i >= 1 else "real"
                status_label = f"result_{i}" if i >= 1 else "result"
                if row[status_label] in [10, 20]:
                    valid.append((i, float(row[time_label])))
                else:
                    invalid.append((i, float(row[time_label])))

            if not valid:
                continue

            times = [t for _, t in valid]
            best = min(times)
            worst = max(times)
            sorted_times = sorted(set(times))
            second = (sorted_times[1] if len(sorted_times) > 1 else None)

            if self.cfg.atr["stable"]:
                for i, t in valid:
                    if t < worst:
                        events[i].append((t, +1))
                        if len(valid) >= 1:
                            events[i].append((worst, -1))
                sota_events.append((best, +1))
                if len(valid) >= 1:
                    sota_events.append((worst, -1))

            elif self.cfg.atr["unique"]:
                for i, t in valid:
                    if t == best:
                        events[i].append((t, +1))
                        if second is not None:
                            events[i].append((second, -1))
                sota_events.append((best, +1))
                if second is not None:
                    sota_events.append((second, -1))

            elif self.cfg.atr["horse"]:
                for i, t in valid:
                    events[i].append((t, +1))
                    events[i].append((best, -1))
                for i, t in invalid:
                    events[i].append((best, -1))
                sota_events.append((best, 0))

        res = []
        for i, evs in enumerate(events):
            xs, ys = self.event_to_curve(evs)
            res.append((folder_names[i], xs, ys))
        sota_xs, sota_ys = self.event_to_curve(sota_events)

        if self.cfg.atr["sota"]:
            res.append(("sota", sota_xs, sota_ys))

        res = sorted(res, key=lambda c: max(c[2]) if len(c[2]) > 0 else float("-inf"))

        if self.cfg.atr["relative"]:
            pass  # TODO

        return res

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

    def create_plot(self, data: list[tuple[str, list[float], list[float]]]):
        lineplot = LinePlot(self.cfg)
        lineplot.create_plot(data)
