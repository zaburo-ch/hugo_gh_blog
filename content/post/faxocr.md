+++
date = "2016-04-13T11:32:33+09:00"
title = "FaxOCR を CNN でやってみた"
tags = ["Python", "機械学習"]
+++
せっかくKerasを使ってみたのでCNNもやってみたいということで、  
[FaxOCR](https://sites.google.com/site/faxocr2010/systemrequirements/kocr/mnist)というMNISTと同形式のデータセットで手書き文字認識をやってみました。  
ソースコードは[ここ](https://github.com/zaburo-ch/FaxOCR/blob/master/code/faxmnist_keras.py)にあります。  

このデータセットではtrain setがかなり小さいので、  
まず最初に適当に拡大縮小や回転をして画像データの枚数を11倍に(1枚から10枚生成)しました。  

CNNのアーキテクチャは[toshi-kさんのコード](https://github.com/toshi-k/kaggle-digit-recognizer/blob/master/2_model.lua)を参考にして適当に設定しました。  
ただ、データセットが小さくて過学習してしまいそうだなーと思ったので、  
上記のものに比べて小さいネットワークになっています。  

入力したテンソルがどの時点でどのサイズになっているか確認する方法がわからなかったので、  
ZeroPaddingなどがこれでうまくいっているのかわかりませんが、  
入力(1, 28, 28) -> (64, 12, 12) -> (64, 12, 12) -> (256, 10, 10) -> (128) -> (10)出力  
という形になっていると嬉しいなくらいの感じで書いています。  
[こういう風に](http://ultraist.hatenablog.com/entry/2014/08/23/144007)デバッグする方法が知りたい......

結果は次の通りです。  

| dataset | 正答率 |
|---------|-------|
| train   | 99.5% |
| valid   | 99.1% |
| test    | 93.1% |

増やしたデータセットのうち90%をtrain、10%をvalidとし、  
trainで訓練してvalidが最も高くなるところで止まるようになっています。  
もとのデータセット全部をtrainにしてtestが高くなるところで止めるともう少し精度が上がります。([これ](https://github.com/zaburo-ch/FaxOCR/blob/master/code/faxmnist_keras_testval.py))  

GPUマシンを持っていないので学習に時間がかかりすぎりてあんまり色々試せない......

[追記]  
データセットのバージョンは[faxocr-numbers-20160411c.zip](https://sites.google.com/site/faxocr2010/systemrequirements/kocr/mnist/faxocr-numbers-20160411c.zip)のものです。