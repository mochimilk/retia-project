# Retia Project
 バーチャルMastodonアイドルれてぃあたん26歳
 
 1. れてぃあたんが学ぶcron基礎講座（終了）
 2. れてぃあたんで学ぶPython基礎講座
 3. れてぃあたんと学ぶ正規表現基礎講座
 4. れてぃあたんと学ぶMastodon API講座（終了）

誰かが特定のワードをトゥーした時「○○かわいい」を自動でトゥーするれてぃあたん

雑な設計書
- botアカウントでログインする
- HTLか通知からトゥー拾う
- トゥー本文と名前を抽出
- 本文の正規表現マッチング
- 発言を生成
- トゥーする

現在使ってるスクリプトファイル
- stream_test2.py

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="クリエイティブ・コモンズ・ライセンス" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />この 作品 は <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">クリエイティブ・コモンズ 表示 - 非営利 4.0 国際 ライセンス</a>の下に提供されています。
（traffic.pyを除く）
