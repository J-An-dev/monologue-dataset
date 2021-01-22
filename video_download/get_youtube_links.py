import urllib.request
import json
import csv

def get_all_video_in_channel(channel_id):
    api_key = 'Your_YouTube_API_KEY'

    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=50&q=weekly'.format(api_key, channel_id)

    video_links = []
    video_titles = []
    CSV = []
    url = first_url
    while True:
        inp = urllib.request.urlopen(url)
        resp = json.load(inp)

        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append(base_video_url + i['id']['videoId'])
                video_titles.append(i['snippet']['title']+'='+i['id']['videoId'])
                CSV.append('obama,' + i['snippet']['title']+'='+i['id']['videoId'] + ',' + base_video_url + i['id']['videoId'])


        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break

    CSV = '\n'.join(CSV)  ## CSV is str type right now, instead of list
    return video_links, video_titles, CSV

links, titles, CSV_list= get_all_video_in_channel('UCDGknzyQfNiThyt4vg4MlTQ')


print(CSV_list)

text_file = open("videos_links_obama.csv", "w")
text_file.write(CSV_list)
text_file.close()





