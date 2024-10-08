import os
import pytest
from LoGoGPT_Analyzer import parse_xml_data, sort_data_by_timestamp, write_to_csv

# テスト用のサンプルXMLデータ
SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<ns:export xmlns:ns="https://ns.direct4b.com/export">
  <ns:message>
    <ns:user id="user1"/>
    <ns:content-text>
      <ns:text>{@:1443074843376353280,20}@LoGo AIアシスタント GPT-4 さんこれはテスト質問です</ns:text>
    </ns:content-text>
    <ns:timestamp>2023-01-01T12:00:00</ns:timestamp>
  </ns:message>
  <ns:message>
    <ns:user id="1443074843376353280"/>
    <ns:content-text>
      <ns:text>これはテスト回答です</ns:text>
    </ns:content-text>
    <ns:timestamp>2023-01-01T12:01:00</ns:timestamp>
  </ns:message>
</ns:export>
"""

@pytest.fixture
def sample_xml_file(tmp_path):
    xml_file = tmp_path / "sample.xml"
    xml_file.write_text(SAMPLE_XML)
    return xml_file

def test_parse_xml_data(sample_xml_file):
    questions, answers, total_question_length, total_answer_length, message_count = parse_xml_data(str(sample_xml_file))
    
    assert len(questions) == 1
    assert len(answers) == 1
    assert total_question_length == 13  # "これはテスト質問です" の長さ
    assert total_answer_length == 10  # "これはテスト回答です" の長さ
    assert message_count == 2

def test_sort_data_by_timestamp():
    unsorted_data = [
        {'Timestamp': '2023-01-01T12:01:00'},
        {'Timestamp': '2023-01-01T12:00:00'}
    ]
    sorted_data = sort_data_by_timestamp(unsorted_data)
    assert sorted_data[0]['Timestamp'] == '2023-01-01T12:00:00'
    assert sorted_data[1]['Timestamp'] == '2023-01-01T12:01:00'

def test_write_to_csv(tmp_path):
    data = [
        {'User ID': 'user1', 'Type': '質問', 'Text': 'これはテスト質問です', 'Length': 13, 'Timestamp': '2023-01-01T12:00:00'},
        {'User ID': '1443074843376353280', 'Type': '回答', 'Text': 'これはテスト回答です', 'Length': 10, 'Timestamp': '2023-01-01T12:01:00'}
    ]
    csv_file = tmp_path / "test_output.csv"
    write_to_csv(data, str(csv_file))
    
    assert csv_file.exists()
    content = csv_file.read_text()
    assert 'User ID,Type,Text,Length,Timestamp' in content
    assert 'user1,質問,これはテスト質問です,13,2023-01-01T12:00:00' in content
    assert '1443074843376353280,回答,これはテスト回答です,10,2023-01-01T12:01:00' in content

# 他のテストケースも同様に追加できます