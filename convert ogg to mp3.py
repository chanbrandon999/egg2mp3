

import os
import sys
import json
from pydub import AudioSegment
# import eyed3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC


WORKING_DIR = str(os.getcwd()) + ""
FINAL_DIR = str("E:\\Music\\My Music 2\\Beat Saber 2")

i = 0
num_songs = len(os.listdir(WORKING_DIR))

for song_dir in os.listdir(WORKING_DIR):
  i += 1

  # Use for testing 
  if "Crow" not in song_dir:
    continue
  if i > 3:
    # print(song_dir)
    # exit()
    pass


  print(str(i) + "/" + str(num_songs) + " \tsong_dir:: " + song_dir)
  albumart_link = 69
  song_file_link = 69
  try:

# _  _ ____ ___ ____ ___  ____ ___ ____    ____ ____ _    _    ____ ____ ___ _ ____ _  _ 
# |\/| |___  |  |__| |  \ |__|  |  |__|    |    |  | |    |    |___ |     |  | |  | |\ | 
# |  | |___  |  |  | |__/ |  |  |  |  |    |___ |__| |___ |___ |___ |___  |  | |__| | \| 
    with open(str(song_dir) + "\\Info.dat") as song_dat_raw:
      song_dat_json = json.load(song_dat_raw)
      # print(song_dat_json)
      if len(song_dat_json["_songSubName"]) > 2:
        song_name = song_dat_json["_songName"] + " - " + song_dat_json["_songSubName"]
      else:
        song_name = song_dat_json["_songName"]

      if len(song_dat_json["_songAuthorName"]) > 2:
        song_author = song_dat_json["_songAuthorName"]
      else:
        song_author = song_dat_json["_levelAuthorName"]
      song_author = song_author.strip()
      
      albumart_link = song_dat_json["_coverImageFilename"]
      song_file_link = song_dat_json["_songFilename"]

      # print("#####SONG#####")
      # print(song_name)
      # print("by")
      # print(song_author)
  except:
    # print("song author and name unknown")
    pass

# ____ ____ _  _ _  _ ____ ____ ___    ____ _  _ ___  _ ____ 
# |    |  | |\ | |  | |___ |__/  |     |__| |  | |  \ | |  | 
# |___ |__| | \|  \/  |___ |  \  |     |  | |__| |__/ | |__| 
  try:

    # Desired output filename
    audio_filename = str(song_dir + " - " + song_name + " - " + song_author + ".mp3")
    
    audio_path_input = song_dir + "\\" + song_file_link                   # Input file
    # audio_path_output = WORKING_DIR + "\\" + song_dir + "\\" + audio_filename
    audio_path_output = FINAL_DIR  + "\\" + audio_filename                # Normal savespace for audio files
    # audio_path_output_short = WORKING_DIR + "\\" + song_dir + "\\" + str(song_dir) + ".mp3"
    audio_path_output_short = FINAL_DIR  + "\\" + str(song_dir) + ".mp3"  # For alternate if filename is too long
      
    # Converts file normally
    if not (os.path.isfile(audio_path_output) or (os.path.isfile(audio_path_output_short))):
      metadata_saved = {}
      # Reprocessing audio files
      print("processing audio:: " + audio_path_input)
      print("processing to:: " + audio_path_output)
      audio = AudioSegment.from_ogg(str(WORKING_DIR + "\\" + audio_path_input))
      # audio.export( audio_filename, format="mp3")
      try:
        audio.export( (audio_path_output), format="mp3", bitrate="320k", parameters=["-q:a", "0"])
      except:
        audio.export( (audio_path_output_short), format="mp3", bitrate="320k", parameters=["-q:a", "0"])
    # Converts files to new bitrates while saving the previous metadata tags 
    else:
      metadata_saved = EasyID3(audio_path_output)
      # Reprocessing audio files
      print("Reprocessing audio:: " + audio_path_input)
      print("Reprocessing to:: " + audio_path_output)
      audio = AudioSegment.from_ogg(str(WORKING_DIR + "\\" + audio_path_input))
      # audio.export( audio_filename, format="mp3")
      try:
        audio.export( (audio_path_output), format="mp3", bitrate="320k", parameters=["-q:a", "0"])
      except:
        audio.export( (audio_path_output_short), format="mp3", bitrate="320k", parameters=["-q:a", "0"])

    pass

    # ____ ____ _  _ ____    ___ ____ ____ ____ 
    # [__  |__| |  | |___     |  |__| | __ [__  
    # ___] |  |  \/  |___     |  |  | |__] ___] 
    try:

      if not os.path.isfile(audio_path_output):
        audio_path_output = audio_path_output_short

      # Restoring Previous Tags
      if 'title' in metadata_saved:
        print("Restoring Previous Tags")
        metadata_saved.save()

      # Creating New Tags
      else:
        metadata = EasyID3(audio_path_output)

        # Rebuild metadata if does not exist
        if 'title' not in metadata:
          print("Tagging audio:: " + audio_path_output)
          metadata['title'] = song_name
          metadata['artist'] = song_author
          metadata['albumartist'] = song_author
          metadata.save()
          pass
        pass

