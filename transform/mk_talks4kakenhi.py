import csv
import os

def replace_unencodable(text):
    # \xd4 が発生する文字列を想定して、適切な置換を行います。
    # ここでは例として "\xd4" をハイフン "-" に置換していますが、
    # 必要に応じて適切な置換文字に変更してください。
    text = text.replace('\xd4', '-')
    # 前回の例でのen dashも置換
    text = text.replace('\u2013', '-')
    return text

def convert_csv(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8', newline='') as fin, \
         open(output_file, mode='w', encoding='shift_jis', newline='') as fout:
        
        reader = csv.DictReader(fin)
        # 出力するB.csvのヘッダー（カラム名）
        # fieldnames = ["発表者名", "発表標題", "学会等名", "発表年（始）", "発表年（終）", "招待講演", "国際学会"]
        # writer = csv.DictWriter(fout, fieldnames=fieldnames)
        # writer.writeheader()
        writer = csv.writer(fout)
        
        for row in reader:
            # 発表者名：カンマ区切りからセミコロン区切りに変換
            presenter = replace_unencodable(row["発表者"].strip().replace('"', ''))
            presenter = ';'.join([name.strip() for name in presenter.split(',')])
            
            # 発表標題
            title = replace_unencodable(row["タイトル"].strip())
            
            # 学会等名
            conference = replace_unencodable(row["会議名"].strip())

            # 発表年は「発表日」列の日付（例："2025/01/09"）から年を抽出
            pub_date = row["発表日"].strip()
            if pub_date:
                # 日付の最初の部分(年)を抽出
                pub_year = pub_date.split('/')[0]
            else:
                pub_year = ""
            
            # 招待講演：値が存在する場合は1、なければ0（サンプルは空 → 0）
            invite = row["招待"].strip()
            invite_flag = "1" if invite else "0"
            
            # 国際学会：英語列の値が存在する場合は1、なければ0（サンプルは空 → 0）
            international = row["英語"].strip()
            international_flag = "1" if international else "0"
            
            # 出力用の行を作成
            # out_row = {
            #     "発表者名": presenter,
            #     "発表標題": title,
            #     "学会等名": conference,
            #     "発表年（始）": pub_year,
            #     "発表年（終）": pub_year,
            #     "招待講演": invite_flag,
            #     "国際学会": international_flag
            # }
            # B.csv の列の順番に合わせたリストを作成
            out_row = [presenter, title, conference, pub_year, pub_year, invite_flag, international_flag]
            writer.writerow(out_row)

if __name__ == "__main__":
    # 入力・出力ファイルのパス
    input_csv = "data/talks.csv"
    output_csv = "data/talks4kakenhi.csv"
    
    if not os.path.exists(input_csv):
        print(f"入力ファイル '{input_csv}' が見つかりません。")
    else:
        convert_csv(input_csv, output_csv)
        print(f"変換が完了しました。'{output_csv}' をご確認ください。")
