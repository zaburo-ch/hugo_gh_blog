+++
date = "2015-09-12T00:08:08+09:00"
title = "Go言語でリダイレクト先のURLを取得する"
tags = ["Go", "HTTP"]
+++
タイトルのとおりGoでリダイレクト先のURLを取得します。  
Goでは普通にClientを使ってGETやらHEADリクエストを行うと、  
リダイレクトがあったとき自動的にリダイレクト先の内容をとってくるようになっているので、  
今回のようにリダイレクト先に行く必要の無い特殊なケースでは、  
リダイレクト時の動作を変更するか、より低レベルのメソッドを利用することで対応します。  

参考にしたページ  
[rest - How Can I Make the Go HTTP Client NOT Follow Redirects Automatically? - Stack Overflow](http://stackoverflow.com/questions/23297520/how-can-i-make-the-go-http-client-not-follow-redirects-automatically)

リダイレクト時の動作を変更する  
----
```Client.CheckRedirect func(req *Request, via []*Request) error```  
がリダイレクト時の動作を定めているためこれを変更します。  
CheckRedirectがerrorを返すと、Clientはリダイレクト先を取得する代わりに  
前のレスポンスの内容とそのerror(wrapped in a url.Error)を返します。  

<script src="https://gist.github.com/zaburo-ch/98a1a0bfef742111020b.js"></script>

30行目では型アサーションを用いてRedirectAttemptedErrorが起こったかを確認しています。  
HEADリクエストの場合もBodyをcloseしなきゃいけないのかはちょっとわかりませんが、  
[これ](http://golang.org/pkg/net/http/#Response)を見る限りは必要そうなのでcloseしています。  

より低レベルのメソッドを利用する
----
http.TransportのRoundTripメソッドを使ってリクエストを行います。  

<script src="https://gist.github.com/zaburo-ch/99e58cf8fa9d3d11bd6a.js"></script>

Transportの設定難しそうだったのでひとまずhttp.DefaultTransport使ってます。  
ClientはStatusCodeが301,302,303,307の時にリダイレクトの処理を行うので、  
たぶんこの20行目の書き方でも上手く行くはずです。  
複数の値のどれかと一致すればtrueみたいな書き方がわからなかったので  
愚直に4つ書いて並べてあります。なんかいい方法あるんでしょうか。  
Pythonみたいにin演算子とかあればいいんですけどね。  