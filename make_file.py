"""名古屋大学の会話データセットを整形する"""

from pathlib import Path
import re
import csv

def remove_unnnecessary(text):
    # *と()<>に囲まれた文字を削除する
    return re.sub('＊|＜.*＞|（.*）','',text)

def make_utterance(file_path):
    with open(file_path) as f:
        lines = f.readlines()
        utterances = []
        temp_utt = ""
        for i in range(len(lines)-1):
            # 会話の行じゃなければスキップ
            if lines[i][0]=='＠' or lines[i][0]=='％':
                continue
            if lines[i][0] in ["M", "F", "Ｘ"] and "：" in lines[i]:
                utterances.append(temp_utt)
                temp_utt = remove_unnnecessary(lines[i].split('：',1)[1].strip())
            else:
                temp_utt += remove_unnnecessary(lines[i].strip())        
    return utterances[1:] # リストの最初は空なので取り除く

def make_utt_pair(utterances):
    utt_dict = {}
    for i in range(len(utterances)-1):
        utt_dict[utterances[i]] = utterances[i+1]
    utt_pairs = []
    for k, v in utt_dict.items():
        utt_pairs.append([k,v])
    return utt_pairs

def main():
    # テキストファイルのパスのリストを取得
    text_files = Path('nucc').glob('**/*.txt') 
    data = []
    for f in text_files:
        utterances = make_utterance(f)
        utt_pairs = make_utt_pair(utterances)
        data.extend(utt_pairs)
    
    # tsvに書き込み
    with open('data/nucc_dataset.tsv', 'w') as f:
        writer = csv.writer(f,delimiter='\t')
        writer.writerows(data)
        


if __name__ == "__main__":
    main()