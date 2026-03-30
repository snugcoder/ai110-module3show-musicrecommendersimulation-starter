"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, UserProfile


def main() -> None:
    songs = load_songs("data/songs.csv") 
    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    
    annie = UserProfile(favorite_genre="lofi", favorite_mood="chill", target_energy=0.5, likes_acoustic=True, target_tempo=70.0, target_valence=0.61, target_danceability=0.59)
    

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 54
    print()
    print("=" * width)
    print(f"  Top {len(recommendations)} Recommendations")
    print("=" * width)

    for i, (song, score, reasons) in enumerate(recommendations, start=1):
        bar_filled = round(score * 10)
        bar = "█" * bar_filled + "░" * (10 - bar_filled)
        print(f"\n  #{i}  {song['title']}  —  {song['artist']}")
        print(f"       {song['genre'].capitalize()} / {song['mood'].capitalize()}")
        print(f"       Score: {score:.2f}  [{bar}]")
        print(f"       Why:")
        for reason in reasons:
            print(f"         • {reason}")

    print()
    print("=" * width)
    print()


if __name__ == "__main__":
    main()
