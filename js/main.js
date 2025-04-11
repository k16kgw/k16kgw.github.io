fetch('data/talks.csv')
  .then(response => response.text())
  .then(csvText => {
    const data = Papa.parse(csvText, { header: true }).data;
    // data 配列を元に DOM 操作で表などを生成
  })
  .catch(error => console.error('CSV読み込みエラー:', error));
