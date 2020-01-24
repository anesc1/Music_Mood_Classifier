# Music_Mood_Classifier
This program classifies your music to one of 4 mood(Happy, Angry, Sad, Calm) based on Russell emotional model. It is made by pyqt GUI and only works with mp3 files. Mp3 files are analyzed with librosa module. Therfore don't forget to download ffmpeg to not to get errors. CNN machine learning model is used and showed 85% of accuracy when training with Emomusic dataset.

![screenshot](https://user-images.githubusercontent.com/38872957/72883897-82d29580-3d48-11ea-9ea7-e282a7953112.PNG)

# How to use
1. Click 'Select Folder' and select a folder that contains mp3 files. 
2. Mp3 fils lists will be showed on Qlistview.
3. Click 'Classify' to classify mood of mp3 files.
4. 4 new folders will be generated where selected folder directory exists and mp3 files will be copied to each belonging mood.