# ____ ___  ___     ____ _    ___  _  _ _  _ ____ ____ ___ 
# |__| |  \ |  \    |__| |    |__] |  | |\/| |__| |__/  |  
# |  | |__/ |__/    |  | |___ |__] |__| |  | |  | |  \  |  

      metadata = ID3(audio_path_output)

      # Delete cover art in file metadata
      # metadata.delall("APIC") 
      # metadata.save()
      # print((metadata.getall("APIC")))

      if 1 == 1 and (len(str(metadata.getall("APIC"))) < 10):

        if os.path.isfile(song_dir + "\\" + albumart_link) and (".png" not in albumart_link):
          # metadata = ID3(audio_path_output)
          print("cover from the albumart_link:: " + albumart_link)
          with open(song_dir + "\\" + albumart_link, 'rb') as albumart:
            print("open ok")
            metadata['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=albumart.read() )
        elif os.path.isfile(song_dir + "\\" + albumart_link):
          # metadata = ID3(audio_path_output)
          print("cover from the albumart_link:: " + albumart_link)
          with open(song_dir + "\\" + albumart_link, 'rb') as albumart:
            print("open ok")
            metadata['APIC'] = APIC(encoding=3, mime='image/png', type=3, desc=u'Cover', data=albumart.read() )
        # else:
        #   print("Error in finding proper image")
        #   if os.path.isfile(song_dir + "\\cover.jpg"):
        #     metadata = ID3(audio_path_output)
        #     # print("cover")
        #     with open(song_dir + "\\cover.jpg", 'rb') as albumart:
        #       metadata['APIC'] = APIC(                  encoding=3,                  mime='image/jpeg',                  type=3, desc=u'Cover',                  data=albumart.read()                )
        #   elif os.path.isfile(song_dir + "\\Cover.jpg"):
        #     # print("cover")
        #     with open(song_dir + "\\Cover.jpg", 'rb') as albumart:
        #       metadata['APIC'] = APIC(                  encoding=3,                  mime='image/jpeg',                  type=3, desc=u'Cover',                  data=albumart.read()                )
        #   elif os.path.isfile(song_dir + "\\" + song_dir + ".jpg"):
        #     # print("cover")
        #     with open(song_dir + "\\" + song_dir + ".jpg", 'rb') as albumart:
        #       metadata['APIC'] = APIC(                  encoding=3,                  mime='image/jpeg',                  type=3, desc=u'Cover',                  data=albumart.read()                )
        #   else:
        #     print("no cover")

        metadata.save()
        # print("Tagging Success")
    except Exception as e:
      print("Tagging Error::  " + str(e))
      pass


  except Exception as e2:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

    print("Big Error!!::  " + str(e2))
    pass

  print("   ")























