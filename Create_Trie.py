import pandas as pd
import json


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.original_words = []

    def to_dict(self):
        return {
            'children': {k: v.to_dict() for k, v in self.children.items()},
            'is_end_of_word': self.is_end_of_word,
            'original_words': self.original_words
        }

    @classmethod
    def from_dict(cls, data):
        node = cls()
        node.is_end_of_word = data['is_end_of_word']
        node.original_words = data['original_words']
        node.children = {k: cls.from_dict(v) for k, v in data['children'].items()}
        return node


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        # Chèn từ vào Trie với chữ thường
        node = self.root
        lower_word = word.lower()
        for char in lower_word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        if word not in node.original_words:
            node.original_words.append(word)

    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.root.to_dict(), f)

    @classmethod
    def load_from_file(cls, filename):
        trie = cls()
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            trie.root = TrieNode.from_dict(data)
        return trie


def build_trie_from_dataframe(csv_filename, trie_filename):
    # Đọc dữ liệu từ tệp CSV vào DataFrame
    df = pd.read_csv(csv_filename)

    # Khởi tạo Trie
    trie = Trie()

    # Chèn các câu hỏi vào Trie
    for _, row in df.iterrows():
        question = row['Question']

        # Chèn câu hỏi vào Trie
        trie.insert(question)

    # Lưu Trie vào tệp
    trie.save_to_file(trie_filename)
    print(f"Trie đã được lưu vào {trie_filename}")


# Sử dụng hàm để xây dựng Trie và lưu vào tệp
csv_filename = 'text_chunks_and_embedding_df.csv'  # Thay đổi tên tệp CSV của bạn nếu cần
trie_filename = 'trie.json'
build_trie_from_dataframe(csv_filename, trie_filename)
