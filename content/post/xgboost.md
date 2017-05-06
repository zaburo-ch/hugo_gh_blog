+++
date = "2017-05-06T03:02:50+09:00"
title = "Gradient Boosting と XGBoost"
math = true
tags = ["機械学習", "XGBoost"]
+++

Gradient Boosting や XGBoostについて調べたことをまとめました．  
Gradient Descent や Newton法と絡めて説明していきたいと思います．  

目次
---

 - Boosting
 - Gradient Descent (Steepest Descent)
 - Gradient Boosting
 - Regression Tree
 - Gradient Tree Boosting
 - Learning rate
 - Newton Boosting
 - XGBoost
 - Generalization Error
 - Conclusion
 - Reference

Boosting
---

Boostingとは，ランダムより少し良い程度の"弱い"学習アルゴリズムを使って，  
そのアルゴリズムよりも"強い"学習アルゴリズムをつくることです．  
イメージとしては，弱い学習アルゴリズムを"boost"してあげる感じでしょうか．  

そもそもそんなことって理論的に可能なの？という問いからBoostingの歴史が始まったわけですが，  
Boostingが可能であることは，1989年にRobert E. Schapire大先生によって  
PAC Learningという枠組みで実際にBoostingを行うアルゴリズムを示す形で証明されました[1]．  

Boostingのアルゴリズムで大きな成功を収めたもののひとつが，[2]で提案された**AdaBoost**で  
以降のBoostingアルゴリズムはAdaBoostに大きな影響を受けています．  
なんとなくBoostingと言えば逐次的に学習器を構築して，その和をとる，  
というようなイメージがありますが，それもAdaBoost由来だと思います．たぶん．  

$t$ 回目の反復で"弱い"学習アルゴリズムにより構築された学習器(弱学習器)を $f\_t$とすると，  
よく使われているBoostingアルゴリズムのほとんどは次のような形で表されます．  

$$F\_T(x)=\sum\_{t=1}^{T}\alpha\_t f\_t(x)$$  

ここで $F\_T(x)$ がBoostingアルゴリズムの出力で，$\alpha\_t$ は適当に設定された係数です．

