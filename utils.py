import os
import re
import json
import argparse

import pandas as pd


def load_day_stats(stats_path, date):
    with open(stats_path, "rb") as f:
        stats = json.load(f)
    stats["date"] = date
    return stats


def build_stats_dict(stats_dir):
    if not os.path.isdir(stats_dir):
        raise NotADirectoryError(f"{stats_dir} is not a directory")
    stats = {"date": [], "/ ": [], "/sample": [], "/sample/related": [],
             "/sample/matrix": [], "/charon/getDataset": []}
    for file_path in [obj_path for obj_path in os.listdir(stats_dir) if
                      os.path.isfile(os.path.join(stats_dir, obj_path))]:
        if re.fullmatch(r"viewbovis_requests_\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])\.json",
                        file_path):
            date_match = re.search(r"\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])",
                                   file_path)
            day_stats = load_day_stats(os.path.join(stats_dir, file_path),
                                       date_match[0])
            for key in stats.keys():
                stats[key].append(day_stats[key])
        else:
            pass
    if stats == {"date": [], "/ ": [], "/sample": [], "/sample/related": [],
                 "/sample/matrix": [], "/charon/getDataset": []}:
        raise Exception("no valid stats files found in provided directory")
    return stats


def build_stats_df(stats_dir):
    stats_df = pd.DataFrame(build_stats_dict(stats_dir))
    idx = pd.date_range(stats_df.date.min(), stats_df.date.max()).date
    return stats_df.set_index(stats_df["date"].map(lambda x: pd.to_datetime(x).date()))\
        .sort_index().reindex(idx, fill_value=0).drop("date", axis=1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stats_dir")
    args = parser.parse_args()
    print(build_stats_df(args.stats_dir))
