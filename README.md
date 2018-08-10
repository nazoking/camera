監視カメラ
=========

 * `recorder.py` 保存機
 * `server.py` 簡易web管理画面
 * `config.json` 設定ファイル
 * `system` systemd 用の設定ファイル。 `make install` でインストールされる
 * `Makefile` make で rsync 等


　recorder が一定時間 config["sleep_sec"] ごとにカメラをキャプチャし、 config["base_dir"] に保存する。
  server は 5800 ポートで待ち受けている。現在のキャプチャ（１秒毎）と、過去の一覧が見える。
　ファイルのダウンロードは samba から
