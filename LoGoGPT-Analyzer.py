import xml.etree.ElementTree as ET
import csv
import os
import logging
from typing import List, Dict, Tuple
import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ProcessPoolExecutor, as_completed

# Constants
USER_ID_GPT = "1443074843376353280"
QUESTION_PREFIXES = [
    "{@:1443074843376353280,20}@LoGo AIアシスタント GPT-4 さん",
    "{@:1443074843376353280,19}@LoGoAIアシスタント GPT-4 さん"
]
NAMESPACE = {"ns": "https://ns.direct4b.com/export"}

def select_directory() -> str:
    """
    ユーザーにフォルダ選択ダイアログを表示し、選択されたフォルダのパスを返す。
    """
    root = tk.Tk()
    root.withdraw()  # Tkのルートウィンドウを非表示
    folder_path = filedialog.askdirectory()  # ダイアログを表示してフォルダパスを取得
    return folder_path

def parse_xml_data(xml_file_path: str) -> Tuple[List[Dict], List[Dict], int, int, int]:
    """
    XMLファイルを解析し、必要なデータを抽出する。
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        logging.error(f"Error parsing XML file {xml_file_path}: {e}")
        return [], [], 0, 0, 0

    extracted_questions = []
    extracted_answers = []
    message_count = 0
    total_question_length = 0
    total_answer_length = 0

    for message in root.findall(".//ns:message", NAMESPACE):
        message_count += 1
        user_elem = message.find("ns:user", NAMESPACE)
        text_elem = message.find("ns:content-text", NAMESPACE)
        timestamp = message.find("ns:timestamp", NAMESPACE).text if message.find("ns:timestamp", NAMESPACE) is not None else ""

        if user_elem is not None and text_elem is not None:
            user_id = user_elem.get('id')
            text_content = text_elem.find('ns:text', NAMESPACE).text if text_elem.find('ns:text', NAMESPACE) is not None else ""

            if text_content:
                if any(text_content.startswith(prefix) for prefix in QUESTION_PREFIXES):
                    for prefix in QUESTION_PREFIXES:
                        text_content = text_content.replace(prefix, "")
                    question_length = len(text_content)
                    total_question_length += question_length
                    extracted_questions.append({
                        'User ID': user_id,
                        'Type': '質問',
                        'Text': text_content,
                        'Length': question_length,
                        'Timestamp': timestamp
                    })
                elif user_id == USER_ID_GPT:
                    answer_length = len(text_content)
                    total_answer_length += answer_length
                    extracted_answers.append({
                        'User ID': user_id,
                        'Type': '回答',
                        'Text': text_content,
                        'Length': answer_length,
                        'Timestamp': timestamp
                    })

    return extracted_questions, extracted_answers, total_question_length, total_answer_length, message_count

def sort_data_by_timestamp(data: List[Dict]) -> List[Dict]:
    """
    データをタイムスタンプでソートする。
    """
    return sorted(data, key=lambda x: x['Timestamp'])

def write_to_csv(data: List[Dict], csv_file_path: str, only_question: bool = False) -> None:
    """
    抽出したデータをCSVファイルに書き込む。
    """
    data_sorted = sort_data_by_timestamp(data)
    if only_question:
        data_sorted = [item for item in data_sorted if item['Type'] == '質問']

    fieldnames = ["User ID", "Type", "Text", "Length", "Timestamp"]
    try:
        with open(csv_file_path, mode='w', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_sorted)
    except IOError as e:
        logging.error(f"Error writing to CSV file {csv_file_path}: {e}")

def write_statistics_to_csv(folder_path: str, total_messages: int, questions: List[Dict], total_question_length: int, total_answer_length: int) -> None:
    """
    統計情報をCSVファイルに書き込む。
    """
    csv_file_path = os.path.join(os.path.dirname(folder_path), 'statistics.csv')
    unique_questioners = set(item['User ID'] for item in questions)
    num_questioners = len(unique_questioners)

    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Total Messages", "Questions", "Unique Questioners", "Total Question Length", "Total Answer Length"])
            writer.writerow([total_messages, len(questions), num_questioners, total_question_length, total_answer_length])
    except IOError as e:
        logging.error(f"Error writing statistics to CSV file {csv_file_path}: {e}")

def log_results(file_count: int, questions: List[Dict], answers: List[Dict], total_question_length: int, total_answer_length: int, total_messages: int) -> None:
    """
    処理結果をログファイルに記録する。
    """
    log_file_path = os.path.join(os.path.dirname(__file__), 'process_log.log')
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

    logging.info(f"Processed XML files: {file_count}")
    logging.info(f"Total messages: {total_messages}")
    logging.info(f"Questions processed: {len(questions)}")
    logging.info(f"Answers processed: {len(answers)}")
    logging.info(f"Total question length: {total_question_length}")
    logging.info(f"Total answer length: {total_answer_length}")
    logging.info(f"Results saved to {log_file_path}")

def process_xml_file(xml_file_path: str) -> Tuple[List[Dict], List[Dict], int, int, int]:
    """
    XMLファイルを処理し、結果を返す。
    """
    return parse_xml_data(xml_file_path)

def main() -> None:
    """
    メイン関数: ユーザーにフォルダを選択させ、XMLファイルからデータを抽出し、CSVファイルに書き出す。
    """
    folder_path = select_directory()
    if not folder_path:
        print("No folder selected.")
        return

    total_questions_length = 0
    total_answers_length = 0
    total_messages = 0
    all_questions = []
    all_answers = []
    file_count = 0

    xml_files = [os.path.join(dirpath, f) for dirpath, _, filenames in os.walk(folder_path) for f in filenames if f.endswith(".xml")]

    with ProcessPoolExecutor() as executor:
        future_to_file = {executor.submit(process_xml_file, xml_file): xml_file for xml_file in xml_files}
        for future in as_completed(future_to_file):
            xml_file = future_to_file[future]
            try:
                questions, answers, question_length, answer_length, msg_count = future.result()
                all_questions.extend(questions)
                all_answers.extend(answers)
                total_questions_length += question_length
                total_answers_length += answer_length
                total_messages += msg_count
                file_count += 1
            except Exception as exc:
                logging.error(f'{xml_file} generated an exception: {exc}')

    write_to_csv(all_questions + all_answers, os.path.join(os.path.dirname(folder_path), 'combined_results.csv'))
    write_to_csv(all_questions, os.path.join(os.path.dirname(folder_path), 'questions_only.csv'), only_question=True)
    write_statistics_to_csv(folder_path, total_messages, all_questions, total_questions_length, total_answers_length)
    log_results(file_count, all_questions, all_answers, total_questions_length, total_answers_length, total_messages)

if __name__ == "__main__":
    main()