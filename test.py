# -*- coding: utf-8 -*-
"""Untitled19.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1lGUXy3f4V4dI1-cgMaIW_WVSp_LWXzxI
"""
import sys
import subprocess
import pkg_resources
subprocess.run([sys.executable,"-m", 'apt' ,'install' ,'ffmpeg'])
required  = {'pytube', 'gdown','spleeter','streamlit','pydrive'} 
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed
if missing:
    # implement pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

import spleeter
import os
from pytube import YouTube
import os
from pathlib import Path
import subprocess
import streamlit as st
import os
from os.path import basename
import time


cwd=str(os.getcwd())

subprocess.run(["git", "clone", "https://github.com/iwantthatresult/ytdlspleeter.git"])

def save(fname,Token):
  savecwd=cwd
  os.chdir(cwd +'/ytdlspleeter')
  subprocess.run(['git','remote', 'set-url', 'origin', 'https://iwantthatresult:'+Token+'@github.com/iwantthatresult/ytdlspleeter.git'])
  subprocess.run(['mv' ,savecwd+'/audio/'+fname, './data'])
  subprocess.run(['git','add', './data/'+fname])
  subprocess.run(['git','config','user.email', '"space.punk3r@gmail.com"'])
  subprocess.run(['git','config','user.name', '"iwantthatresult"'])
  subprocess.run(['git', 'commit', '-m', '"adding new song"'])
  subprocess.run(['git' ,'push',  'https://iwantthatresult:'+Token+'@github.com/iwantthatresult/ytdlspleeter.git'])
  os.chdir(savecwd)


def youtube2mp3 (url,outdir,fname,Token):
    # url input from user
    yt = YouTube(url)
    ##@ Extract audio with 160kbps quality from video
    video = yt.streams.filter(only_audio=True,abr='160kbps').last()
    ##@ Downloadthe file
    out_file = video.download(output_path=outdir,filename=fname)
    base, ext = os.path.splitext(out_file)
    new_file = Path(f'{base}.mp3')
    os.rename(out_file, new_file)
    ##@ Check success of download
    if new_file.exists():
        print(f'{yt.title} has been successfully downloaded.')
        idsave=fname
        fnamesave=fname+'.mp3'
        fname=cwd+"/audio/"+fname+'/'+fname+'.mp3'
        out=cwd+'/audio/'
        fout=cwd+"/audio/"+idsave+'/vocals.mp3'
        subprocess.run(["spleeter separate "+ fname +" -p spleeter:5stems -c mp3 -o "+ out], capture_output=True)
        audio_file = open(fout, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='mp3')
        user_input=st.text_input(fname)
        save(idsave,Token)
    else:
        print(f'ERROR: {yt.title}could not be downloaded!')
    
def audiodl(id):
  id=str.split(id)
  Token=id[0]
  print(id)
  for i in range(1,len(id)):
    url='www.youtube.com/watch?v='+id[i]
    youtube2mp3(url,cwd+'/audio/'+str(id[i])+"",str(id[i]),Token)  
user_input1 = st.text_input("insère ton lien poto", '')
while len(user_input1)==0:
  time.sleep(5)
a=audiodl(user_input1)
user_input=st.text_input(cwd)
