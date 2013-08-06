import json
from subprocess import Popen, PIPE
from LyricsWiki import LyricsWiki
from Feedback import Feedback

def find():
  feedback = Feedback()
  song = current_song()
  if "error" in song:
    feedback.add_item(song["error"])
  else:
    result = LyricsWiki.search(song["artist"], song["song"])
    if result:
      title = "Show lyrics"
      subtitle = "%s - %s" % (result["artist"], result["song"])
      feedback.add_item("Show lyrics", subtitle, result["url"])
    else:
      feedback.add_item("No lyrics found", "", "", "no")
  return feedback

def current_song():
  script = """
  if application "Spotify" is running then
    tell application "Spotify"
      set player_state to player state
      if player_state is stopped then
        return "{\\\"error\\\":\\\"Player is stopped\\\"}"
      else
        set artist_name to artist of current track
        set song_name to name of current track
        return "{\\\"artist\\\":\\\"" & artist_name & "\\\",\\\"song\\\":\\\"" & song_name & "\\\"}"
      end if
    end tell
  else
    return "{\\\"error\\\":\\\"Spotify is not running\\\"}"
  end if"""
  return json.loads(run_applescript(script))

def run_applescript(script):
  p = Popen(["osascript", "-"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  stdout, stderr = p.communicate(script)
  return stdout
