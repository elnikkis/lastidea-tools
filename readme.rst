================================
ラストイデア アイテムビューワ
================================

viewer/
   ラストイデア公式シミュレータのデータを使ってアイテム一覧を表示する

lastidea_crawler/
   5ch wikiからのアイテムのデータ収集



viewer
=============

使い方
--------

1. `公式シミュ <https://sim.lastidea.jp/>`_ のJSONデータをダウンロードしてくる
2. viewer/index.html をブラウザで開く


JSONデータ
------------

いまのところ必要なものは properties.json と equipments.json

ダウンロードしてくる。

- https://cache-sim-lastidea.sqex-edge.jp/json/20190716131456
- https://cache-sim-lastidea.sqex-edge.jp/json/20190614190605

- https://cache-sim-lastidea.sqex-edge.jp/json/20190614190605/baseStatus.json
- https://cache-sim-lastidea.sqex-edge.jp/json/20190614190605/characterLevels.json
- https://cache-sim-lastidea.sqex-edge.jp/json/20190614190605/equipments.json
- https://cache-sim-lastidea.sqex-edge.jp/json/20190614190605/groupedEquipmentIdsBySlot.json
- https://cache-sim-lastidea.sqex-edge.jp/json/20190614190605/properties.json
- skillTrees.json
- groupedSkills.json
- groupedSkillLevels.json



lastidea_crawler
======================

.. code:: shell

   python -m lastidea_crawler.get_itemlist > data/itemlist.tsv
   python -m lastidea_crawler.get_properties < data/itemlist.tsv > data/properties.tsv
   python -m lastidea_crawler.show_target_property data/itemlist.tsv data/properties.tsv '炎ダメージ倍率'

