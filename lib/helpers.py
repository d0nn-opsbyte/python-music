from models import session, User, Playlist, Song
from datetime import datetime
from tabulate import tabulate

def list_users():
    users = session.query(User).order_by(User.name).all()
    if not users:
        print("No users found.")
        return users
    
    print("\n--- All Users ---")
    for user in users:
        total_songs = sum(len(playlist.songs) for playlist in user.playlists)
        print(f"{user.id}. {user.name} - {user.email} (Joined: {user.created_at.strftime('%Y-%m-%d')})")
    return users

def create_user(name, email):
    try:
        if not name or not email:
            raise ValueError("Name and email cannot be empty!")
            
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            raise ValueError(f"Email '{email}' is already registered!")
            
        new_user = User(name=name, email=email)
        session.add(new_user)
        session.commit()
        print(f"User '{new_user.name}' created successfully! ")
        return new_user
        
    except ValueError as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        raise Exception(f"Unexpected error: {e}")   

def create_playlist(user_id, title, description=None):
    try:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found!")
            
        if not title:
            raise ValueError("Playlist title cannot be empty!")
            
        new_playlist = Playlist(title=title, description=description, user_id=user_id)
        session.add(new_playlist)
        session.commit()
        print(f"Playlist '{new_playlist.title}' created for {user.name}! 🎶")
        return new_playlist
        
    except ValueError as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        raise Exception(f"Unexpected error: {e}")

def view_user_playlists(user_id):
    user = session.get(User, user_id)
    if not user:
        raise ValueError("User not found!")
        
    playlists = session.query(Playlist).filter_by(user_id=user_id).all()
    if not playlists:
        print(f"{user.name} has no playlists yet.")
        return playlists
        
    print(f"\n--- {user.name}'s Playlists ---")
    for playlist in playlists:
        song_count = session.query(Song).filter_by(playlist_id=playlist.id).count()
        print(f"{playlist.id}. {playlist.title}")
        if playlist.description:
            print(f"   Description: {playlist.description}")
        print(f"   Songs: {song_count}")
        print()
    return playlists

def add_song_to_playlist(playlist_id, title, artist, album=None):
    try:
        playlist = session.get(Playlist, playlist_id)
        if not playlist:
            raise ValueError("Playlist not found!")
            
        if not title or not artist:
            raise ValueError("Title and artist cannot be empty!")
            
        new_song = Song(
            title=title, 
            artist=artist, 
            album=album, 
            playlist_id=playlist_id
        )
        session.add(new_song)
        session.commit()
        print(f"Added '{title}' by {artist} to '{playlist.title}'! ✅")
        return new_song
        
    except ValueError as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        raise Exception(f"Unexpected error: {e}")

def view_playlist_songs(playlist_id):
    playlist = session.get(Playlist, playlist_id)
    if not playlist:
        raise ValueError("Playlist not found!")
        
    songs = session.query(Song).filter_by(playlist_id=playlist_id).all()
    if not songs:
        print(f"Playlist '{playlist.title}' is empty.")
        return songs
        
    print(f"\n--- Songs in '{playlist.title}' ---")
    for i, song in enumerate(songs, 1):
        album_info = f" (Album: {song.album})" if song.album else ""
        print(f"{i}. {song.title} by {song.artist}{album_info}")
    return songs

def delete_song(song_id):
    song = session.get(Song, song_id)
    if not song:
        raise ValueError("Song not found!")
        
    session.delete(song)
    session.commit()
    print(f"Deleted '{song.title}' by {song.artist} successfully.")
    return song

def search_songs(search_term):
    if not search_term:
        raise ValueError("Please enter a search term.")
        
    songs = session.query(Song).filter(
        (Song.title.ilike(f"%{search_term}%")) | 
        (Song.artist.ilike(f"%{search_term}%")) |
        (Song.album.ilike(f"%{search_term}%"))
    ).all()
    
    if not songs:
        print("No songs found matching your search.")
        return songs
        
    print(f"\n--- Search Results for '{search_term}' ---")
    for song in songs:
        playlist = session.get(Playlist, song.playlist_id)
        user = session.get(User, playlist.user_id)
        album_info = f" | Album: {song.album}" if song.album else ""
        print(f"'{song.title}' by {song.artist}{album_info}")
        print(f"   → Playlist: {playlist.title} | User: {user.name}")
        print()
    return songs

def seed_sample_data():
    try:
        # Check if data already exists
        existing_users = session.query(User).count()
        if existing_users > 0:
            print("Data already exists in the database!")
            print("Use 'list-users-cmd' to see existing data.")
            return False
        
        # Create sample users
        sample_users = [
            {"name": "Alice Johnson", "email": "alice@email.com"},
            {"name": "Bob Smith", "email": "bob@email.com"},
            {"name": "Charlie Brown", "email": "charlie@email.com"}
        ]
        
        users = []
        for user_data in sample_users:
            user = User(**user_data)
            session.add(user)
            users.append(user)
        
        session.commit()
        
        # Create sample playlists
        playlists_data = [
            {"title": "Rock Classics", "description": "Best rock songs ever", "user_id": users[0].id},
            {"title": "Chill Vibes", "description": "Relaxing music for studying", "user_id": users[1].id},
            {"title": "Workout Mix", "description": "High energy workout songs", "user_id": users[2].id},
            {"title": "Road Trip", "description": "Perfect driving playlist", "user_id": users[0].id}
        ]
        
        playlists = []
        for playlist_data in playlists_data:
            playlist = Playlist(**playlist_data)
            session.add(playlist)
            playlists.append(playlist)
        
        session.commit()
        
        # Create sample songs
        songs_data = [
            # Rock Classics (Playlist 1)
            {"title": "Bohemian Rhapsody", "artist": "Queen", "album": "A Night at the Opera", "playlist_id": playlists[0].id},
            {"title": "Sweet Child O' Mine", "artist": "Guns N' Roses", "album": "Appetite for Destruction", "playlist_id": playlists[0].id},
            {"title": "Hotel California", "artist": "Eagles", "album": "Hotel California", "playlist_id": playlists[0].id},
            
            # Chill Vibes (Playlist 2)
            {"title": "Weightless", "artist": "Marconi Union", "album": "Weightless", "playlist_id": playlists[1].id},
            {"title": "Strawberry Swing", "artist": "Coldplay", "album": "Viva la Vida", "playlist_id": playlists[1].id},
            
            # Workout Mix (Playlist 3)
            {"title": "Eye of the Tiger", "artist": "Survivor", "album": "Eye of the Tiger", "playlist_id": playlists[2].id},
            {"title": "Stronger", "artist": "Kanye West", "album": "Graduation", "playlist_id": playlists[2].id},
            
            # Road Trip (Playlist 4)
            {"title": "Life is a Highway", "artist": "Tom Cochrane", "album": "Mad Mad World", "playlist_id": playlists[3].id},
            {"title": "On the Road Again", "artist": "Willie Nelson", "album": "Honeysuckle Rose", "playlist_id": playlists[3].id}
        ]
        
        for song_data in songs_data:
            song = Song(**song_data)
            session.add(song)
        
        session.commit()
        
        print("Sample data seeded successfully! ")
        print("Created 3 users, 4 playlists, and 9 songs.")
        
        
        print("\nUsers created:")
        for user in users:
            print(f"  User {user.id}: {user.name}")
        
        print("\nPlaylists created:")
        for playlist in playlists:
            print(f"  Playlist {playlist.id}: {playlist.title} (User {playlist.user_id})")
        
        return True
        
    except Exception as e:
        session.rollback()
        raise Exception(f"Error seeding database: {e}")