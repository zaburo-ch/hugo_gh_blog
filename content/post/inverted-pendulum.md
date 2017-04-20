+++
date = "2016-03-15T21:00:44+09:00"
title = "Pythonで 倒立振子のシミュレータ を実装する"
tags = ["Python", "NumPy"]
+++
[Neural Fitted Q Iteration](http://ml.informatik.uni-freiburg.de/_media/publications/rieecml05.pdf)の実験で使う倒立振子のシミュレータを書きました。  
論文ではCLSquareというシステムを使って実験が行われているのですが、  
頑張ってインストールしたものの上手く動かせなかったので自分で書きました。  

倒立振子の運動方程式については[こちら](http://www.robot.mach.mie-u.ac.jp/~nkato/class/sc/Invpend_eq3.pdf)のスライドが詳しいです。  
今回は摩擦を無視するのでスライドでいう B と C が 0 になります。  

台車の重さやポールの長さなどの各種定数は、NFQの論文に倣い、  
[これ](https://scholar.google.com/citations?view_op=view_citation&hl=ja&user=VqHiIg8AAAAJ&citation_for_view=VqHiIg8AAAAJ:u5HHmVD_uO8C)のInverted Pendulumの実験と同じにしました。  

コードはこんな感じ。
<script src="https://gist.github.com/zaburo-ch/ebeb65b7b1e97f2ece80.js"></script>

アクションは[-50N, 50N, 0N]の3種類で、[0, 1, 2]で表現しました。  
do_action(a)でアクションが実行され t だけ時間が進みます。  

matplotlibでビジュアライズできるようにしたので、  
実行すると次のようなアニメーションが表示されます。  
![inverted pendulum](/images/pendulum01.gif)

加速度がこの式で与えられるのは微分してみたらわかるけど、  
速度や位置(角速度や角度)をどうやって更新していいのかわからなかったので、  
tが小さければ高校物理のvt+1/2*at^2で大丈夫でしょって感じで  
t_sum回ループ回して細かく更新することでそれっぽい結果を得ました。  

ちゃんと検索してみると[C言語での実装](https://searchcode.com/codesearch/view/34802371/)が見つかったので、  
これを真似してupdate_stateを書き換えてみるとこんな感じ。
<script src="https://gist.github.com/zaburo-ch/70f16749efeef5beb95e.js"></script>
物理が分からない自分が書いたコードより安心なので、実験ではこっちを使おうと思います。  
