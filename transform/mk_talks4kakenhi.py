import argparse
import pandas as pd

def transform_csv(input_file, output_file):
    # 入力 CSV を読み込み
    df = pd.read_csv(input_file)

    # 例: 各列名の左右の空白を除去し、小文字に変換
    df.columns = [col.strip().lower() for col in df.columns]

    # 例: 文字列データについて、各セルの余分な空白を除去
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()

    # 例: 列の順序をアルファベット順に並べ替え
    df = df[sorted(df.columns)]

    # 整形後の DataFrame を新たな CSV ファイルとして出力（index は不要）
    df.to_csv(output_file, index=False)
    print(f"整形した CSV を {output_file} に保存しました。")

import csv
import os

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
            # 発表者名：カンマ区切りからセミコロン区切りに変更
            presenter = row["発表者"].strip()
            # もしフィールド内に " が含まれている場合は除去
            presenter = presenter.replace('"', '')
            # 名前間のカンマをセミコロンに置換
            presenter = ';'.join([name.strip() for name in presenter.split(',')])
            
            # 発表標題：そのまま
            title = row["タイトル"].strip()
            
            # 学会等名：そのまま（会議名）
            conference = row["会議名"].strip()
            
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
    input_csv = "talks.csv"
    output_csv = "talks4kakenhi.csv"
    
    if not os.path.exists(input_csv):
        print(f"入力ファイル '{input_csv}' が見つかりません。")
    else:
        convert_csv(input_csv, output_csv)
        print(f"変換が完了しました。'{output_csv}' をご確認ください。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CSV を整形して別ファイルに出力します')
    parser.add_argument('input_file', help='入力 CSV ファイル（更新されたファイル）')
    parser.add_argument('output_file', help='出力 CSV ファイル')
    args = parser.parse_args()

    transform_csv(args.input_file, args.output_file)
