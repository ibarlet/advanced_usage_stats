# Utilities to be used in this project
import requests
import pandas as pd
import numpy as np
import os
import json
import logging
from time import sleep

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Data pulling utilities
def download_replay(
    url: str,
    storage_folder: str,
    output_filename: str = None,
    overwrite: bool = False,
    download_delay: int = 2,
):
    """
    Downloads a replay from the given URL and saves it to the specified folder.
    :param url: URL of the replay to download
    :param storage_folder: Folder to save the downloaded replay
    :param output_filename: Name to save the replay as (optional)
    :param overwrite: Whether to overwrite the file if it already exists
    :param download_delay: Delay in seconds between downloads to spare PS servers (optional)
    """
    if "replay" not in url:
        if "smogtours.psim.us/battle-" in url:
            logger.warning(
                f"URL {url} is a smogtours battle link. Switching to replay link."
            )
            url = url.replace(
                "smogtours.psim.us/battle-", "replay.pokemonshowdown.com/smogtours-"
            )
        else:
            logger.warning(f"URL {url} does not contain 'replay'. Skipping download.")
            return None
    if url[:7] != "http://" and url[:8] != "https://":
        url = "http://" + url
    if not output_filename:
        output_filename = url.split("/")[-1]
    file_path = f"{storage_folder}/{output_filename}"
    if not overwrite and os.path.exists(file_path):
        logger.debug(f"File {file_path} already exists. Skipping download.")
        return output_filename

    sleep(download_delay)  # Delay to spare PS servers
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        logger.debug(f"Downloaded {url} to {file_path}")
    else:
        logger.warning(f"Failed to download {url}. Status code: {response.status_code}")
        return None

    return output_filename


# Stat parsing utilities
def parse_single_replay(replay_path: str, game_id: str = None) -> pd.DataFrame:
    """
    Parses a single replay file and returns a pandas DataFrame with the parsed data.
    :param replay_path: Path to the replay file
    :param game_id: Optional game ID to add for an extra filter later
    :return: DataFrame with the parsed data
    """
    with open(replay_path) as f:
        data = json.load(f)

    pd_log = pd.DataFrame(data["log"].split("\n"))
    pd_log = pd_log[0].str.split("|", expand=True)
    col2split = pd_log[2].str.split(":", n=1, expand=True)
    pd_log["trainer"] = col2split[0]
    pd_log["nickname"] = col2split[1]
    pd_log = pd_log.replace("", None)

    turn_count = (pd_log.loc[pd_log[1] == 'turn']['trainer']).astype(int).max()

    players = pd_log.loc[pd_log[1] == "player"][["trainer", 3]].dropna().drop_duplicates()
    players = players.rename(columns={3: "trainer_name"})
    winner = pd_log.loc[pd_log[1] == "win"][2]
    players["won"] = players["trainer_name"].isin(winner)

    switches = pd_log.loc[pd_log[1] == "switch"][["trainer", "nickname", 3, 4]]
    switches = switches.rename(
        columns={
            3: "species_gender",
            4: "health_remaining",
        }
    )
    switches = switches.drop_duplicates(subset=["trainer", "species_gender"])
    # Gender data here gets corrupted by shiny data. May need to address if we ever look at gender
    try:
        switches[["species", "gender"]] = switches["species_gender"].str.split(
            ",", n=1, expand=True
        )
    except ValueError:
        switches["species"] = switches["species_gender"]
        switches["gender"] = None
    switches = switches[
        [
            "trainer",
            "nickname",
            "species",
        ]
    ]
    switches["trainer"] = switches["trainer"].str[:-1]
    pokemon_seen = switches.merge(
        players, left_on="trainer", right_on="trainer", how="left"
    )

    used_moves = pd_log.loc[pd_log[1] == "move"][
        [
            "trainer",
            "nickname",
            3,
        ]
    ]
    used_moves = used_moves.rename(
        columns={
            "trainer": "trainer_user",
            "nickname": "nickname_user",
            3: "move",
        }
    )
    used_moves = used_moves.drop_duplicates(subset=["trainer_user", "move"])
    used_moves["trainer_user"] = used_moves["trainer_user"].str[:-1]
    used_moves = (
        used_moves.groupby(["trainer_user", "nickname_user"])["move"]
        .apply(
            lambda x: pd.Series(x.values[:4])
        )  # Limit to 4 moves so transform doesn't break everything
        .unstack()
        .reset_index()
    )

    if len(used_moves.columns) < 6:
        # If there are fewer than 4 moves used by all pokemon in the match, fill with NaN
        for i in range(6 - len(used_moves.columns)):
            used_moves[f"move {4-i}"] = np.nan

    # Rename colums to more useful names
    used_moves.columns = [
        "trainer_user",
        "nickname_user",
        "move 1",
        "move 2",
        "move 3",
        "move 4",
    ]
    # Add into pokemon_seen and drop unused columns
    pokemon_seen = pokemon_seen.merge(
        used_moves,
        left_on=["trainer", "nickname"],
        right_on=["trainer_user", "nickname_user"],
        how="left",
    )
    pokemon_seen['turn_count'] = turn_count
    pokemon_seen = pokemon_seen.drop(
        columns=["trainer_name", "trainer", "nickname", "trainer_user", "nickname_user"]
    )

    if game_id is not None:
        pokemon_seen["game_id"] = game_id

    return pokemon_seen
