# LogoGPT-Analyzer

LogoGPT-Analyzerは、LoGoチャットのXMLログファイルからChatGPTとの対話データを抽出し、CSVファイルに出力するためのPythonスクリプトです。

## 特徴

- XMLファイルからの対話データ抽出
- 質問と回答の文字数計算
- 結果のCSVファイル出力
- 統計情報の生成
- マルチプロセッシングによる高速な処理

## インストール方法

1. このリポジトリをフォークしてください。
2. フォークしたリポジトリをクローンします：

   ```
   git clone https://github.com/YourUsername/LogoGPT-Analyzer.git
   cd LogoGPT-Analyzer
   ```

3. 仮想環境を作成し、アクティベートします：

   ```
   python -m venv .venv
   source .venv/bin/activate  # Linuxの場合
   .venv\Scripts\activate  # Windowsの場合
   ```

4. 必要なパッケージをインストールします：

   ```
   pip install -r requirements.txt
   ```

## 使用方法

1. スクリプトを実行します：

   ```
   python LoGo_Gpt_Analyzer.py
   ```

2. フォルダ選択ダイアログが表示されるので、XMLファイルが格納されているフォルダを選択します。
3. 処理が完了すると、以下のファイルが生成されます：
   - `combined_results.csv`: 全ての質問と回答の詳細情報
   - `questions_only.csv`: 質問のみの詳細情報
   - `statistics.csv`: 統計情報
   - `process_log.log`: 処理ログ

## 貢献方法

プロジェクトへの貢献を歓迎します。貢献方法の詳細は[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)のもとで公開されています。

## セキュリティ

セキュリティの脆弱性を発見した場合は、[SECURITY.md](SECURITY.md)の指示に従って報告してください。