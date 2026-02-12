# 2026 Spotify wrapped unwrapped
## FFAM-MDAP Collab
from load_json_files import load_json_files
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

# load json files
folder = "/Users/abelton/Library/CloudStorage/OneDrive-TheUniversityofMelbourne/Projects/Spotify"
folder = "."

json_data = load_json_files(folder)
#print(json_data.keys())

selectedfiles = ['Inferences.json','Wrapped2024.json', 'YourLibrary.json']

capsuledf = pd.DataFrame()
keysdf = pd.DataFrame(columns=['file','top_level_key','key','value_sample'])
# inferences
samplekeys = ['inferences', 'demographic', 'interest']
# yoursoundcapsule
samplekeys= samplekeys + ['stats', 'highlights']
# Playlist1
samplekeys= samplekeys + ['playlists']
print(samplekeys)
exploring = False


if (exploring):
    for file_name, data in json_data.items():
            print(f"\n--- Sample from {file_name} ---")
            if isinstance(data, list):
                print(data[:2])  # Print first 2 items if it's a list
            elif isinstance(data, dict):
                sample_items = list(data.items())[:2]
                for key, value in sample_items:
                    print(f"{key}: {value}")

# show a sample from each selected json file
for file_name, data in json_data.items():
        if isinstance(data, dict):
            # get toplevel keys
            top_level_keys = list(data.keys())
            for key,value in data.items():
                keysdf = pd.concat([keysdf, pd.DataFrame({'file':[file_name],'top_level_key':[key],'key':[key],'value_sample':[str(value)[:100]]})], ignore_index=True)
        if isinstance(data, list):
            keysdf = pd.concat([keysdf, pd.DataFrame({'file':[file_name],'top_level_key':'none','key':'none','value_sample':[str(data[0])[:100]]})], ignore_index=True)
keysdf.to_csv("spotify_json_keys_overview.csv", index=False)       

# get demographic, interest and custom1p from inferences json file
demographics = []       
interests = []
custom1p = []
for file_name, data in json_data.items():
    if 'Inferences' in file_name:
        for item in data['inferences']:
            if 'demographic' in item:
                demographics.append(item.replace('demographic_',''))
            if 'interest' in item:
                interests.append(item.replace('interest_','').replace('-',' ').replace('_',' '))
            if '1P_Custom' in item:
                custom1p.append(item.replace('1P_Custom_','').replace('-',' ').replace('_',' '))

demographics.sort()
interests.sort()
custom1p.sort()

print(f"Demographics: {demographics}")
print(f"Interests: {interests}")
print(f"Custom1p: {custom1p}")

quit()

# get stats and highlights from yoursouncapsule json file
highlights = []
stats=[]
for file_name, data in json_data.items():
    if 'YourSoundCapsule' in file_name:
        for item in data['stats']:
            stats.append(item)
        for item in data['highlights']:
            highlights.append(item)

highdf = pd.DataFrame(highlights)
#highcols = ['date', 'highlightType', 'proportionListeningHighlight', 'milestoneHighlight', 'multiEntityMilestoneHighlight']
#statscols =  ['date', 'streamCount', 'secondsPlayed', 'topTracks', 'topArtists', 'topGenres']
statsdf = pd.DataFrame(stats)

for i, row in statsdf.iterrows():
    # flatten topTracks, topArtists, topGenres
    for col in ['topTracks', 'topArtists', 'topGenres']:
        if col in row and isinstance(row[col], list):
            flattened = ', '.join([item['name'] for item in row[col]])
            statsdf.at[i, col] = flattened

print(statsdf.head())
Quit()
# print(statsdf)

# get most recent streaming history
files = [fname for fname in json_data.keys() if 'Streaming_History' in fname]
filesdf = pd.DataFrame(files, columns=['fname'])
filesdf[['start year','end year']] = filesdf['fname'].apply(lambda x: pd.Series([
    int(x.replace('.json','').split('_')[3].split('-')[0]),
    int(x.replace('.json','').split('_')[3].split('-')[1])]))
print(filesdf)
recentfile = filesdf.sort_values(by=['end year','start year'], ascending=False).iloc[0]['fname']
print(f"Most recent streaming history file: {recentfile}")

streaminghistorydf = pd.DataFrame(json_data[recentfile])
streaminghistorydf['ts'] = pd.to_datetime(streaminghistorydf['ts'])
streaminghistorydf['day'] = streaminghistorydf['ts'].dt.to_period('D')
# group streaming history by month from ts column and create columns with sum of ms_played and list of master-metadata_track_name

monthly_streams = streaminghistorydf.groupby('day').agg({
    'ms_played': lambda x: round(x.sum() / 60000),  # Convert to minutes
    'master_metadata_track_name': lambda x: list(x),
    'master_metadata_album_artist_name': lambda x: list(x),
    'master_metadata_album_album_name': lambda x: list(x)
}).reset_index()
monthly_streams.rename(columns={'ms_played': 'minutes_played'}, inplace=True)

# show a graph of daily minutes played
plt.figure(figsize=(12, 6))

# Convert period to timestamp for plotting
monthly_streams['date'] = monthly_streams['day'].apply(lambda x: x.to_timestamp())
monthly_streams['year_month'] = monthly_streams['date'].dt.to_period('M')
# filter to last 12 months
one_year_ago = pd.Timestamp.now() - pd.DateOffset(months=12)
monthly_streams = monthly_streams[monthly_streams['date'] >= one_year_ago]

# Find the day with max minutes played for each month
max_days_idx = monthly_streams.groupby('year_month')['minutes_played'].idxmax()

# Plot all data points in default color
plt.plot(monthly_streams['date'], monthly_streams['minutes_played'], marker='o', markersize=3, color='steelblue', label='Daily plays')

