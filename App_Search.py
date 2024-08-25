import tkinter as tk
import json

#  Cấu trúc dữ liệu Trie
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.original_words = []  # Danh sách các từ gốc

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

    def search(self, prefix):
        node = self.root
        suggestions = []

        # Tìm đến node tương ứng với tiền tố
        for char in prefix:
            if char not in node.children:
                return suggestions
            node = node.children[char]

        # Duyệt các node con để tìm các từ hoàn chỉnh
        self._find_words(node, prefix, suggestions)
        return suggestions

    def _find_words(self, node, prefix, suggestions):
        if node.is_end_of_word:
            suggestions.extend(node.original_words)
        for char, child_node in node.children.items():
            self._find_words(child_node, prefix + char, suggestions)


# Đọc Trie từ tệp JSON
trie_filename = 'trie.json'
trie = Trie.load_from_file(trie_filename)


class TrieSearchApp:
    def __init__(self, root, trie):
        self.trie = trie
        self.root = root
        self.root.title("Trie Search Application")
        self.root.geometry("600x400")

        # Tạo giao diện người dùng
        self.create_widgets()

    def create_widgets(self):
        # Tạo thanh tìm kiếm
        self.search_label = tk.Label(self.root, text="Enter search:")
        self.search_label.pack(pady=10)

        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.update_suggestions)

        # Tạo danh sách gợi ý
        self.suggestion_listbox = tk.Listbox(self.root, width=80, height=10)
        self.suggestion_listbox.pack(pady=10)

    def update_suggestions(self, event):
        # Lấy tiền tố từ ô tìm kiếm và chuyển đổi thành chữ thường
        prefix = self.search_entry.get().strip().lower()

        # Tìm kiếm các câu hỏi liên quan trong Trie
        suggestions = self.trie.search(prefix)

        # Cập nhật danh sách gợi ý
        self.suggestion_listbox.delete(0, tk.END)
        for suggestion in suggestions[:10]:  # Hiển thị tối đa 10 gợi ý
            self.suggestion_listbox.insert(tk.END, suggestion)


# Khởi tạo giao diện
if __name__ == "__main__":
    root = tk.Tk()
    app = TrieSearchApp(root, trie)
    root.mainloop()
