import csv

def generate_html(csv_file, html_file):
    talks_items = []
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
            # 招待フラグ、英語フラグはそれぞれ "1" なら有効
            invited_flag = row["招待"].strip()
            english_flag = row["英語"].strip()
            
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

            li_item = (
                f'        <li>\n'
                f'          {invited_prefix}{presenter}, \n'
                f'          "{title}", \n'
                f'          {conf_html}, \n'
                f'          {venue}, {date}.{english_suffix}\n'
                f'        </li>'
            )
            talks_items.append(li_item)
    
    # HTML全体の構造（ヘッダー、ヒーローセクション、コンテンツ、フッター）
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
      <h2>講演情報</h2>
      <ol reversed>
{chr(10).join(talks_items)}
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
