
import os
import sys
import json
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC


# Root of beat saber map folders! 
# Either put this python file at the root of the [CustomLevels] folder
# OR 
# Put the full path in this variable. 
WORKING_DIR = str(os.getcwd()) + ""

# CHANGE TO WHERE YOU WANT YOUR MUSIC TO END UP 
FINAL_DIR = str("E:\\Music\\My Music 2\\Beat Saber 2")

i = 0
num_songs = len(os.listdir(WORKING_DIR))
print(num_songs)

for song_dir in os.listdir(WORKING_DIR):
  i += 1

  # Use for not converting certain songs 
  path_part_deny_conversion = "XXXXXXXXXXXXXXXX"
  if path_part_deny_conversion in song_dir:
    print("skipping...")
    continue


  # Prints current song directory 
  print(str(i) + "/" + str(num_songs) + " \tsong_dir:: " + song_dir)
  albumart_link = 69
  song_file_link = 69

# _  _ ____ ___ ____ ___  ____ ___ ____    ____ ____ _    _    ____ ____ ___ _ ____ _  _ 
# |\/| |___  |  |__| |  \ |__|  |  |__|    |    |  | |    |    |___ |     |  | |  | |\ | 
# |  | |___  |  |  | |__/ |  |  |  |  |    |___ |__| |___ |___ |___ |___  |  | |__| | \| 
# Collect the info of the song from the beat saber info.dat file 
  no_exception_metadata = True

  try:
    with open(str(song_dir) + "\\Info.dat", encoding="utf8") as song_dat_raw:
      song_dat_json = json.load(song_dat_raw)
      # print(song_dat_json)  # uncomment to print if you want

      # Gets the name utilizing primary name and sub-name if a useful one exists
      # Sub-name includes the [feat. artist] labels 
      if len(song_dat_json["_songSubName"]) > 2:
        song_name = song_dat_json["_songName"] + " - " + song_dat_json["_songSubName"]
      else:
        song_name = song_dat_json["_songName"]

      # Find song author but if it does not exist, get the level author name. Will be wrong but better than nothing.
      if len(song_dat_json["_songAuthorName"]) > 0:
        song_author = song_dat_json["_songAuthorName"]
      else:
        song_author = song_dat_json["_levelAuthorName"]

      # Remove spaces at the beginning and at the end of the string
      song_author = song_author.strip() 
      
      # Prepare to find album art and the file. 
      albumart_link = song_dat_json["_coverImageFilename"]
      song_file_link = song_dat_json["_songFilename"]

      # print("#####SONG#####")
      # print(song_name + " \t\tby \t\t" + song_author)
  except Exception as e2:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

    print("ERROR WITH METADATA EXTRACTION! \t" + str(e2))
    pass

  try:
    with open(str(song_dir) + "\\Info.dat") as song_dat_raw:
      song_dat_json = json.load(song_dat_raw)
      # print(song_dat_json)  # uncomment to print if you want

      # Gets the name utilizing primary name and sub-name if a useful one exists
      # Sub-name includes the [feat. artist] labels 
      if len(song_dat_json["_songSubName"]) > 2:
        song_name_non_utf8 = song_dat_json["_songName"] + " - " + song_dat_json["_songSubName"]
      else:
        song_name_non_utf8 = song_dat_json["_songName"]

      # Find song author but if it does not exist, get the level author name. Will be wrong but better than nothing.
      if len(song_dat_json["_songAuthorName"]) > 0:
        song_author_non_utf8 = song_dat_json["_songAuthorName"]
      else:
        song_author_non_utf8 = song_dat_json["_levelAuthorName"]

      # Remove spaces at the beginning and at the end of the string
      song_author_non_utf8 = song_author_non_utf8.strip() 
      
      # Prepare to find album art and the file. 
      albumart_link = song_dat_json["_coverImageFilename"]
      song_file_link = song_dat_json["_songFilename"]

      # print("#####SONG#####")
      # print(song_name + " \t\tby \t\t" + song_author)
  except Exception as e2:
    no_exception_metadata = False
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

    print("ERROR WITH METADATA EXTRACTION! \t" + str(e2))
    print("CORRECTING PREVIOUS FILE TAGS!")
    pass

