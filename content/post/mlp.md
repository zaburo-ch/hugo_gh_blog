+++
date = "2016-02-20T01:29:30+09:00"
title = "Pythonで 多層パーセプトロン を実装する"
tags = ["Python", "NumPy", "機械学習"]
+++
前回は古典的Q学習を実装しましたが、次はニューラルネットを用いたQ学習として、  
[Neural Fitted Q Iteration](http://ml.informatik.uni-freiburg.de/_media/publications/rieecml05.pdf)を使ったQ学習を実装しようと考えています。  

今回はその前の勉強として、  
誤差逆伝播法を用いた多層パーセプトロンをNumPyだけで実装してみます。  
誤差逆伝播法についてはこちらのスライドが詳しいです。  

<iframe src="//www.slideshare.net/slideshow/embed_code/key/1T0PJeFTRBMnCG?startSlide=32" width="425" height="355" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe>  
<a href="//www.slideshare.net/weda654/3-45366686" title="わかりやすいパターン認識_3章" target="_blank">わかりやすいパターン認識_3章</a>

コードはこんな感じ。
<script src="https://gist.github.com/zaburo-ch/7ab05a6dda71b5ccfe4f.js"></script>

活性化関数は全てシグモイド関数で、コスト関数は残差の平方和を用いました。  
各層はforwardで出力を計算して、  
backwardで前の層の誤差を計算しつつ W や b の更新を行います。  
tanhなどの層も同じような関数を実装してMLPのinitを適宜変えれば使える(はず)。  

[DeepLearningTutorialsのMLPのコード](http://deeplearning.net/tutorial/mlp.html)っぽくしたくて、  
[DeepLearningTutorialsのDBNをNumPyで実装した方のコード](http://blog.yusugomori.com/post/40250499669/python%E3%81%AB%E3%82%88%E3%82%8Bdeep-learning%E3%81%AE%E5%AE%9F%E8%A3%85deep-belief-nets-%E7%B7%A8)とか、  
[NumPyでMLPを実装を実装した方のコード](http://aidiary.hatenablog.com/entry/20140201/1391218771)などを参考に書きました。  

各所に載っている式を見る限りは出力層も活性化関数を使うっぽいんですが、  
Chainerの多層パーセプトロンのサンプルをはじめとして、  
出力層で線形変換するだけ(活性化関数を使わない)のものが結構あって混乱しました。  
たぶんシグモイド関数やtanhだと出力できる範囲が狭くて不便なので  
出力層だけ恒等関数使ってるんだろうという感じでとりあえず考えています。  
先のNFQの論文で、全ての層でシグモイドを使ったみたいなことが書いてあったので、  
今回は出力層にもシグモイド関数を使うことにしています。  
あと出力層での誤差も、出力層の活性化関数の微分をかけるのかどうかがわからなくて  
結構悩みましたが、スライドの式に従ってかけることにしました。  

また、確率的勾配降下法(SGD)でミニバッチを使った学習ができるように書きましたが、  
ミニバッチを使う時に W や b の更新をどうやるのかがよくわからなくて、  
結局ループ回して学習パターン1つずつ使って更新を行うようにしました。  
出力層の時点で誤差の和をとってそれを伝播するんだと思ったのですが、  
そしたらそれと掛け合わせる前の層の出力はどうするんだ！？ってなって  
結局わからず、まあ結局やってること大体一緒でしょってことでこの形にしました。  

結果はこんな感じになります。赤が教師信号、青がMLPの出力で、  
左が1000回反復した場合、右が10000回反復した場合です。  
<img src="/images/mlp_approximate_abs_1000.png" width="300px" />
<img src="/images/mlp_approximate_abs_10000.png" width="300px" />

たぶん学習できていると思うのですが、  
いまいちうまくいっているのか確証が持てなかったので、  
同じネットワークをChainerでも実装してみました。  

コードは[ここ](https://gist.github.com/zaburo-ch/8f4fe27e898b42a38635)。Tutorialのものをちょっといじっただけです。

結果は次の通り。  
<img src="/images/mlp_approximate_abs_chainer_1000.png" width="300px" />
<img src="/images/mlp_approximate_abs_chainer_10000.png" width="300px" />

Chainerの方が若干うまく近似できていますが、  
概ね同じような感じの結果が得られたので、自分で書いた方も大丈夫なはず。  

実行時間はNumPyだけの方がかなり早いです。  
ただ自分で微分する必要もなく適当に層つなぐだけで出来ちゃったのでChainerすごい  

**2016/03/15 追記**  
Kerasでも試してみました。コードは[ここ](https://gist.github.com/zaburo-ch/13b9bfc221246b319a19)。

結果はだいたい同じような感じ  
<img src="/images/mlp_approximate_abs_keras_1000.png" width="300px" />
<img src="/images/mlp_approximate_abs_keras_10000.png" width="300px" />

後ろでTheanoが使われていることもありかなり速いです。  
まだMLP書いただけなので、もっと大規模なモデルを実装するときにどうなるかはわかりませんが、  
モデルの記述の仕方や、sklearnっぽいfit・predictの書き方など、  
結構書きやすいように感じました。もっと使ってみたい。  
