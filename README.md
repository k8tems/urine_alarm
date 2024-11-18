### 腎臓移植後の排尿スケジュールを管理するアプリ

腎臓移植後、24時間1又は2時間に1回トイレに行って腎臓のメンテナンスを行う必要がある  
対応するスプシのスケジュールを監視しつつ、適宜当スクリプトでアラームの設定を行う  
アラームはiftttを用いて携帯で鳴らす  
退院後スプシ抜いてiPhone単体で動くアプリにパッケージ化予定  

- 必要な物
  - google sheetsにアクセスする為の`credentials.json`
  - ifttt_urlが設定された`config.yaml`(`sample_config.yaml`参照)  
  - 好きなアラーム音のalarm.wav  
  10回鳴らされる  

- スプシ  
https://docs.google.com/spreadsheets/d/1uOgZufvXS7L54ccVaeUhFIk7wW665NceGetH2pB2SKo/edit?usp=sharing
![](https://gyazo.com/bf6cfce6be43c9b638d753c8af5968f1.j)

スプシを日時に分けたの返ってややこしくしてるだけだから  
一つにまとめて日時に絞り込めるようにした方が良い事に気付いたけど、  
排尿スケジュールが終わって退院が近づいてるのでアプリにする時に考える  

### TODO
- ネット切れた時の通知
- このパターンを再現する
![](https://gyazo.com/db77d2891e25eaf02dcf42d8a9455412.j)
＞単純に窓が裏にあると駄目って事？
