+++
date = "2015-10-08T00:59:54+09:00"
title = "pandasで為替データを扱う【Python】"
tags = ["Python", "pandas", "Matplotlib", "FX"]
+++
データ分析を本格的にやっていきたいと考えていて、  
その足がかりとしてpandasの使い方を勉強をしています。  

今回は為替データを扱ってみたいと思います。  
[Forexite](https://www.forexite.com/)というサイトで分足データが無料でダウンロードできるので、これを使います。  
さっそく[こちら(2015年10月6日分)](https://www.forexite.com/free_forex_quotes/2015/10/061015.zip)からzipをダウンロードしてきて解凍すると  
色々な通貨のデータが一つのtxtファイルにまとまっています。  

USDJPYのデータを抽出し5分足の終値と  
ボリンジャーバンド、指数加重移動平均をプロットするところまでやります。

IPythonで試行錯誤しながらやったものをまとめたコードが以下の通りです。
<script src="https://gist.github.com/zaburo-ch/12e9ada46ee2b7a16e5f.js"></script>

こんな感じのグラフが表示されます。  
![図1](/images/pandas_study_01.png)  
\<DTYYYYMMDD\>と\<TIME\>をマージする部分の強引さが酷いですね。  
きっともっとスマートにできるんだろうなぁ
