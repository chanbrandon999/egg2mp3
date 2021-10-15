

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
  print(str(i) + "/" + str(num_songs) + " \tsong_dir:: " + song_dir)
  albumart_link = 69
  song_file_link = 69
  try:

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

  try:

    audio_filename = str(song_dir + " - " + song_name + " - " + song_author + ".mp3")
    
    audio_path_input = song_dir + "\\" + song_file_link
    # audio_path_output = WORKING_DIR + "\\" + song_dir + "\\" + audio_filename
    audio_path_output = FINAL_DIR  + "\\" + audio_filename
    # audio_path_output_short = WORKING_DIR + "\\" + song_dir + "\\" + str(song_dir) + ".mp3"
    audio_path_output_short = FINAL_DIR  + "\\" + str(song_dir) + ".mp3"

    if not (os.path.isfile(audio_path_output) or (os.path.isfile(audio_path_output_short))):
      # Reprocessing audio files
      print("processing audio:: " + audio_path_input)
      print("processing to:: " + audio_path_output)
      audio = AudioSegment.from_ogg(str(WORKING_DIR + "\\" + audio_path_input))
      # audio.export( audio_filename, format="mp3")
      try:
        audio.export( (audio_path_output), format="mp3")
      except:
        audio.export( (audio_path_output_short), format="mp3")

    pass

    try:



      if not os.path.isfile(audio_path_output):
        audio_path_output = audio_path_output_short

      metadata = EasyID3(audio_path_output)

      if 'title' not in metadata:
        print("Tagging audio:: " + audio_path_output)
        metadata['title'] = song_name
        metadata['artist'] = song_author
        metadata['albumartist'] = song_author
        metadata.save()

      metadata = ID3(audio_path_output)

      # metadata.delall("APIC") # Delete every APIC tag (Cover art)
      # metadata.save()
      # print((metadata.getall("APIC")))

      if 1 == 1 and (len(str(metadata.getall("APIC"))) < 10):

        if os.path.isfile(song_dir + "\\" + albumart_link) and (".png" not in albumart_link):
          # metadata = ID3(audio_path_output)
          print("cover from the albumart_link:: " + albumart_link)
          with open(song_dir + "\\" + albumart_link, 'rb') as albumart:
            print("open ok")
            metadata['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc=u'Cover',
                data=albumart.read()
              )
        elif os.path.isfile(song_dir + "\\" + albumart_link):
          # metadata = ID3(audio_path_output)
          print("cover from the albumart_link:: " + albumart_link)
          with open(song_dir + "\\" + albumart_link, 'rb') as albumart:
            print("open ok")
            metadata['APIC'] = APIC(
                encoding=3,
                mime='image/png',
                type=3, desc=u'Cover',
                data=albumart.read()
              )
        else:
          print("Error in finding proper image")
          if os.path.isfile(song_dir + "\\cover.jpg"):
            metadata = ID3(audio_path_output)
            # print("cover")
            with open(song_dir + "\\cover.jpg", 'rb') as albumart:
              metadata['APIC'] = APIC(
                  encoding=3,
                  mime='image/jpeg',
                  type=3, desc=u'Cover',
                  data=albumart.read()
                )
          elif os.path.isfile(song_dir + "\\Cover.jpg"):
            # print("cover")
            with open(song_dir + "\\Cover.jpg", 'rb') as albumart:
              metadata['APIC'] = APIC(
                  encoding=3,
                  mime='image/jpeg',
                  type=3, desc=u'Cover',
                  data=albumart.read()
                )
          elif os.path.isfile(song_dir + "\\" + song_dir + ".jpg"):
            # print("cover")
            with open(song_dir + "\\" + song_dir + ".jpg", 'rb') as albumart:
              metadata['APIC'] = APIC(
                  encoding=3,
                  mime='image/jpeg',
                  type=3, desc=u'Cover',
                  data=albumart.read()
                )
          else:
            print("no cover")

        metadata.save()
        # print("Tagging Success")
    except Exception as e:
      print("Tagging Error::  " + str(e))
      pass


  except Exception as e2:
    print("Big Error!!::  " + str(e2))
    pass

  print("   ")























