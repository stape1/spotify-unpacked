# 2026 Spotify wrapped unwrapped
## FFAM-MDAP Collab
### My streaming history and playlist exploration
from load_json_files import load_json_files
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from adjustText import adjust_text

# load json files
folder = "/Users/abelton/Library/CloudStorage/OneDrive-TheUniversityofMelbourne/Projects/Spotify"
folder = "."

json_data = load_json_files(folder)
#print(json_data.keys())

data = []
# explore playlist data
files = [fname for fname in json_data.keys() if 'Playlist' in fname]
for f in files:
    print(f)
    data.append(json_data[f])

print(data[2]['playlists'][0].keys())
playlistdf = pd.json_normalize(data[2]['playlists'])

tracksdf = pd.json_normalize(data[2]['playlists'], record_path='items', meta=['name', 'lastModifiedDate', 'description'])
print(tracksdf.sample(3))

# Combine all playlists from all files
all_items = []

all_items.append(pd.json_normalize(
        data[2]['playlists'],
        record_path='items',
        meta=['name', 'lastModifiedDate', 'description']
    ))

items_df = pd.concat(all_items, ignore_index=True)
print(items_df.columns)
print(items_df[['name','track.trackName']].sample(5))
print('==========================')
print(items_df[items_df['name']=='gym']['track.trackName'].sample(5))


# get most recent streaming history
files = [fname for fname in json_data.keys() if 'Streaming_History' in fname]
filesdf = pd.DataFrame(files, columns=['fname'])
filesdf[['start year','end year']] = filesdf['fname'].apply(lambda x: pd.Series([
    int(x.replace('.json','').split('_')[3].split('-')[0]),
    int(x.replace('.json','').split('_')[3].split('-')[1])]))
recentfile = filesdf.sort_values(by=['end year','start year'], ascending=False).iloc[0]['fname']
print(f"Most recent streaming history file: {recentfile}")

streaminghistorydf = pd.DataFrame(json_data[recentfile])
streaminghistorydf['ts'] = pd.to_datetime(streaminghistorydf['ts'])
streaminghistorydf['day'] = streaminghistorydf['ts'].dt.to_period('D')
print(streaminghistorydf.columns)

# add column for playlist name if track is in a playlist
# ie items_df['name] where streaminghistorydf['spotify_track_uri'] = items_df['track.trackUri']

# Create a mapping from track URI to playlist names (handles multiple playlists per track)
track_to_playlists = items_df.groupby('track.trackUri')['name'].apply(list)

# Map track URIs to playlist names
streaminghistorydf['playlist'] = streaminghistorydf['spotify_track_uri'].map(track_to_playlists)

# Add flag for whether track is from a playlist
streaminghistorydf['is_from_playlist'] = streaminghistorydf['playlist'].notna()

# Aggregate by day and playlist status
monthly_streams = streaminghistorydf.groupby(['day', 'is_from_playlist']).agg({
    'ms_played': lambda x: round(x.sum() / 60000),  # Convert to minutes
}).reset_index()
monthly_streams.rename(columns={'ms_played': 'minutes_played'}, inplace=True)

# Pivot to separate columns for playlist vs non-playlist
monthly_streams_pivot = monthly_streams.pivot(index='day', columns='is_from_playlist', values='minutes_played').fillna(0)
monthly_streams_pivot.columns = ['non_playlist', 'playlist']
monthly_streams_pivot = monthly_streams_pivot.reset_index()

# show a graph of daily minutes played
plt.figure(figsize=(12, 6))

# Convert period to timestamp for plotting
monthly_streams_pivot['date'] = monthly_streams_pivot['day'].apply(lambda x: x.to_timestamp())

# filter to last 12 months
one_year_ago = pd.Timestamp.now() - pd.DateOffset(months=12)
monthly_streams_pivot = monthly_streams_pivot[monthly_streams_pivot['date'] >= one_year_ago]

# Calculate total minutes and find peak day for each month
monthly_streams_pivot['total_minutes'] = monthly_streams_pivot['playlist'] + monthly_streams_pivot['non_playlist']
monthly_streams_pivot['year_month'] = monthly_streams_pivot['date'].dt.to_period('M')
max_days_idx = monthly_streams_pivot.groupby('year_month')['total_minutes'].idxmax()
max_days = monthly_streams_pivot.loc[max_days_idx]

# Plot stacked area chart
plt.fill_between(monthly_streams_pivot['date'], 0, monthly_streams_pivot['playlist'], 
                 alpha=0.6, color='steelblue', label='From Playlists')
plt.fill_between(monthly_streams_pivot['date'], monthly_streams_pivot['playlist'], 
                 monthly_streams_pivot['playlist'] + monthly_streams_pivot['non_playlist'], 
                 alpha=0.6, color='coral', label='Not in Playlists')

