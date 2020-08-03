#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# By: ElSysNet

# License: GPLv3

import textract, subprocess, os, fnmatch, re
from time import sleep

def execute_unix(inputcommand):
   p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
   (output, err) = p.communicate()
   p.wait()
   return output

def walklevel(some_dir, level=1):
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
                yield root, dirs, files
                num_sep_this = root.count(os.path.sep)
                if num_sep + level <= num_sep_this:
                        del dirs[:]

def matchedfiles(top, exts):
        hits = list()
        for root, dirnames, filenames in walklevel(top,0):
                for filename in filenames:
                        if any(fnmatch.fnmatch(filename.lower(), ext) for ext in exts):
                                hits.append(filename)
        return hits

def create_chunked_textlist(string, divider):
        words = string.split()
        v = divider
        wchks = len(words)/v
        down = lambda n: n//v*v
        round_wchks = down(wchks)
        gleiche = round_wchks*v
        rest = len(words)-(round_wchks*v)
        x = 0
        m = int(round_wchks)
        new_list = []
        x_list = ""
        end_list = []
        while x <= gleiche-int(round_wchks):
                new_list = new_list + words[x:m]
                for w in new_list:
                        x_list = x_list + " " + w
                x = x + int(round_wchks)
                m = m + int(round_wchks)
                end_list.append(x_list)
                x_list = ""
                new_list = []
        for w in words[x:x+int(rest)]:
                x_list = x_list + " " + w
        end_list.append(x_list)
        return end_list

if __name__ == '__main__':
        folder_in_deu = "/home/user/TTS/TTS-INPUT_deu/"
        folder_in_eng = "/home/user/TTS/TTS-INPUT_eng/"
        tmp_folder = "/var/tmp/"
        folder_out = "/home/user/TTS/TTS-OUTPUT/"
        folder_archiv = "/home/user/TTS/TTS-ARCHIV/"
        while True:
                try:
                        text_file_list_deu = matchedfiles(folder_in_deu, ["*.pdf", "*.rtf", "*.pdf", "*.docx", "*.txt", "*.epub"])
                        if text_file_list_deu:
                                for text_file in text_file_list_deu:
                                        if ".docx" in text_file:
                                                wav_file = text_file[:-5] + ".wav"
                                                mp3_file = text_file[:-5] + ".mp3"
                                        elif ".epub" in text_file:
                                                wav_file = text_file[:-5] + ".wav"
                                                mp3_file = text_file[:-5] + ".mp3"
                                        else:
                                                wav_file = text_file[:-4] + ".wav"
                                                mp3_file = text_file[:-4] + ".mp3"
                                        string = textract.process(folder_in_deu+text_file).decode('utf-8', errors="replace")
                                        cmd0 = "mv %s" % folder_in_deu + text_file + " %s" % folder_archiv + text_file
                                        print(execute_unix(cmd0), "Bewege Datei " + text_file + " nach Archiv...")
                                        words = string.split()
                                        if (len(words) < 10000) and (len(words) > 1000): 
                                                end_list = create_chunked_textlist(string, 10)
                                        elif len(words) <= 1000:
                                                end_list = create_chunked_textlist(string, 1)
                                        elif len(words) > 10000:
                                                end_list = create_chunked_textlist(string, 100) 
                                        dirFiles = []
                                        wav_files = []
                                        x = -1
                                        for string in end_list:
                                                x = x + 1
                                                wav_files = wav_file[:-4] + "_" + str(x) + ".wav"
                                                wav_path = tmp_folder + wav_files
                                                cmd1 = "pico2wave -l=de-DE -w=%s" % wav_path + " '%s'" % string
                                                print(execute_unix(cmd1), "Erstelle Sprachsynthese in "  + wav_files + "...")
                                                dirFiles.append(wav_files)
                                        dirFiles.sort(key=lambda f: int(re.sub('\D', '', f)))
                                        fnames = ""
                                        if int(len(dirFiles)) > 1:
                                                for fn in dirFiles:
                                                        fnames = fnames + " " + tmp_folder + fn
                                                cmd2 = "sox " + fnames + " " + tmp_folder + wav_file
                                                print(execute_unix(cmd2), "Vereine chunks von "  + wav_file + "...")
                                                cmd3 = "rm -f " + fnames
                                                print(execute_unix(cmd3), "Lösche chunks von " + wav_file + "...")
                                        else:
                                                cmd4 = "mv %s" % tmp_folder + wav_file + " %s" % tmp_folder + wav_file[:-5] + ".wav"
                                                execute_unix(cmd4)
                                                cmd5 = "mv %s" % tmp_folder + mp3_file + " %s" % tmp_folder + wav_file[:-5] + ".mp3"
                                                execute_unix(cmd5)
                                        cmd6 = "lame --preset extreme %s" % tmp_folder + wav_file
                                        print(execute_unix(cmd6), "Konvertiere " + wav_file + " in MP3-Format...")
                                        cmd7 = "rm %s" % tmp_folder + wav_file
                                        print(execute_unix(cmd7), "Lösche Hilfsdateien von " + wav_file + "...: ")
                                        cmd8 = "mv %s" % tmp_folder + mp3_file + " %s" % folder_out + mp3_file
                                        print(execute_unix(cmd8), "Finalisiere " + mp3_file + "...")
                        else:
                                print("Keine Datei zum Umwandeln in Sprache vorhanden.")
                except:
                        pass
                sleep(20.0)
