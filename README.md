# chofu-premium-gift
## これは何？
[調布のプレミアム付商品券のページ](https://premium-gift.jp/chofu2021/use_store) のデータを  
スクレイピングするためのPythonスクリプトです。  

公式サイトでちんたら検索するよりも、一覧で手に入れてMyMapに落とし込んだほうが便利だと思ったので作りました。  

## 使い方  
python3.8 + pipenv の環境が必要です。  

```
# 必要なパッケージのインストール  
$ pipenv install

# 実行
$ scrapy crawl gift_ticket -o data.csv
```  

後は生成したCSVを MyMapでインポートして完了です。  

## ライセンス
MIT License  