Gradient Descent (Steepest Descent)
---
Gradiet Boostingの説明をする前に  
Gradiet Boosting非常に関連の強い[Gradient descent](https://en.wikipedia.org/wiki/Gradient\_descent) (勾配降下法)に触れておきます．  
Steepest Descent (最急降下法)とも呼ばれているアレです．  

Gradient Descent は関数 $\phi:\mathbb{R}^n \rightarrow \mathbb{R}$ を最小化するような $p\in\mathbb{R}^n$ を探すアルゴリズムで，  
繰り返し $\phi$ が小さくなる方向に解を更新し，最適解に近づけていきます．  
具体的には $t-1$ 回目の反復が終わった後の解を $p\_{t-1}$ として，

$$p\_t = p\_{t-1} - \alpha\_t \nabla \phi(p\_{t-1})$$

と解の更新を行います．ここで $- \nabla \phi(p\_{t-1})$ が減少する方向を表していて，  
$\alpha\_t$ がこの更新でその方向にどれだけ動かすかを表しています．  

$\alpha\_t$ の決め方はいくつか提案されていますが，  
[Line Search](https://en.wikipedia.org/wiki/Line\_search) と呼ばれる手法では
$\phi(p\_{t-1} - \alpha \nabla f(p\_{t-1}))$ を最小化する $\alpha$ を用います．

ニューラルネットの学習などの文脈でGradient Descnetが使われる場合には，  
N個のデータ $(x\_i, y\_i)$ と損失関数$L$に対して，  
$p$ をパラメータ，$F(x; p)$ を $p$ の下での関数(学習器)の出力として，

$$\phi(p)=\sum\_{i=1}^{N} L(y\_i, F(x\_i;p))$$

を最小化するパラメータ $p$ を求めるために使われることが多いです．  
この場合のGradient Descentを，パラメータを変化させて目的関数を最小化するという意味で，  
**パラメータ空間におけるGradient Descent**と言うことにしましょう．  

パラメータ空間におけるGradient Descentで，$T$回反復を終えた後の解は  
$p\_t' = - \nabla \phi(p\_{t-1})$ とおいて，初期値を $p\_0$ とすると，次のように表すことができます．

$$p\_T = p\_0 + \sum\_{t=1}^{T} \alpha\_t p\_t'$$

なんとなくBoostingの式と似てませんか？  

Boostingでは，すでに学習した弱学習器のパラメータを変化させるのではなく，  
新しい弱学習器を加えることにより全体の出力を変化させることができます．  
そこで，目的関数を $F\_{t-1}$ で微分して降下方向を出し $f\_t$ をそれにfitさせることで，  
**関数の空間でGradient Descent**をしよう，というのがGradient Boostingになります．  


Gradient Boosting [3]
---

関数区間でGradient Descentをする場合には目的関数は次のように書けます．  

$$\phi(F) = \sum\_{i=1}^{N}L(y\_i, F(x\_i))$$

しかし各データの損失の和を最小化する方向を求めるのは一般には難しいので，  
各データ $(x\_i, y\_i)$ についてそれぞれで
損失 $L(y\_i, F(x\_i))$ を小さくすることを考えます．  
つまり各 $x\_i$ について損失が小さくなる向きに関数の出力を変化させるわけです．  

$t-1$ 回目の反復が終わった後の全体の出力を$F\_{t-1}(x)$として，  
$F\_t(x)$ が各 $(x\_i, y\_i)$ に対して次のようになってくれればうれしいです．  
(出力に1次元を想定しているので $\nabla$ はただの偏微分になります)  

$$F\_{t}(x\_i) = F\_{t-1}(x\_i) - \alpha\_t \frac{\partial L(y\_i, F\_{t-1}(x\_i))}{\partial F\_{t-1}(x\_i)}$$

従って，

$$f\_t(x\_i) = - \frac{\partial L(y\_i, F\_{t-1}(x\_i))}{\partial F\_{t-1(x\_i)}}$$

となるように弱学習器 $f\_t$ の学習を行います．  
具体的には各 $x\_i$ に対して次のような $\tilde{y\_i}$ を考え，

$$\tilde{y\_i} = - \frac{\partial L(y\_i, F\_{t-1}(x\_i))}{\partial F\_{t-1}(x\_i)}$$

データ $(x\_i, \tilde{y\_i})$ に対して二乗誤差  

$$\sum\_{i=1}^N(\tilde{y\_i} - f\_t(x\_i))^2$$

が最小になるように弱学習器 $f\_t$ をfitさせます．  
その後，全体の損失 $\phi(F\_{t-1} + \alpha\_t f\_t)$ が小さくなるように$\alpha\_t$ をLine Searchなどで決定します．  

$T$回反復を終えた後の解は，初期値を $f\_0$ として，次のように表すことができます．

$$F\_T(x) = f\_0(x) + \sum\_{t=1}^{T} \alpha\_t f\_t(x)$$

これが最もベーシックなGradient Boostingになります．  
初期値については元論文[3]では目的関数を最小化するような定数にしています(XGBBoostの実装は確認してない)．  

疑似コードにすると次のようになります．  
<img src="/images/gradient_boosting_pseudo_code.png" width="400px">

Regression Tree
---
これまでは弱学習器に何を用いるか特に決めずに解説しましたが，  
Gradient Boosting では回帰木 (Regression Trees) が使われることが多いため，  
回帰木の**CART**[4]による構築について触れておきます．  
Gradient Boostingの話からは少しずれるので興味ない場合は飛ばしても大丈夫だと思います．  

回帰木では葉に値が紐づいています(その値を葉の重みと呼びます)．  
葉が$T$ 個あるとして，適当に葉に1から$T$までの番号をふり，  
その葉の重みを $w\_j (j=1,2,...,T)$ と表すことにします．  
また，木への入力 $x$ がたどり着く葉の番号を $q(x)$ としましょう．  
$x$ に対する木の出力 $f(x)$ は次のように書けます．

$$f(x) = w\_{q(x)}$$

今回はGradient Boostingに使う弱学習器という文脈なので，  
N個のデータ$(x\_i, \tilde{y\_i})$に対して，二乗誤差和を最小化する木の構築を考えてみます．

$$\sum\_{i=1}^N (\tilde{y\_i} - f(x\_i))^2$$

この式は，木の構造が決まっているとき，すなわち関数 $q$ が決まっているとき，  
$j$ 番目の葉にたどり着くデータの集合 $I\_j = \\\{ i~|~1\leq i\leq N, q(x\_i) = j \\\}$を用いて

$$\sum\_{j=1}^T \sum\_{i\in I\_j} (\tilde{y\_i} - w\_j)^2$$

と変形できます．さらにガチャガチャ変形すると

$$\sum\_{j=1}^T |I\_j|(w\_j - \sum\_{i=1}^N \frac{y\_i}{|I\_j|})^2 + constant$$

となり$w\_j$ の値を $I\_j$ に含まれる $y\_i$ の平均にすることで最小値を取ることがわかります．  
このように，最小化したいものが二乗誤差和である場合には，   
**ある木が実現できる最小値が解析的に求められます**．  
(今回は二乗誤差でしたが他にも様々な損失関数に対して使えます)  

この最小値をその木の評価値(一般的には**不純度**と呼ばれます)として扱い，  
この評価値が低くなるように木の構築を行います．  
木の構築では，ルートノード1つしかない状態から始めて，  
一定の深さになるか損失が下がらなくなるまでノードの分割を繰り返します．  

分割対象になったノードに対して，そのノードに到達するデータの集合を $I$とし，  
ある特徴量のある値を閾値として $I$ が $I\_L$ と $I\_R$ に分割されたとします．  
その分割による木の評価値の変化(減少量)は次のように表されます．  

Gain = ( $I$ の評価値) - ( $I\_L$ の評価値 + $I\_R$ の評価値)

これを$I$のすべてのデータのすべての特徴量で試し一番Gainが大きくなるものを選びます．  

この厳密に全ての候補について試すという方法は  
XGBoostの論文では **"Exact" Greedy Algorithm** と呼ばれています．  


Gradient Tree Boosting [3]
---

回帰木を使う場合にはGradient Boostingをさらに効率的に行うことができます．  
Gradient Boosting で最小化したい目的関数は，木の構造が決まると，  

$$\sum\_{j=1}^T \sum\_{i\in I\_j} L(y\_i, F\_{t-1}(x\_i) + w\_j)$$

と変形することができます．この式が解析的に解ける場合には，  
$(x\_i, \tilde{y\_i})$ にfitするように木を構築した後，$w\_j$ をこの式を最小化するように再び変更することで  
Line Search などで $\alpha\_t$ を決める処理を行う必要がなくなるわけです．

でもその式が解析的に解けるのであれば，最初から $(x\_i, \tilde{y\_i})$ の二乗誤差和じゃなくて

$$\sum\_{i=1}^N L(y\_i, F\_{t-1}(x\_i) + f\_t(x\_i))$$

を最小化するように木を構築すればいいじゃないかと思うわけですが，  
二乗誤差和を損失に使うほうが断然早いので良いという感じらしいです．  

Learning rate [3]
---

Gradient Boostingの正則化として，更新を行う際に  
次のように Learning Rate (学習率) $\eta$ を使う方法が提案されています．

$$F\_t(x) = F\_{t-1}(x) + \eta \alpha\_t f\_t(x)$$

学習率を低くするとパフォーマンスが良くなるということが経験的に知られていて，  
学習率を低くするとその分最適な反復回数は大きくなることも言われています．  
(ここで言う最適はleave-out test sampleで損失が最小になる回数)  

(XGBoostを)実際に使ってみている感覚としては学習率は確かに小さいほうが良くて，  
0.01とか0.005くらいで十分に小さいという印象があります．  
それ以上は小さくしても遅くなるだけであまり精度に違いはでない感じがします．  
0.1とかだとやや大きいけどやや大きいけどデータによっては十分精度が出て，  
1.0だとかなり過学習しやすいような感じです(個人の感想です)．  


Newton Boosting
---

さて，これまで説明した Gradient Boosting は  
関数空間でGradient Descentを用いて目的関数を最小化しているのでした．

次はこの最小化をGradient Descentでなく[**Newton法**](https://en.wikipedia.org/wiki/Newton%27s\_method\_in\_optimization)で行う場合について考えてみます．  
(ここでいうNewton法は[根を見つける手法](https://en.wikipedia.org/wiki/Newton%27s\_method)のことではありません)  

Newton法では目的関数をテイラー展開で**二次の項**まで近似して，  
高校数学で習った二次関数の最小化と同じノリで最小化を行います．  

弱学習器 $f\_t$ を加えるときの目的関数は次の式で表せます．

$$\sum\_{i=1}^{N}L(y\_i, F\_{t-1}(x\_i) + f\_t(x\_i))$$

この式を二次近似して次式を得ます．  

$$\sum\_{i=1}^{N}[~L(y\_i, F\_{t-1}(x)) + g\_i f\_t(x\_i) + \frac{1}{2}h\_i f\_t^2(x\_i)~]$$

ここで $g\_i = \frac{\partial L(y\_i, F\_{t-1}(x\_i))}{\partial F\_{t-1}(x\_i)}$ で $h\_i = \frac{\partial^2 L(y\_i, F\_{t-1}(x\_i))}{\partial^2 F\_{t-1}(x\_i)}$です．  
(ちなみに $-g\_i$ は Gradient Boostingでの $\tilde{y\_i}$ と一致します)  
この式を変形して $f\_t$ に関係の無い項をconstantとすると次のようになります．  

$$\sum\_{i=1}^{N}[~\frac{h\_i}{2} (f\_t(x\_i) + \frac{g\_i}{h\_i})^2 ~] + constant$$

$(x\_i, - g\_i / h\_i)$ に対する二乗誤差が $h\_i$ で重みづけされた形になりました．  
この式を最小化するように $f\_t$ の構築を行う方法を**Newton Boosting**と呼びます[5]．  
回帰木では先の二乗誤差和の例と同様に，この式を直接目的関数として扱うことができます．  

Newton法では，目的関数が二次でない場合は適当に定めた $\alpha\_t$ を使うのですが，  
これは Learning Rate を適当にスケールして吸収すればよいので，  
Newton Boosting の場合は $\alpha\_t=1$ とします．  


XGBoost [6]
---

XGBoostではこのNewton Boostingが採用されています．  
さらに，**木の正則化**を行うための項を最小化する目的関数 $\phi$ に直接入れているのが特徴的です．  
(個人的には木はtrimとかで正則化するイメージですが直接目的関数にいれています)  

具体的には次のような目的関数を設定しています．  

$$\phi(F\_t) = \sum\_{i=1}^{N}L(y\_i, F\_t(x\_i)) + \sum\_{k=0}^t \Omega(f\_k)$$
$$\Omega(f) = \gamma T + \frac{1}{2}\lambda||w||^2$$

ここで，$T$ は回帰木 $f$ の葉の数，$w$ は葉の重みで，$\gamma, \lambda$はハイパーパラメータです．  
この形の正則化項であれば，普通のNewton Boostingと同じように  
二次近似して変形することで同じように回帰木を構築しやすい形にできます．  

XGBoostを実際に使うときの指定としては  
そのまま $\gamma$ は `gamma`，$\lambda$ は `lambda` というパラメータがあります．  
デフォルトの値はそれぞれ $0$ と $1$ です．  
論文には載っていませんが，doc/parameter.md を見る限り  
`alpha` というパラメータで葉の重みのL1ノルムでの正則化も行えるようです．  

また，高速化のための工夫として，データの数や次元数が大きくなった場合，  
木の構築に Exact Greedy Algorithm を使うと時間がかかりすぎてしまうのを改善するため，  
分割に使う候補を絞る **Weighted Quantile Sketch** という手法も提案されています．  

データが沢山あって，ここから分割の候補を $m$ 個選んでください，と言われたとき，  
素直な方法として，小さい順に並べて等間隔に $m$ 個取る，という方法が考えられます．  
この，同じ要素数の $m$ 個の部分集合に分割する点を $m$-Quantiles ($m$-分位点) と言い，  
Quantileを高速に求めるアルゴリズムとして Quantile Sketch[7] があります．  

Weighted Quantile Sketchはその名の通り，  
このQuantile Sketchを重み付きに拡張したものです．  

Newton Boosting の項で説明した通り，  
XGBoostの目的関数は二乗誤差が $h\_i$ で重みづけられた形になるため，  
$h\_i$ が大きいほど $f\_t$ でうまくfitできなかったとき目的関数に与える影響が大きくなります．  
そこで通常のQuantile Sketchのように各々1つとして扱ってQuantileを求めるのでなく，  
$h\_i$ で重みづけしQuantile Sketchを行います．  

既存研究では無かった理論保証付きのアルゴリズムを提案したそうで，論文でめっちゃ推されてます．  
詳しい内容についてはXGBoost論文の[Supplementary Material](http://homes.cs.washington.edu/~tqchen/pdf/xgboost-supp.pdf)に載っています．

Sketchingを使用するように明示的に指定するには  
パラメータの `tree_method` を `'approx'`にすれば良いです．  
また `sketch_eps` で候補点がどれくらい離れるかを指定できます．  

この他にも，スパースなデータに対して高速に分割を見つけるアルゴリズムが実装されていたり，  
データをブロック化して効率的に扱う機能がついていたりなど，  
大規模な環境で高速に動作するために様々な工夫が行われています．  


Generalization Error
---

理論的な汎化誤差についてはまだわかっていることは少ないようです(たぶん)．  

ここが私が一番気になっているところで，  
Gradient Boostingでは加えた後の経験損失が小さくなるように弱学習器を足しているわけですが，  
なんで弱学習器をより複雑にして損失をさげるよりも，  
複雑でない弱学習器でこの手続きを繰り返すほうがうまくいくのでしょうか．  
また，なんで $\alpha\_t$ を求めた上でさらに学習率をかける方法がうまくいくのでしょうか．  
不思議です．その辺について，汎化誤差から理論的に何か言えることはないのかなと思っています．  

AdaBoostについては元々統計的機械学習というより学習理論の分野で出てきたこともあって，  
古くから汎化誤差について研究が進められています．  
ここら辺は正直ちゃんと理解できておらずうまく説明できる気がしないので，詳しくは  
AdaBoostに関するsurvey論文[8]の章とか，marginの話の論文[9]とかを読んでくださいという感じです．  
参照している論文が結構古いのでもしかしたらそこらへんの研究はもう少し進んでいるかもしません．

また，Gradient Boosting の汎化誤差については調べてみたものの見つからなかったので，  
これらについて何か情報があったら教えてもらえると非常に助かります．  
もしかしたらGradient Descentのほうから調べていったほうが良いのかもしれません．  
よくわからんという感じです．強い人教えてください．


Conclusion  
---

かなり書き散らした感じになって今いましたがとりあえず以上になります．  
いま自分が抱えている研究のタスクが終わったら，  
このAdaBoostの汎化誤差の論文をちゃんと読んだり，Gradient Boostingの汎化誤差のことを調たりしつつ  
XGBoostの学習アルゴリズムをいろいろと改造して遊んでみたいと思っています．  

ご指摘等ありましたら[Github](https://github.com/zaburo-ch)に載ってるアドレスか，  
[Twitter](https://twitter.com/musharna000)等で連絡いただければと思います．  

HugoにReferenceの機能がないのでぽちぽち自分で番号書いたりした...  
ここだけbibtex使いたい...  

Reference
---

[1] Robert E. Schapire. The strength of weak learnability. Machine Learning, 5(2):197–
227, 1990.  
[2] Yoav Freund and Robert E. Schapire. A decision-theoretic generalization of on-line
learning and an application to boosting. Journal of Computer and System Sciences,
55(1):119–139, 1997.  
[3] Jerome H. Friedman. Greedy function approximation: A gradient boosting machine.
The Annals of Statistics, 29(5), 2001.  
[4] Leo Breiman, Jerome H. Friedman, Richard A. Olshen, and Charles J. Stone. Classification and regression trees. The Wadsworth and Brooks-Cole statistics-probability series, Taylor & Francis.  
[5] Didrik Nielsen. Tree Boosting With XGBoost - Why Does XGBoost Win "Every" Machine Learning Competition? Master thesis, Norwegian University of Science and Technology, 2016.  
[6] Tianqi Chen and Carlos Guestrin. Xgboost: A scalable tree boosting system. Proceedings of the 22Nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785-794, 2016.  
[7] Michael Greenwald and Sanjeev Khanna. Space-Efficient Online Computation of Quantile Summaries. Proceedings of the 2001 ACM SIGMOD international conference on Management of data, 58-66, 2001  
[8] Robert E. Schapire. The boosting approach to machine learning: An overview. Nonlinear estimation and classification. 149-171, 2003.  
[9] Robert E. Schapire, Yoav Freund, Peter Bartlett, and Wee Sun Lee. Boosting the
margin: A new explanation for the effectiveness of voting methods. The Annals of
Statistics, 26(5):1651–1686, 1998.  