# ____ ____ _  _ _  _ ____ ____ ___    ____ _  _ ___  _ ____ 
# |    |  | |\ | |  | |___ |__/  |     |__| |  | |  \ | |  | 
# |___ |__| | \|  \/  |___ |  \  |     |  | |__| |__/ | |__| 
  try:

    # Desired output filename
    # mapcode - song name - song author.mp3
    # #ASDFASDFASDFSADFASDFSDF # audio_filename = str((song_dir) + " - " + (song_name) + " - " + (song_author) + ".mp3")
    audio_filename = str((song_dir) + " - " + (song_name_non_utf8) + " - " + (song_author_non_utf8) + ".mp3")
    
    # Find input file from the beat saber folders
    print(song_file_link)
    audio_path_input = str(song_dir) + "\\" + str(song_file_link)
    # Figure out where converted file must go
    audio_path_output = (FINAL_DIR  + "\\" + audio_filename)

    # Must get rid of filename with the colon in the end. 
    # Overrides previous audio path output prepared from [audio_filename]
    if audio_path_output.count(':') > 1:
      audio_path_output = (FINAL_DIR  + "\\" + song_dir + ".mp3")

    audio_path_output_short = (FINAL_DIR  + "\\" + song_dir + ".mp3")  # For alternate if filename is too long


    metadata_saved = {}
    # Check for existing converted files to overwrite. 
    if os.path.isfile(audio_path_output):
      metadata_saved = EasyID3(audio_path_output)
    if os.path.isfile(audio_path_output_short):
      audio_path_output = audio_path_output_short
      metadata_saved = EasyID3(audio_path_output_short)

    # If the metadata doesn't exist, reproecss audio.
    # Set to true to do a in-place replacement of audio 
    # if 'title' not in metadata_saved:
    if False:

      print("processing audio:: " + audio_path_input)
      print("processing to:: " + audio_path_output)
      
      audio = AudioSegment.from_ogg(str(WORKING_DIR + "\\" + audio_path_input))


      # Maximum bitrate set to 320k
      # BITRATE IS VARIABLE BITRATE
      # https://github.com/jiaaro/pydub/blob/master/API.markdown#:~:text=parameters%20%7C%20example%3A%20%5B%22%2Dac%22%2C%20%222%22%5D%20Pass%20additional
      # https://www.ffmpeg.org/ffmpeg.html#:~:text=%2Daq%20q%20(,for%20%2Dq%3Aa.
      try:
        audio.export( (audio_path_output), format="mp3", bitrate="320k", parameters=["-q:a", "0"])
      except:
        print("error in saving! Using short path")
        audio.export( (audio_path_output_short), format="mp3", bitrate="320k", parameters=["-q:a", "0"])

    pass

    # ____ ____ _  _ ____    ___ ____ ____ ____ 
    # [__  |__| |  | |___     |  |__| | __ [__  
    # ___] |  |  \/  |___     |  |  | |__] ___] 
    try:

      if not os.path.isfile(audio_path_output):
        audio_path_output = audio_path_output_short
      elif not os.path.isfile(audio_path_output_short):
        pass

      # # Restoring previous tags if was converting files 
      # if 'title' in metadata_saved:
      #   print("Restoring Previous Tags")
      #   metadata_saved.save()
      # else:
      metadata = EasyID3(audio_path_output)

      # Rebuild metadata if does not exist
      # Set to true to overwrite metadata
      # if 'title' not in metadata or not song_name_non_utf8.isascii() or not song_author_non_utf8.isascii():
      if 'title' not in metadata:
      # if True:
        print("Tagging audio:: " + audio_path_output)
        metadata['title'] = song_name
        metadata['artist'] = song_author
        metadata['albumartist'] = song_author
        print(metadata)
        print("song_name:: \t", song_name_non_utf8.isascii())
        print("song_author:: \t", song_author_non_utf8.isascii())
        metadata.save()
        pass
      pass

# ____ ___  ___     ____ _    ___  _  _ _  _   ____ ____ ___ 
# |__| |  \ |  \    |__| |    |__] |  | |\/|   |__| |__/  |  
# |  | |__/ |__/    |  | |___ |__] |__| |  |   |  | |  \  |  

      # Load the converted file 
      metadata = ID3(audio_path_output)

      # # Delete cover art in file metadata
      # metadata.delall("APIC") 
      # metadata.save()
      # print((metadata.getall("APIC")))

      # APIC content must be empty 
      if (len(str(metadata.getall("APIC"))) < 10):

        # Get the included map cover image if exist 
        if os.path.isfile(song_dir + "\\" + albumart_link):

          # Inject the album art cover as a JPEG into the music file
          print("cover from the albumart_link:: " + albumart_link)
          with open(song_dir + "\\" + albumart_link, 'rb') as albumart:
            print("open ok")
            metadata['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=albumart.read() )
        else:
          print("Error in finding proper image")

        metadata.save()
        print("Image save success")
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










