from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_tempo: Optional[float] = None
    target_valence: Optional[float] = None
    target_danceability: Optional[float] = None
    

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    FLOAT_FIELDS = {"energy", "valence", "danceability", "acousticness"}
    INT_FIELDS   = {"id", "tempo_bpm"}
    print(f"Loading songs from {csv_path}...")
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        songs = []
        for row in reader:
            for field in FLOAT_FIELDS:
                row[field] = float(row[field])
            for field in INT_FIELDS:
                row[field] = int(row[field])
            songs.append(row)
    print(f"Loaded {len(songs)} songs.")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song based on user preferences.
    Required by src/main.py

    Returns a tuple of (score, reasons) where score is 0.0–1.0 and
    reasons is a list of human-readable strings explaining the score.
    """
    # "Users think in terms of mood and genre first"
    weights = {
        "genre":        0.35,
        "mood":         0.30,
        "energy":       0.20,
        "valence":      0.10,
        "acousticness": 0.05,
    }

    scores: Dict[str, float] = {}
    reasons: List[str] = []

    # --- Genre (exact match) ---
    if song["genre"].lower() == user_prefs.get("favorite_genre", "").lower():
        scores["genre"] = 1.0
        reasons.append(f"Genre '{song['genre']}' matches your favorite genre.")
    else:
        scores["genre"] = 0.0
        reasons.append(f"Genre '{song['genre']}' doesn't match your favorite genre ('{user_prefs.get('favorite_genre')}').")

    # --- Mood (exact match) ---
    if song["mood"].lower() == user_prefs.get("favorite_mood", "").lower():
        scores["mood"] = 1.0
        reasons.append(f"Mood '{song['mood']}' matches your preferred mood.")
    else:
        scores["mood"] = 0.0
        reasons.append(f"Mood '{song['mood']}' doesn't match your preferred mood ('{user_prefs.get('favorite_mood')}').")

    # --- Energy (proximity to target_energy) ---
    target_energy = user_prefs.get("target_energy")
    if target_energy is not None:
        energy_score = max(0.0, 1.0 - abs(song["energy"] - target_energy))
        scores["energy"] = energy_score
        reasons.append(f"Energy {song['energy']:.2f} is {'close to' if energy_score >= 0.8 else 'away from'} your target ({target_energy:.2f}).")
    else:
        scores["energy"] = 0.5  # neutral when no preference given
        reasons.append("No energy preference set; applying neutral score.")

    # --- Valence (proximity to target_valence) ---
    target_valence = user_prefs.get("target_valence")
    if target_valence is not None:
        valence_score = max(0.0, 1.0 - abs(song["valence"] - target_valence))
        scores["valence"] = valence_score
        reasons.append(f"Valence {song['valence']:.2f} is {'close to' if valence_score >= 0.8 else 'away from'} your target ({target_valence:.2f}).")
    else:
        scores["valence"] = 0.5
        reasons.append("No valence preference set; applying neutral score.")

    # --- Acousticness (aligned with likes_acoustic preference) ---
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if likes_acoustic:
        scores["acousticness"] = song["acousticness"]
        reasons.append(f"Acousticness {song['acousticness']:.2f} — you prefer acoustic songs.")
    else:
        scores["acousticness"] = 1.0 - song["acousticness"]
        reasons.append(f"Acousticness {song['acousticness']:.2f} — you prefer non-acoustic songs.")

    # --- Weighted total ---
    total = sum(weights[feature] * scores[feature] for feature in weights)
    return round(total, 4), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
