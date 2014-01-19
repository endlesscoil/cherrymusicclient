def get_track_info(func):
    def inner(track):
        if not track._retrieved_song_info:
            track.get_info()

        return func(track)
    return inner