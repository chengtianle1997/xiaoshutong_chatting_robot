import os
from pocketsphinx import LiveSpeech, get_model_path
 
model_path = get_model_path()
 
speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    # hmm=os.path.join(model_path, 'en-us'),
    # lm=os.path.join(model_path, 'en-us.lm.bin'),
    # dic=os.path.join(model_path, 'cmudict-en-us.dict')
    hmm=os.path.join(model_path, 'zh_cn.cd_cont_5000'),
    lm=os.path.join(model_path, 'zh_cn.lm.bin'),
    dic=os.path.join(model_path, 'zh_cn.dic')
)
for phrase in speech:
    print("phrase:", phrase)
    print(phrase.segments(detailed=True))