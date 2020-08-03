import textract, subprocess, os, fnmatch
from time import sleep

def execute_unix(inputcommand):
   p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
   (output, err) = p.communicate()
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

if __name__ == '__main__':
	folder_in_deu = "/home/user/Documents/TTS-INPUT_deu/"
	folder_in_eng = "/home/user/Documents/TTS-INPUT_eng/"
	folder_tmp = "/home/user/Documents/tmp/"
	folder_out = "/home/user/Documents/TTS-OUTPUT/"
	folder_archiv = "/home/user/Documents/TTS-ARCHIV/"

	while True:
		try:
			text_file_list_deu = matchedfiles(folder_in_deu, [".csv",".doc",".docx",".eml",".epub",".gif",".jpg",".json",".html",".mp3",".msg",".odt",".ogg",".pdf",".png",".pptx",".ps",".rtf",".tiff",".txt"".wav",".xlsx",".xls"])
			text_file_list_eng = matchedfiles(folder_in_eng, [".csv",".doc",".docx",".eml",".epub",".gif",".jpg",".json",".html",".mp3",".msg",".odt",".ogg",".pdf",".png",".pptx",".ps",".rtf",".tiff",".txt"".wav",".xlsx",".xls"])
			
			for file in text_file_list_deu:
				string = textract.process(folder_in_deu+file).decode('utf-8', errors="replace")
				wav_file = file[:-4] + ".wav"
				wav_path = folder_out + wav_file
				cmd1 = "pico2wave -l=de-DE -w=%s" % wav_path + " '%s'" % string
				p1 = subprocess.Popen(cmd1, shell=True)
				p1.wait()
				
				cmd2 = 'lame --preset extreme %s' % wav_path
				p2 = subprocess.Popen(cmd2, shell=True)
				p2.wait()
				cmd3 = "rm %s" % wav_path
				p3 = subprocess.Popen(cmd3, shell=True)
				p3.wait()
				cmd4 = "mv %s" % folder_in_deu + file + " %s" % folder_archiv + file
				p4 = subprocess.Popen(cmd4, shell=True)
				p4.wait()

			for file2 in text_file_list_eng:
				string = textract.process(folder_in_eng+file2).decode('utf-8', errors="replace")
				wav_file2 = file2[:-4] + ".wav"
				wav_path2 = folder_out + wav_file2
				cmd1 = "pico2wave -l=en-EN -w=%s" % wav_path2 + " '%s'" % string
				p1 = subprocess.Popen(cmd1, shell=True)
				p1.wait()
				
				cmd2 = 'lame --preset extreme %s' % wav_path2
				p2 = subprocess.Popen(cmd2, shell=True)
				p2.wait()
				cmd3 = "rm %s" % wav_path2
				p3 = subprocess.Popen(cmd3, shell=True)
				p3.wait()
				cmd4 = "mv %s" % folder_in_eng + file2 + " %s" % folder_archiv + file2
				p4 = subprocess.Popen(cmd4, shell=True)
				p4.wait()
		except:
			pass
		sleep(30.0)
