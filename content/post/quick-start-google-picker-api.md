+++
date = "2015-08-06T01:41:08+09:00"
title = "Google Picker API を使ってみる"
tags = ["Picker API", "Google Drive", "JavaScript", "Google App Engine"]
+++
Google Driveのファイルを利用できるPicker APIを
GAE上で使ってみたのでメモっておきます。  
クライアントIDが何かとか詳しい話は抜きにしてとにかく動かすまで。  

こちらのガイドに従ってやります。  
[https://developers.google.com/picker/docs/](https://developers.google.com/picker/docs/)  

まずPciker APIを有効にします。  
[Google Developers Console](https://console.developers.google.com/)にログインしてAPIを使うプロジェクトのページに入ります。  
左側のサイドバーの「APIと認証」->「API」を選択。  
Pickerとかで検索して「Google Picker API」を選択しAPIを有効にします。  

次にクライアントIDとAPIキーを作成します。  
「APIと認証」->「認証情報」から2つとも作成できます。  

クライアントIDの方はウェブアプリケーションを選択し、  
「JavaScript 生成元」にはAPIを使用するページのオリジンを指定。  
今回はlocalhost:8080でも動いて欲しいので次の二つを指定しました。  
http://プロジェクトID.appspot.com/  
http://localhost:8080/  
リダイレクトURLはよくわからなかった。とりあえず、  
http://localhost:8080/oauth2callback  
みたいな感じで指定してるけどたぶん意味ないです。  

APIキーの方はブラウザキーを選択。  
リファラーはクライアントIDの時と同じ感じで  
http://プロジェクトID.appspot.com/*  
http://localhost:8080/*  
としました。  

これでクライアントIDとAPIキーが取得できたので  
先のガイドの「The "Hello World" Application」のとおりにページを用意して  
developerKeyとclientIdを書き換えればとりあえず動きます。  

このスクリプトの流れは、  
<pre><code>&lt;script type="text/javascript" src="https://apis.google.com/js/api.js?onload=onApiLoad"&gt;&lt;/script&gt;
</code></pre>
でGoogle API Loader scriptを読み込む。  
読み込みが終わると onload=onApiLoad で指定しているonApiLoadが呼ばれて  
authとpickerのスクリプトが読み込まれる。  
両方読み込まれるとcreatePicker()の内容が実行されて  
pickerのインスタンスが作成、可視化される。  
という感じになっています。  

pickerの生成時にコールバック用の関数とかいろいろ指定できるのですが、  
addView()の部分がキモで、ここで表示されるファイルの種類を指定しています。  
指定方法についてはガイドの「Showing Different Views」に表が載っていて  
サンプルの通りだとPicasaのWeb Albumsにある写真が表示されるようになっています。  

こことscopeを表に従って変えればGoogle Driveのアイテムとかも表示できるのですが  
全部取得してしまうとごちゃごちゃになるのでsetMimeTypesでMIME Typeを指定します。  
MIME Typeは[MIME Type 一覧表](http://www.plala.or.jp/access/community/phps/mime.html)を見て適当に。  
例えばpdfだけを表示するようにしたい場合は次のようにします。  
<pre><code>function createPicker() {
    var view = new google.picker.View(google.picker.ViewId.DOCS);
    view.setMimeTypes("application/pdf");
    if (pickerApiLoaded && oauthToken) {
        var picker = new google.picker.PickerBuilder().
            addView(view).
            setLocale('ja').
            setOAuthToken(oauthToken).
            setDeveloperKey(developerKey).
            setCallback(pickerCallback).
            build();
        picker.setVisible(true);
    }
}
</code></pre>
setLocale('ja')で日本語で表示するよう指定することができます。  

Pcikerで取得した内容はsetCallbackで指定した関数にJSONで渡されるので  
これを適当に処理してやればおっけーです。  


以上です。  

[Google Drive File Picker Example](https://gist.github.com/Daniel15/5994054)  
Gistにもっと工夫したものがあったのでこれも参考にするといいと思います。  