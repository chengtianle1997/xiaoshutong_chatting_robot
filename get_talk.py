import robot_recorder
import robot_speaker
import get_answer
import txt_to_voice
import voice_to_txt
import time

class GetTalk:
    def __init__(self):
        self.recorder = robot_recorder.robot_recorder()
        self.speaker = robot_speaker.robot_speaker()
        self.txt_to_voice = txt_to_voice.txt_to_voice()
        self.voice_to_txt = voice_to_txt.voice_to_txt()
        self.get_answer = get_answer.TuringRobot()

        # 录音状态指示
        self.recording = False
    
    # 主功能函数：开始聊天
    def Talk(self):
        # 开始录音
        self.recording = True
        self.recorder.record()
        self.recording = False
        # 语音转文字
        code, txt, error_msg = self.voice_to_txt.convert()
        # 问题转回答
        code, answer = self.get_answer.get_answer(txt)
        # 文字转语音
        code, error_msg = self.txt_to_voice.convert(answer)
        # 播放语音
        self.speaker.play("answer.mp3")
    
    # 主功能函数：手动停止录音（若录音过程未结束）
    def Stop(self):
        if self.recording:
            self.recorder.stop()
        return


# Test Demo
if __name__ == '__main__':
    getTalk = GetTalk()
    import _thread
    _thread.start_new_thread(getTalk.Talk)
    time.sleep(20)
    print("测试结束")