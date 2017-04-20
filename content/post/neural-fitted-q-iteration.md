+++
date = "2016-03-17T13:37:58+09:00"
title = "Pythonで Neural Fitted Q Iteration を実装する"
tags = ["Python", "NumPy", "機械学習"]
+++
[前々回に実装した多層パーセプトロン](https://zaburo-ch.github.io/post/mlp/)と[前回実装した倒立振子のシミュレータ](https://zaburo-ch.github.io/post/inverted-pendulum/)を用いて、  
[Neural Fitted Q Iteration](http://ml.informatik.uni-freiburg.de/_media/publications/rieecml05.pdf)(NFQ)の実験を行います。  

NFQはQ学習の最適行動価値関数を多層パーセプトロンを用いて近似する手法の一つで、  
学習中にはデータを追加せず、事前に集められたデータのみから学習を行います。  

コードはこんな感じ。MLPはkerasで構築しました。  
<script src="https://gist.github.com/zaburo-ch/f2f61a94ee722447d2d7.js"></script>

mはepisodeの個数にあたる変数になっていて、  
[50, 100, 150, 200, 300, 400]の各m対して、50回実験を行うようになっています。  
実験の大まかな流れは、  

1. make_episodes(m)でm個のepisodeを作る  
2. 多層パーセプトロンを構築  
3. Neural Fitted Q Iterationを実行  
4. 倒立振子を立たせるタスクを実行  
5. 停止するまでの時間を記録(t<299なら失敗、t==299なら成功)  

という感じです。肝心の3.では、  
episodesの中からpattern_set_size個ずつepisodesを取り出し、  
その中の各cycleから入力xと教師信号tを作成して、  
多層パーセプトロンをこれにfitさせるのを繰り返すことで学習を行っています。  
episodes1周だけではうまくタスクを成功させることができなかったので、  
毎回取り出す順番をランダムに変えてepisodesを5周させるようにしています。  

実験結果は次のようになりました。

| m   | 成功した回数    |
|-----|---------------|
| 50  | 25 / 50 (50%) |
| 100 | 41 / 50 (82%) |
| 150 | 43 / 50 (86%) |
| 200 | 43 / 50 (86%) |
| 300 | 48 / 50 (96%) |
| 400 | 46 / 50 (92%) |

m = 50 の場合については論文とほぼ同程度成功できています。  
しかし、それ以外の場合では論文の結果よりもやや悪い数字が出てしまっています。  
特に m >= 200 では100%となるらしいのですが、100%は出ませんでした。  

 - Rpropを使うところをSGDでやったこと(sigmoid関数がフラットになる範囲で学習が停滞する)  
 - episodesの周回数(5)やpattern_set_size(=m/10)をテキトーに決めたこと  
 - fitの時のepoch数が1000で固定されていること  

あたりかなが原因なのかなと思っています。  
この辺りをちゃんと設定すれば100%も出せると思うのですが、  
まあそれほど悪くない結果が出ているのでひとまずこれで良いことにします。  

倒立振子のアニメーションは以下のような感じ。  
コスト関数が単純(倒れたら1、倒れないなら0)なため、  
直立した状態でキープしようとするのではなく、  
倒れそうになってから直そうとするので台車ごとすっ飛んで行きます。  

![m=50,失敗](/images/pendulum_m50_fail.gif)
m = 50, 失敗

![m=50,成功](/images/pendulum_m50_success.gif)
m = 50, 成功(gifは10秒で打ち切り)

![m=400,失敗](/images/pendulum_m400_fail.gif)
m = 400, 失敗

![m=400,成功](/images/pendulum_m400_success.gif)
m = 400, 成功(gifは10秒で打ち切り)