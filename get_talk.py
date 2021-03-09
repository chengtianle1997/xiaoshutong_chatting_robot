import robot_recorder
import robot_speaker
import get_answer
import txt_to_voice
import voice_to_txt
import time
import config
import random
import _thread

class GetTalk:
    def __init__(self, init_enable=False, debugger=False):
        self.recorder = robot_recorder.robot_recorder()
        self.speaker = robot_speaker.robot_speaker()
        self.txt_to_voice = txt_to_voice.txt_to_voice()
        self.voice_to_txt = voice_to_txt.voice_to_txt()
        self.get_answer = get_answer.TuringRobot()
        # 录音状态指示
        self.recording = False
        # 初始化使能
        self.init_enable = init_enable
        # 调试功能使能
        self.debugger = debugger
        # 语音资源文件根目录
        self.audiodir = "resources/"
        # 检查文件配置
        if init_enable:
            self.InitAutoReply()
        # 状态表
        self.status = ["recording", "solving", "finished"]
    
    # 主功能函数：开始聊天
    def Talk(self):
        _thread.start_new_thread(self.Talk_t)

    def Talk_t(self):
        # 开始录音
        self.set_status(self.status[0])
        self.recording = True
        self.recorder.record()
        self.recording = False
        self.set_status(self.status[1])
        # 语音转文字
        code, txt, error_msg = self.voice_to_txt.convert()
        self.set_question_txt(txt)
        # 错误处理
        if not code == 0:
            if code == 888:
                self.networkerr_sound()
            elif code == 999:
                self.internalerr_sound()
            else:
                self.internalerr_sound()
            if self.debugger:
                print("voice to txt error: code-{}, errmsg-{}".format(code, error_msg))
            return
        # 问题转回答
        code, answer = self.get_answer.get_answer(txt)
        self.set_answer_txt(answer)
        # 错误处理
        if not code == 0:
            if code == 999:
                self.networkerr_sound()
            else:
                self.internalerr_sound()
            if self.debugger:
                print("get answer error: code-{}".format(code))
            return
        # 文字转语音
        code, error_msg = self.txt_to_voice.convert(answer)
        # 错误处理
        if not code == 0:
            if code == 888:
                self.networkerr_sound()
            elif code == 999:
                self.internalerr_sound()
            else:
                self.internalerr_sound()
            if self.debugger:
                print("txt to voice eror: code-{}, errmsg-{}".format(code, error_msg))
            return
        # 播放语音
        self.speaker.play("answer.mp3")
        self.set_status(self.status[2])
    
    # 主功能函数：手动停止录音（若录音过程未结束）
    def Stop(self):
        if self.recording:
            self.recorder.stop()
        return

    # 检查并加载预设定语音
    def InitAutoReply(self):
        # 加载欢迎音
        welcome_file = self.audiodir + "welcome.mp3"
        welcome_txt = config.get_config("autoreply", "welcome")
        self.txt_to_voice.convert(welcome_txt, welcome_file)
        # 加载命令提示音
        instr_file = self.audiodir + "instruction.mp3"
        instr_txt = config.get_config("autoreply", "instruction")
        self.txt_to_voice.convert(instr_txt, instr_file)
        # 加载网络错误语音1, 2, 3
        neterr_file_root = self.audiodir + "networkerr"
        for i in range(1, 4):
            neterr_file = neterr_file_root + str(i) + ".mp3"      
            neterr_txt = config.get_config("autoreply", "networkerror" + str(i))
            # 生成预置语音文件
            self.txt_to_voice.convert(neterr_txt, neterr_file)
        # 加载内部错误语音1, 2, 3
        interr_file_root = self.audiodir + "internalerr"
        for i in range(1, 4):
            interr_file = interr_file_root + str(i) + ".mp3"
            interr_txt = config.get_config("autoreply", "internalerror" + str(i))
            # 生成预置语音文件
            self.txt_to_voice.convert(interr_txt, interr_file)

    # 播放欢迎音
    def welcome_sound(self):
        file_url = self.audiodir + "welcome.mp3"
        _thread.start_new_thread(self.speaker.play, (file_url,))

    # 播放命令提示音
    def instruct_sound(self):
        file_url = self.audiodir + "instruction.mp3"
        _thread.start_new_thread(self.speaker.play, (file_url,))

    # 播放网络错误提示音
    def networkerr_sound(self):
        n = random.randint(1, 3)
        file_url = self.audiodir + "networkerr" + str(n) + ".mp3"
        _thread.start_new_thread(self.speaker.play, (file_url,))
    
    # 播放内部错误提示音
    def internalerr_sound(self):
        n = random.randint(1, 3)
        file_url = self.audiodir + "internalerr" + str(n) + ".mp3"
        _thread.start_new_thread(self.speaker.play, (file_url,))

    # 设定问题文字
    def set_question_txt(self, question_txt):
        if self.debugger:
            print(question_txt)

    # 设定回答文字
    def set_answer_txt(self, answer_txt):
        if self.debugger:
            print(answer_txt)

    # 设定当前状态
    def set_status(self, status):
        if self.debugger:
            print("status:{}".format(status))

# Test Demo
if __name__ == '__main__':
    # 获取实例
    getTalk = GetTalk(init_enable=False, debugger=True)
    # 开始聊天
    getTalk.Talk()
    # 保持程序运行（主线程关闭，子线程随之关闭）
    time.sleep(15)
    print("测试结束")