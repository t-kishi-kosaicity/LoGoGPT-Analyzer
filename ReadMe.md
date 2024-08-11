# LogoGPT-Analyzer

## 概要
LogoGPT-Analyzerは、LoGoチャットのXMLログファイルからChatGPTとの対話データを抽出し、CSVファイルに出力するためのPythonスクリプトです。このツールは、組織内でのChatGPTの利用状況を分析し、効果的な質問例を見つけるのに役立ちます。

## 特徴
- XMLファイルからの対話データ抽出
- 質問と回答の文字数計算
- 結果のCSVファイル出力
- 統計情報の生成
- ユーザーフレンドリーなGUIによるフォルダ選択
- マルチプロセッシングによる高速な処理

## 前提条件
- Python 3.6以上
- 必要なPythonパッケージ（requirements.txtを参照）

## インストール方法

1. リポジトリをクローンまたはダウンロードします。
2. 仮想環境を作成し、アクティベートします:
```bash
python -m venv .venv
source .venv/bin/activate  # Linuxの場合
.venv\Scripts\activate  # Windowsの場合
```
3. 必要なパッケージをインストールします:
```bash
pip install -r requirements.txt
```

## 使用方法

1. スクリプトを実行します:
```bash
python LoGoGPT-Analyzer.py
```
2. フォルダ選択ダイアログが表示されるので、XMLファイルが格納されているフォルダを選択します。
3. 処理が完了すると、以下のファイルが生成されます:
   - `combined_results.csv`: 全ての質問と回答の詳細情報
   - `questions_only.csv`: 質問のみの詳細情報
   - `statistics.csv`: 統計情報
   - `process_log.log`: 処理ログ

## 後処理

1. `questions_only.csv`を使用して、ChatGPTに効果的な質問例を10個選んでもらいます。
2. 選ばれた質問例をPowerPointファイル（`selected_10questions.pptx`）にまとめます。
3. 生成されたCSVファイルと`selected_10questions.pptx`を適切なフォルダに保存します。
4. `statistics.csv`の内容を`logo_gpt_count.xlsx`に貼り付けます。
5. `selected_10questions.pptx`を加工し、組織内の掲示板に掲示します。

## 注意事項
- XMLログファイルは月に1回しか出力できません。
- ファイルに機密情報が含まれる可能性があるため、適切なアクセス制御を行ってください。
- 大量のXMLファイルを処理する場合、十分なメモリを確保してください。

## 開発者向け情報
- コードの詳細な説明やエラー対応については、ChatGPTを活用してください。
- 改善提案やバグ報告は、Issueを通じてお知らせください。

## ライセンス
このプロジェクトは[MITライセンス](LICENSE)のもとで公開されています。