import numpy as np
import usingwave
from scipy.signal import fftconvolve
import os, tkinter, tkinter.filedialog, tkinter.messagebox


def gui():
    print("input filename")

    root = tkinter.Tk()
    root.withdraw()

    # 選択候補を拡張子jpgに絞る（絞らない場合は *.jpg → *）
    filetype = [("", "*.wav")]

    dirpath = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo('24chからバイノーラル', '24ch-wavファイルを選択してください')

    # 選択したファイルのパスを取得
    filepath = tkinter.filedialog.askopenfilename(filetypes=filetype, initialdir=dirpath)

    return filepath


def azi(azinum):
    if azinum - 10 < 0:
        azi = "00" + str(azinum)
    elif azinum - 100 < 0:
        azi = "0" + str(azinum)
    else:
        azi = str(azinum)
    return azi


if __name__ == '__main__':

    fs, data = usingwave.readwav(gui())
    # fs, data = usingwave.readwav("/Users/shugoto/movingpink.wav") #仮置き

    L_data = np.zeros((1, len(data) + 512 - 1))
    L_conv_data = np.zeros((24, len(data) + 512 - 1))
    for i in range(23):
        L_sound_data = (data[:, i])
        if i < 8:
            azimuth = azi(i*45)
            hrtf_file = "/Users/shugoto/Desktop/研究室関連/full/elev40/L40e{0}a.wav".format(azimuth)
        elif i < 16:
            azimuth = azi((i - 8) * 45)
            hrtf_file = "/Users/shugoto/Desktop/研究室関連/full/elev0/L0e{0}a.wav".format(azimuth)
        else:
            azimuth = azi((i - 16) * 45)
            hrtf_file = "/Users/shugoto/Desktop/研究室関連/full/elev-40/L-40e{0}a.wav".format(azimuth)
        ir_fs, ir_data = usingwave.readwav(hrtf_file)

        L_conv_data[i] = fftconvolve(L_sound_data, ir_data[:, 0])
        L_data += L_conv_data[i]

    R_data = np.zeros((1, len(data) + 512 - 1))
    R_conv_data = np.zeros((24, len(data) + 512 - 1))
    for i in range(23):
        R_sound_data = (data[:, i])
        if i < 8:
            azimuth = azi(i * 45)
            hrtf_file = "/Users/shugoto/Desktop/研究室関連/full/elev40/R40e{0}a.wav".format(azimuth)
        elif i < 16:
            azimuth = azi((i - 8) * 45)
            hrtf_file = "/Users/shugoto/Desktop/研究室関連/full/elev0/R0e{0}a.wav".format(azimuth)
        else:
            azimuth = azi((i - 16) * 45)
            hrtf_file = "/Users/shugoto/Desktop/研究室関連/full/elev-40/R-40e{0}a.wav".format(azimuth)
        ir_fs, ir_data = usingwave.readwav(hrtf_file)

        R_conv_data[i] = fftconvolve(R_sound_data, ir_data[:, 0])
        R_data += R_conv_data[i]

    mix = np.concatenate([L_data, R_data])
    mix /= np.max(np.abs(mix))

    print("enter filename :")
    filename = input()
    usingwave.writewav(filename, mix.T)









