import os
import tensorflow as tf
import librosa
import numpy as np
import shutil

class Folder:
    def makeFolders(CurrentPath):
        if not(os.path.isdir(CurrentPath+"/Happy")):
            os.makedirs(os.path.join(CurrentPath+"/Happy"))
        if not(os.path.isdir(CurrentPath+"/Angry")):
            os.makedirs(os.path.join(CurrentPath+"/Angry"))
        if not(os.path.isdir(CurrentPath+"/Sad")):
            os.makedirs(os.path.join(CurrentPath+"/Sad"))
        if not(os.path.isdir(CurrentPath+"/Calm")):
            os.makedirs(os.path.join(CurrentPath+"/Calm"))

class ML:
    def MoodClassify(CurrentPath, mp3_files,progressBar):
        model_path = r"C:\Users\anesc\PycharmProjects\Music_Mood_Classifier\model\mfcc"
        num=0
        logits = None
        mp3_num = len(mp3_files)
        for item in mp3_files:
            num = num + 1
            file = CurrentPath + "/" + item
            y, sr = librosa.load(file, duration=30)
            S = librosa.feature.melspectrogram(y=y, sr=12000, S=None, n_fft=512, hop_length=256, n_mels=96, fmax=8000)
            MF = librosa.feature.mfcc(S=librosa.power_to_db(S))
            row = MF.shape[0]
            col = MF.shape[1]
            MFCC_data = MF.flatten()
            MFCC_data = MFCC_data[np.newaxis, :]
            if num == 1 :
                X = tf.placeholder(tf.float32, [None, row * col])
                X_img = tf.reshape(X, [-1, row, col, 1])
                W1 = tf.Variable(tf.random_normal([3, 3, 1, 32], stddev=0.01))
                L1 = tf.nn.conv2d(X_img, W1, strides=[1, 1, 2, 1], padding='SAME')
                L1 = tf.nn.relu(L1)
                L1 = tf.nn.max_pool(L1, ksize=[1, 3, 3, 1],
                                    strides=[1, 2, 3, 1], padding='SAME')

                W2 = tf.Variable(tf.random_normal([3, 3, 32, 64], stddev=0.01))
                L2 = tf.nn.conv2d(L1, W2, strides=[1, 1, 2, 1], padding='SAME')
                L2 = tf.nn.relu(L2)
                L2 = tf.nn.max_pool(L2, ksize=[1, 3, 3, 1],
                                    strides=[1, 2, 3, 1], padding='SAME')
                W3 = tf.Variable(tf.random_normal([3, 3, 64, 128], stddev=0.01))
                L3 = tf.nn.conv2d(L2, W3, strides=[1, 1, 2, 1], padding='SAME')
                L3 = tf.nn.relu(L3)
                L3 = tf.nn.max_pool(L3, ksize=[1, 3, 3, 1],
                                    strides=[1, 2, 3, 1], padding='SAME')
                L3_flat = tf.reshape(L3, [-1, 3 * 12 * 128])
                W4 = tf.get_variable("W4", shape=[3 * 12 * 128, 4],
                                     initializer=tf.contrib.layers.xavier_initializer())
                b = tf.Variable(tf.random_normal([4]))
                logits = tf.matmul(L3_flat, W4) + b

            with tf.Session() as sess:
                # Load the weights and bias
                saver = tf.train.Saver()
                saver.restore(sess, model_path + "\\" + "model.ckpt")
                result = sess.run(tf.argmax(logits, axis=1), feed_dict={X: MFCC_data[0:1]})
                if(result==0):
                    shutil.copy(file,CurrentPath+"/Happy")
                elif(result==1):
                    shutil.copy(file,CurrentPath+"/Angry")
                elif (result == 2):
                    shutil.copy(file, CurrentPath + "/Sad")
                elif (result == 3):
                    shutil.copy(file, CurrentPath + "/Calm")
            progressBar.setProperty("value",(int)((num/mp3_num)*100))