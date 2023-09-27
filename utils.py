import os
import re
import json

import pandas as pd


def load_day_stats(stats_path, date):
    with open(stats_path, "rb") as f:
        stats = json.load(f)
    stats["date"] = date
    return stats


def build_stats_df(stats_dir):
    stats = {"date": [], "/ ": [], "/sample": [], "/sample/related": [],
             "/charon/getDataset": []}
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
    stats_df = pd.DataFrame(stats)
    return stats_df.set_index("date")
