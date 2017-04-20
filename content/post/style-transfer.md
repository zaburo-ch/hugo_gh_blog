+++
date = "2016-12-17T17:04:54+09:00"
title = "Style Transfer いろいろ"
tags = ["Python", "TensorFlow"]
+++
研究室のゼミでStyle Transferに関して論文紹介を行った際に使用したスライドを  
少し修正してslide shareにアップロードしました．  

<iframe src="//www.slideshare.net/slideshow/embed_code/key/crr96NXhlx6ow9" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/zaburo/style-transfer" title="Style transfer" target="_blank">Style transfer</a> </strong> from <strong><a target="_blank" href="//www.slideshare.net/zaburo">zaburo</a></strong> </div>

TensorFlowの練習も兼ねて実装してみたので  
この記事では，実装するときに悩んだところなどついていくつか取り上げたいと思います．  

下記の実装を参考にさせていただきました．  
https://github.com/cysmith/neural-style-tf  
https://github.com/tensorflow/magenta/tree/master/magenta/models/image_stylization  


まずはスライド中でGatys et al. 2016aとして紹介している  
もっとも基本的なStyle Transferを実装します．コードは[こちら](https://github.com/zaburo-ch/style_transfer/blob/master/my_style_transfer.py)．  

基本的には論文の式を実装するだけですが  
コンテンツの損失の式がピクセル数で割るような形になっていないのに  
論文に入力画像のサイズが書いていないので(見逃しているだけ？)，  
論文のalphaとbetaの比をそのままつかってもうまくいきませんでした．  

そこでJohnson et al. 2016に書かれている式を使うことにしました．  
具体的にはコンテンツの損失で二乗和をとっているところを二乗平均にしました．  
ついでに，スタイルの損失についてもJohnson et al. 2016に従って修正します．  
ここはGram matrixを`height * width`で割って二乗平均をとる形にしました．  
(Gram matrixを`channel * height * width`で割るのと等価なはずです)  

VGGについてはTensorFlow-Slimを使ってサクッと書きました．  
基本は[slimの下にあるvgg_16](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/contrib/slim/python/slim/nets/vgg.py)から全結合層を除いたものになっています．  
endpointはそのままだとkeyが`vgg_16/convN/convN_M`のような形になるので，  
使いやすいようにkeyを変更して使っています．  
slimを使うと数行でVGG16が実装できるので非常に便利でした．  

また，損失の定義する方法としては，コンテンツ・スタイル画像をテンソルとして別々に定義し  
最適化の際にそれらをVGGに入力した値などを計算させるような方法も考えられますが，  
損失を定義する段階でコンテンツ・スタイル画像を入力した場合の計算しておき，  
それを定数として扱った方が高速に動作したのでそのように書きました．  


次にGatys et al. 2016bで提案された色を保存したままStyle Transferを行う手法の1つである  
Luminance-only Transferを実装します．コードは[こちら](https://github.com/zaburo-ch/style_transfer/blob/master/luminance_only.py)  
これは[英語版WikipediaのYIQの記事](https://en.wikipedia.org/wiki/YIQ)にYIQとRGBの相互変換が載っているので  
これを実装すればほとんどおしまいです．  

あとは，RGB -> YIQ -> YチャンネルはそのままでIQチャンネルを全て0にしたもの -> RGB  
という流れで変換してStyle Transferして結果のIQチャンネルを元のIQチャンネルに戻すだけです．  
また，コンテンツのYチャンネルとスタイルのYチャンネルの平均・分散が
同じになるように途中でスタイルのYチャンネルを変換するとより結果がよくなるそうです．


Johnson et al. 2016についても[magentaのimage_stylization](https://github.com/tensorflow/magenta/tree/master/magenta/models/image_stylization)を参考にして実装してみましたが，  
いまひとつ綺麗な画像が生成できていないので要改善という感じです...  
コードは[こちら](https://github.com/zaburo-ch/style_transfer/tree/master/fast_transfer)  

もしかしたらTensorFlowのバージョンによって違うのかもしれませんが，  
`tf.image.convert_image_dtype(image, dtype=tf.float32)`  
は使った段階で[0, 1)に値が丸められるので，この後で255で割る必要はないようです．    
参考にしたコードでは255で割っていたのでそれを真似していたらハマってしまいました...  

あとデバッグの際にはsummaryで値を眺めてみるというのもありですが，  
`tf.Print`で実際の値を見るのも非常に役に立ちました．↓このへんを参考に．
http://stackoverflow.com/questions/38810424/how-does-one-debug-nan-values-in-tensorflow/38813502
https://www.tensorflow.org/api_docs/python/control_flow_ops/debugging_operations#Print


とりあえず思いつくことは以上になります．  
ついこの間1ネットワークで任意のスタイルに適用できるという凄い論文  
(Chen & Schmidt 2016)が出たのでこれについても試してみたいですね．  


**参考文献**  
 - Gatys et al. 2016a [Image Style Transfer Using Convolutional Neural Networks](http://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf)  
 - Gatys et al. 2016b [Preserving Color in Neural Artistic Style Transfer](https://arxiv.org/abs/1606.05897)  
 - Johnson et al. 2016 [Perceptual Losses for Real-Time Style Transfer and Super-Resolution](https://arxiv.org/abs/1603.08155)  
 - Chen & Schmidt 2016 [Fast Patch-based Style Transfer of Arbitrary Style](https://arxiv.org/abs/1612.04337)  
