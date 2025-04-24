import csv
import re

def convert_markdown_link_to_html(text):
    """
    Markdown形式のリンク [URL](label) を HTML の<a href="URL">label</a>に変換する。
    """
    pattern = r'\[(.*?)\]\((.*?)\)'
    # 正規表現の各マッチで、グループ1を href、グループ2を表示テキストとしてHTMLタグを生成
    return re.sub(pattern, lambda m: f'<a href="{m.group(1)}">{m.group(2)}</a>', text)


def generate_html(csv_file, html_file):
    items_poster = []
    items_review_talk = []
    items_nonreview_talk = []
    # CSV はヘッダー行がある想定（列名が以下の順番で設定されている）
    # 発表者, タイトル, 会議名, 会議リンク, 会議期間, 開催地, 発表日, 備考, 査読, 招待, 英語, ポスター
    with open(csv_file, newline='', encoding='utf-8') as csv_f:
        reader = csv.DictReader(csv_f)
        for row in reader:
            presenter = row["発表者"].strip()
            title     = row["タイトル"].strip()
            conf      = row["会議名"].strip()
            conf_link = row["会議リンク"].strip()
            period    = row["会議期間"].strip()
            venue     = row["開催地"].strip()
            date      = row["発表日"].strip()
            # 補足事項
            other     = row["備考"].strip()
            other = convert_markdown_link_to_html(other)# Markdownリンクが含まれていたら変換する
            special   = row["特筆事項"].strip()
            special = convert_markdown_link_to_html(special)
            # フラグはそれぞれ "1" なら有効
            review_flag  = row["査読"].strip()
            invited_flag = row["招待"].strip()
            english_flag = row["英語"].strip()
            poster_flag  = row["ポスター"].strip()
            
            invited_prefix = "(Invited) " if invited_flag == "1" else ""
            english_suffix = " (English)" if english_flag == "1" else ""
            
            # 会議名に括弧が含まれていれば、リンクテキストと括弧内の補足情報を分割
            if "（" in conf:
                anchor_text, rest = conf.split("（", 1)
                anchor_text = anchor_text.strip()
                # rest は全角左括弧「（」を先頭に追加し、右側に全角右括弧「）」がある場合はそのまま残す（不要なら消してもよい）
                rest = "（" + rest.strip()
                # period の値がある場合は、後ろに括弧付き period を付与する
                if period:
                    conf_html = f'<a href="{conf_link}" target="_blank">{anchor_text}</a>{rest}({period})'
                else:
                    conf_html = f'<a href="{conf_link}" target="_blank">{anchor_text}</a>{rest}'
            else:
                # もし全角括弧がなければ、単純にリンクと period を出力
                if period:
                    conf_html = f'<a href="{conf_link}" target="_blank">{conf}</a> ({period})'
                else:
                    conf_html = f'<a href="{conf_link}" target="_blank">{conf}</a>'

            if poster_flag:
                li_item_poster = (
                    f'        <li>\n'
                    f'          {invited_prefix}{presenter}, \n'
                    f'          "{title}", \n'
                    f'          {conf_html}, \n'
                    f'          {venue}, {date}.{english_suffix} \n'
                    f'          {other} <b>{special}</b>\n'
                    f'        </li>'
                )
                items_poster.append(li_item_poster)
            elif review_flag:
                li_item_review_talk = (
                    f'        <li>\n'
                    f'          {invited_prefix}{presenter}, \n'
                    f'          "{title}", \n'
                    f'          {conf_html}, \n'
                    f'          {venue}, {date}.{english_suffix} \n'
                    f'          {other} <b>{special}</b>\n'
                    f'        </li>'
                )
                items_review_talk.append(li_item_review_talk)
            else:           
                li_item_nonreview_talk = (
                    f'        <li>\n'
                    f'          {invited_prefix}{presenter}, \n'
                    f'          "{title}", \n'
                    f'          {conf_html}, \n'
                    f'          {venue}, {date}.{english_suffix}\n'
                    f'          {other} <b>{special}</b>\n'
                    f'        </li>'
                )
                items_nonreview_talk.append(li_item_nonreview_talk)

    num_review = len(items_review_talk)
    num_nonreview = len(items_nonreview_talk)
    num_poster = len(items_poster)

    # HTML全体の構造（ヘッダー、ヒーローセクション、コンテンツ、フッター）
    #chr(10).join は 改行文字(chr(10))を入れて結合している。
    html_template = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Keiichiro KAGAWA - TALKS</title>
  <link rel="stylesheet" href="./css/styles.css" />
</head>
<body>
  <!-- 共通ヘッダー -->
  <header>
    <div class="container header-container">
      <h1><a href="index.html" class="logo-link">Keiichiro Kagawa</a></h1>
      <nav>
        <ul>
          <li><a href="index.html">HOME</a></li>
          <li><a href="myself.html">MYSELF</a></li>
          <li><a href="papers.html">PAPERS</a></li>
          <li><a href="talks.html" class="active">TALKS</a></li>
          <li><a href="links.html">LINKS</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <!-- ヒーローセクション -->
  <section id="talks-hero" class="hero">
    <h2>TALKS</h2>
  </section>

  <!-- コンテンツエリア -->
  <main class="container">
    <section id="talks-content">
      <h2>口頭発表（査読あり）</h2>
      <ol reversed start="{num_poster + num_nonreview + num_review}">
{chr(10).join(items_review_talk)}
      </ol>

      <h2>口頭発表（査読なし）</h2>
      <ol reversed start="{num_poster + num_nonreview}">
{chr(10).join(items_nonreview_talk)}
      </ol>

      <h2>ポスター発表（査読なし）</h2>
      <ol reversed>
{chr(10).join(items_poster)}
      </ol>
    </section>
  </main>

  <footer>
    <div class="container footer-container">
      <p>&copy; Keiichiro KAGAWA, 2025</p>
    </div>
  </footer>
</body>
</html>
'''
    with open(html_file, 'w', encoding='utf-8') as out_f:
        out_f.write(html_template)

if __name__ == "__main__":
    # CSV は data/talks.csv、出力 HTML はリポジトリ直下の talks.html に出力
    generate_html("data/talks.csv", "talks.html")
