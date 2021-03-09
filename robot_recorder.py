import pyaudio
import numpy as np
from scipy import fftpack
import wave
import time
import _thread
from pydub import AudioSegment

class robot_recorder():
    def __init__(self, filename="question", debugger=False):
        self.threshold = 6000
        self.filename = filename  #文件存放路径
        self.CHUNK = 1024  # 块大小
        self.FORMAT = pyaudio.paInt16  # 每次采集的位数
        self.CHANNELS = 1  # 声道数
        self.RATE = 16000  # 采样率：每秒采集数据的次数
        self.stop_sign = False  # 停止指示符
        self.auto_timeout = 1  # 阈值检测时间
        self.timeout = 10  # 自动停止系统超时时间
        self.ratio = 2/3  # 检测低于阈值音值的比例
        self.debugger = debugger  # 是否输出测试内容
        self.startdetect_time = 3  # 录音开始后的延迟检测时间

        # 文件转换
        self.wav_file_name = filename + ".wav"
        self.mp3_file_name = filename + ".mp3"

    # 录音线程函数
    def record_t(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS, 
        rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        frames = []
        stopflag = 0
        stopflag2 = 0
        if self.debugger:
            print("开始录音......")
        start_time = time.time()
        while not self.stop_sign:
            data = stream.read(self.CHUNK)
            rt_data = np.frombuffer(data, np.dtype('<i2'))
            # 傅里叶变换
            fft_temp_data = fftpack.fft(rt_data, rt_data.size, overwrite_x=True)
            fft_data = np.abs(fft_temp_data)[0:fft_temp_data.size // 2 + 1]
            # 输出值以判断阈值
            if self.debugger:
                debugger_time = time.time()
                print("音值：{}， 时间：{}".format(sum(fft_data) // len(fft_data), debugger_time - start_time))
            # 判断麦克风是否停止(通过阈值)
            # stopflag 记录大于阈值的次数
            # stopflag2 记录小于阈值的次数
            if sum(fft_data) // len(fft_data) > self.threshold:
                stopflag += 1
            else:
                stopflag2 += 1
            oneSecond = int(self.RATE / self.CHUNK)
            nSecond = oneSecond * self.auto_timeout
            if stopflag2 + stopflag > nSecond:
                # 小于阈值的部分超过 2/3
                detect_time = time.time()
                if stopflag2 > nSecond * self.ratio and detect_time - start_time > self.startdetect_time:
                    break
                else:
                    stopflag2 = 0
                    stopflag = 0
            frames.append(data)
            # 检查是否超时
            pause_time = time.time()
            if pause_time - start_time > self.timeout:
                break
        if self.debugger:
            print("录音结束")
        stream.stop_stream()
        stream.close()
        p.terminate()
        try:
            wf = wave.open(self.wav_file_name, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
            # 转为mp3格式
            sound = AudioSegment.from_wav(self.wav_file_name)
            sound.export(self.mp3_file_name, format='mp3')
            return 0
        except Exception as e:
            if self.debugger:
                print(e)
            return -1
    
    # 主功能函数：开始录音 （开启自动停止）
    def record(self):
        _thread.start_new_thread(self.record_t)

    # 主功能函数： 手动停止录音
    def stop(self):
        self.stop_sign = True


# Test Demo
if __name__ == '__main__':
    recorder = robot_recorder(debugger=True)
    recorder.record()
    time.sleep(2) # 手动停止测试，该时间小于延迟检测时间
    recorder.stop()

    
    