# Highlight max days in purple
max_days = monthly_streams.loc[max_days_idx]
plt.scatter(max_days['date'], max_days['minutes_played'], color='purple', s=50, zorder=5, label='Peak day each month')

# Add annotations for peak days
for idx, row in max_days.iterrows():
    plt.annotate(row['date'].strftime('%a %d %b'), 
                 xy=(row['date'], row['minutes_played']),
                 xytext=(0, 10),  # 10 points above
                 textcoords='offset points',
                 ha='center',
                 fontsize=8,
                 color='purple',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='purple', alpha=0.7))

# Format x-axis to show monthly ticks
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
plt.xticks(rotation=45)

plt.title('Daily Minutes Played')
plt.xlabel('Month')
plt.ylabel('Minutes Played')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig('daily_minutes_played.png')
# plt.show()

print("now tope artists per month")
dfcolumns = ['ts', 'platform', 'ms_played', 'conn_country', 'ip_addr',
       'master_metadata_track_name', 'master_metadata_album_artist_name',
       'master_metadata_album_album_name', 'spotify_track_uri', 'episode_name',
       'episode_show_name', 'spotify_episode_uri', 'audiobook_title',
       'audiobook_uri', 'audiobook_chapter_uri', 'audiobook_chapter_title',
       'reason_start', 'reason_end', 'shuffle', 'skipped', 'offline',
       'offline_timestamp', 'incognito_mode']
# data wrangling to get top artists for each month by total minutes played
streaminghistorydf['year_month'] = streaminghistorydf['ts'].dt.to_period('M')

print(streaminghistorydf['reason_start'].unique().tolist())
print(streaminghistorydf['shuffle'].unique().tolist())

monthly_artists = streaminghistorydf.groupby(['year_month', 'master_metadata_album_artist_name']).agg({
    'ms_played': lambda x: round(x.sum() / 60000)  # Convert to minutes  
}).reset_index()
monthly_artists.rename(columns={'ms_played': 'minutes_played'}, inplace=True)
monthly_artists['Ranking'] = monthly_artists.groupby('year_month')['minutes_played'].rank(ascending=False, method='first')
artists_in_order= monthly_artists[monthly_artists['Ranking'] <= 5]['master_metadata_album_artist_name'].unique().tolist()
print("nbr of artists total")
print(len(monthly_artists['master_metadata_album_artist_name'].unique().tolist()))
print("nbr of artists in focus")
print(len(artists_in_order))
#monthly_artists.drop(monthly_artists[monthly_artists['master_metadata_album_artist_name'].isin(artists_in_order)].index, inplace=True)

# filter to last 12 months
one_year_ago = pd.Timestamp.now() - pd.DateOffset(months=12)
monthly_artists = monthly_artists[monthly_artists['year_month'] >= one_year_ago.to_period('M')]

# Sort by year_month and minutes_played to see top artists per month
monthly_artists = monthly_artists.sort_values(['year_month', 'minutes_played'], ascending=[True, False])
top_artists = monthly_artists['master_metadata_album_artist_name'].unique().tolist()

# Create a list of artists sorted by average ranking
artists_avg_ranking = monthly_artists.groupby('master_metadata_album_artist_name').agg({
    'Ranking': 'mean',
    'minutes_played': 'sum',
    'year_month': 'count'  # Number of months they appeared in
}).reset_index()
artists_avg_ranking.rename(columns={'year_month': 'months_appeared'}, inplace=True)
artists_avg_ranking['weighted_score'] = artists_avg_ranking['Ranking'] * (1 + (12 - artists_avg_ranking['months_appeared']) * 0.5)
artists_avg_ranking = artists_avg_ranking.sort_values('weighted_score')
artists_in_order = artists_avg_ranking['master_metadata_album_artist_name'].tolist()

# change ranking to 6 when its above 5
monthly_artists.loc[monthly_artists['Ranking'] > 5, 'Ranking'] = 6

# insert a row between each month for each artist to make a pretty animation later

# create a scatter plot with a circle for each artist for the month 2023-08 where the size of the circle is proportional to minutes played, y axis is rank and x axis is artist name
months = monthly_artists['year_month'].unique().tolist()
print(months)

for month_to_plot in months:
    print(f"Plotting month: {month_to_plot}")
    plt.figure(figsize=(10, 6))  # Create NEW figure for each month
    framenbr = 0
    #data_to_plot = monthly_artists[(monthly_artists['year_month'] == month_to_plot)&(monthly_artists['Ranking']<=5)]
    data_to_plot = monthly_artists[(monthly_artists['year_month'] == month_to_plot)]

    # Create a categorical variable with the desired order
    data_to_plot['artist_ordered'] = pd.Categorical(
        data_to_plot['master_metadata_album_artist_name'],
        categories=artists_in_order,
        ordered=True
    )
    print(data_to_plot) 
    plt.scatter(data_to_plot['artist_ordered'], data_to_plot['Ranking'], 
                s=data_to_plot['minutes_played']*10, alpha=0.6, color='teal', edgecolors='w', linewidth=0.5)

    # add annotations for each point with artist name and minutes played
    for i, row in data_to_plot.iterrows():
        plt.annotate(f"{row['master_metadata_album_artist_name']} ({row['minutes_played']} min)", 
                    xy=(row['artist_ordered'], row['Ranking']),
                    xytext=(0, 20),  # 10 points above
                    textcoords='offset points',
                    ha='center',
                    fontsize=8)

    plt.title(f'Top Artists for {month_to_plot} by Minutes Played')
    #plt.xlabel('Artist Name')
    #plt.ylabel('Rank')
    #plt.grid()
    plt.xticks([],[])
    plt.tight_layout()
    plt.savefig(f'top_artists_{month_to_plot}_{framenbr}.png')

        #framenbr += 1
        #plt.show()
