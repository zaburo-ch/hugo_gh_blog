+++
date = "2016-02-14T14:28:18+09:00"
title = "Pythonで Q学習 を実装する"
tags = ["Python", "NumPy", "機械学習"]
+++
Deep Q-Networkについて調べてみたら面白い記事を見つけました。  
[DQNの生い立ち　＋　Deep Q-NetworkをChainerで書いた  
http://qiita.com/Ugo-Nama/items/08c6a5f6a571335972d5](http://qiita.com/Ugo-Nama/items/08c6a5f6a571335972d5)  

この記事を読んで、Deep Q-Networkが  
Q学習 -> Q-Network -> Deep Q-Network という流れ生まれたものだということがわかりました。  
この流れをPythonで実装しながら辿ってみようと思います。  

今回はQ学習を実装します。  
Q学習について下記のページに詳しく載っているので割愛します。  
[強化学習  
http://www.sist.ac.jp/~kanakubo/research/reinforcement_learning.html](http://www.sist.ac.jp/~kanakubo/research/reinforcement_learning.html)  
[強化学習とは？  
http://sysplan.nams.kyushu-u.ac.jp/gen/edu/RL_intro.html](http://sysplan.nams.kyushu-u.ac.jp/gen/edu/RL_intro.html)  

まず、Q学習で適応する環境として次のような簡単な環境を考えます。  
```
環境の状態は、'A'または'B'からなる長さ8の文字列で表され、  
その文字列にはある法則により得点がつけられる。  
プレイヤーはその法則についての知識を予め持たないが、  
文字列中の任意の1文字を選んで'A'または'B'に置き換えることができ、  
その結果、その操作による得点の変化量を報酬として受け取る。  
```
たぶんマルコフ決定過程になっていると思います。マルコフ性、[エルゴート性](http://ibisforest.org/index.php?%E3%82%A8%E3%83%AB%E3%82%B4%E3%83%BC%E3%83%89%E6%80%A7)も持つはず。  

文字列に得点をつける法則はなんでも良いのですが、  
今回は、特定の文字列(単語)に次のように得点を割り当てて、  
{"A": 1, "BB": 1, "AB": 2, "ABB": 3, "BBA": 3, "BBBB": 4}  
文字列中に含まれる単語の合計得点を文字列の得点とするということにします。  
例えば"AAAAAAAA"なら8点(1 * 8)、"AAAAAAAB"なら9点(1 * 7 + 2)です。  

環境のとりうる状態は長さ8のそれぞれに'A', 'B'の2通りあるので2^8通りあり、  
アクションは、何もしないのと、位置1~8のそれぞれを'A'または'B'なのでを計17通りあります。  
今回のコードでは状態は文字列、アクションは整数(0~16)で管理します。  

<script src="https://gist.github.com/zaburo-ch/9ee5fd731d40d47c82ad.js"></script>

先述した強化学習の記事では、Q学習の学習中に、  
一定の回数遷移を繰り返した後、状態をs0に戻すものとそうでないものがあり、  
どちらを採用するか悩んだので QLearning(n_rounds, t_max)として  
2重のループにすることで一応どちらの方法でも実行できるようにしました。  

これを実行結果はこんな感じ  
![/images/q_learning_figure_1.png](/images/q_learning_figure_1.png)
軸のラベルを書き忘れていますが、  
横軸が外側のループが回った数で、縦軸がそれまでに学習したQを使ってt_max回遷移した時のスコアですね。  
"ABBBBBBB"に遷移して終わるのとき最大値28をとるのですが、  
約900セット(t_max * 900回)の学習でそれを実現する遷移ができるようになっています。  

この問題だとイマイチQ学習のイメージがつかみにくいので、  
素直に最短路問題とかにしとけば良かったなーと思っています。  

最短路問題を使ったわかりやすい例はこちら  
[Q学習による最短経路学習 - poor_codeの日記  
http://d.hatena.ne.jp/poor_code/20090628/1246176165](http://d.hatena.ne.jp/poor_code/20090628/1246176165)