import urllib
import json

class LyricsWiki:
  @staticmethod
  def search(artist, song = ""):
    url = "http://lyrics.wikia.com/api.php?artist=%s&song=%s&fmt=realjson" % (urllib.quote_plus(artist), urllib.quote_plus(song))
    conn = urllib.urlopen(url)
    response = conn.read()
    return LyricsWiki.__parsed_result(response)

  @staticmethod
  def __parsed_result(str):
    parsed = json.loads(str)
    if parsed["page_id"]:
      return { "artist"  : parsed["artist"],
               "song"    : parsed["song"],
               "url"     : parsed["url"],
               "snippet" : parsed["lyrics"] }
    else:
      return None