# Add line plots on top
plt.plot(monthly_streams_pivot['date'], monthly_streams_pivot['playlist'], 
         color='darkblue', linewidth=1, alpha=0.8)
plt.plot(monthly_streams_pivot['date'], monthly_streams_pivot['playlist'] + monthly_streams_pivot['non_playlist'], 
         color='darkred', linewidth=1, alpha=0.8)

# Highlight peak days
plt.scatter(max_days['date'], max_days['total_minutes'], color='purple', s=50, zorder=5, label='Peak day each month')

# Add annotations for peak days
for idx, row in max_days.iterrows():
    playlist_pct = (row['playlist'] / row['total_minutes'] * 100) if row['total_minutes'] > 0 else 0
    non_playlist_pct = (row['non_playlist'] / row['total_minutes'] * 100) if row['total_minutes'] > 0 else 0
    annotation_text = f"{row['date'].strftime('%a %d %b')}\nPlaylist: {int(row['playlist'])}m ({playlist_pct:.0f}%)\nNon-playlist: {int(row['non_playlist'])}m ({non_playlist_pct:.0f}%)"
    plt.annotate(annotation_text, 
                 xy=(row['date'], row['total_minutes']),
                 xytext=(0, 10),  # 10 points above
                 textcoords='offset points',
                 ha='center',
                 fontsize=7,
                 color='purple',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='purple', alpha=0.8))

# Format x-axis to show monthly ticks
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
plt.xticks(rotation=45)

plt.title('Daily Minutes Played: Playlist vs Non-Playlist Songs')
plt.xlabel('Month')
plt.ylabel('Minutes Played')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('playlistvsother.png')
plt.show()

# show playlist names in order of most recently played (even if only 1 track played)
recent_playlists = streaminghistorydf[streaminghistorydf['is_from_playlist']].sort_values(by='ts', ascending=False)
# Explode the playlist column to get individual playlist names
recent_playlists_exploded = recent_playlists.explode('playlist')
recent_playlists_names = recent_playlists_exploded['playlist'].drop_duplicates().tolist()
# get nbr of days it was played (at least one song played on that day)
playlist_days_played = recent_playlists_exploded.groupby('playlist')['day'].nunique()

print("Recently played playlists:")
for pname in recent_playlists_names:
    days_played = playlist_days_played.get(pname, 0)
    print(f"- {pname} (played on {days_played} days)")

# plot nbr days played for each playlist as a bubble chart
plt.figure(figsize=(12, 8))

# Calculate additional metrics for bubble chart
playlist_stats = recent_playlists_exploded.groupby('playlist').agg({
    'day': 'nunique',  # Number of unique days
    'ms_played': lambda x: x.sum() / 60000  # Total minutes played
}).reset_index()
playlist_stats.columns = ['playlist', 'days_played', 'total_minutes']

# Calculate average minutes per day
playlist_stats['avg_minutes_per_day'] = playlist_stats['total_minutes'] / playlist_stats['days_played']

# Sort by days played
playlist_stats = playlist_stats.sort_values('days_played', ascending=False)

# Create bubble chart
# X-axis: days played, Y-axis: total minutes, Size: average minutes per day
scatter = plt.scatter(playlist_stats['days_played'], 
                     playlist_stats['total_minutes'],
                     s=playlist_stats['avg_minutes_per_day'] * 50,  # Scale bubble size
                     c=range(len(playlist_stats)),  # Color by rank
                     cmap='viridis',
                     alpha=0.2,
                     edgecolors='black',
                     linewidth=1)

# Add playlist name labels to bubbles with adjustText to avoid overlap
try:
    
    texts = []
    for idx, row in playlist_stats.iterrows():
        text = plt.annotate(row['playlist'], 
                    xy=(row['days_played'], row['total_minutes']),
                    ha='center', 
                    va='center',
                    fontsize=8,
                    weight='bold')
        texts.append(text)
    
    # Adjust text positions to avoid overlaps
    adjust_text(texts, 
                arrowprops=dict(arrowstyle='-', color='gray', lw=0.5, alpha=0.5),
                expand_points=(1.5, 1.5))
except ImportError:
    # Fallback: only show labels for top playlists if adjustText not available
    top_n = min(10, len(playlist_stats))
    for idx, row in playlist_stats.head(top_n).iterrows():
        plt.annotate(row['playlist'], 
                    xy=(row['days_played'], row['total_minutes']),
                    xytext=(5, 5),
                    textcoords='offset points',
                    ha='left',
                    fontsize=8,
                    weight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.7))

plt.xlabel('Number of Days Played')
plt.ylabel('Total Minutes Played')
plt.title('Playlist Activity: Days vs Total Minutes\n(Bubble size = avg minutes per day)')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('playlist_days_played.png')
plt.show()  
