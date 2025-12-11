"""
Test script to recommend YouTube movies and songs based on theme.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.party.adventure_list import search_youtube_videos

def recommend_theme_content(theme: str):
    """
    Recommend YouTube songs and movies based on party theme.
    
    Args:
        theme: Party theme name (e.g., "superhero", "princess", "pirate")
    """
    print(f"\n{'='*60}")
    print(f"🎬 THEME: {theme.upper()}")
    print(f"{'='*60}\n")
    
    # Search for songs
    print("🎵 RECOMMENDED SONGS:")
    print("-" * 60)
    songs_query = f"{theme} party songs for kids music"
    songs = search_youtube_videos(songs_query, max_results=5)
    
    if songs:
        for i, song in enumerate(songs, 1):
            print(f"\n{i}. {song['title']}")
            print(f"   Channel: {song['channel']}")
            print(f"   Views: {song['views']}")
            print(f"   URL: {song['url']}")
            if 'thumbnail' in song:
                print(f"   Thumbnail: {song['thumbnail']}")
    else:
        print("❌ No songs found")
    
    # Search for movies
    print("\n\n🎥 RECOMMENDED MOVIES:")
    print("-" * 60)
    movies_query = f"{theme} movie for kids family entertainment"
    movies = search_youtube_videos(movies_query, max_results=5)
    
    if movies:
        for i, movie in enumerate(movies, 1):
            print(f"\n{i}. {movie['title']}")
            print(f"   Channel: {movie['channel']}")
            print(f"   Views: {movie['views']}")
            print(f"   URL: {movie['url']}")
            if 'thumbnail' in movie:
                print(f"   Thumbnail: {movie['thumbnail']}")
    else:
        print("❌ No movies found")
    
    # Summary
    print(f"\n\n{'='*60}")
    print(f"📊 SUMMARY FOR '{theme.upper()}'")
    print(f"{'='*60}")
    print(f"Total Songs Found: {len(songs)}")
    print(f"Total Movies Found: {len(movies)}")
    print(f"Total Content: {len(songs) + len(movies)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    # Theme name as string variable
    theme = "superhero"
    
    # You can change the theme here:
    # theme = "princess"
    # theme = "pirate"
    # theme = "dinosaur"
    # theme = "space"
    # theme = "underwater"
    
    print(f"\n📝 Using YOUTUBE_API_KEY: {os.getenv('YOUTUBE_API_KEY')[:20]}...")
    
    # Recommend content for the theme
    recommend_theme_content(theme)
    
    # Optionally test with multiple themes
    print("\n\n" + "="*60)
    print("🔄 TESTING WITH MULTIPLE THEMES")
    print("="*60)
    
    test_themes = ["princess", "pirate", "dinosaur"]
    
    for test_theme in test_themes:
        recommend_theme_content(test_theme)
