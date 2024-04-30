import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
from googletrans import Translator

def translate_xml(input_path, output_path):
    tree = ET.parse(input_path)
    root = tree.getroot()
    translator = Translator()

    for entry in root.findall('.//entry'):
        original = entry.find('original')
        if original is not None and original.text:
            original_text = original.text
            # Translate the text using googletrans
            translated_text = translator.translate(original_text, src='it', dest='fr').text
            edited = entry.find('edited')
            if edited is None:
                edited = ET.SubElement(entry, 'edited')
            edited.text = translated_text

    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    messagebox.showinfo("Success", "Translation completed and saved to " + output_path)

def open_file_dialog(label):
    filename = filedialog.askopenfilename(filetypes=(("XML files", "*.xml"), ("All files", "*.*")))
    label.config(text=filename)
    return filename

def save_file_dialog(label):
    filename = filedialog.asksaveasfilename(filetypes=(("XML files", "*.xml"), ("All files", "*.*")))
    label.config(text=filename)
    return filename

def main():
    root = tk.Tk()
    root.title("XML Translator")

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    input_label = tk.Label(frame, text="Select input XML file", width=60, relief=tk.SUNKEN)
    input_label.pack(side=tk.TOP, padx=5, pady=5)
    input_button = tk.Button(frame, text="Browse...", command=lambda: open_file_dialog(input_label))
    input_button.pack(side=tk.TOP, padx=5, pady=5)

    output_label = tk.Label(frame, text="Select output XML file", width=60, relief=tk.SUNKEN)
    output_label.pack(side=tk.TOP, padx=5, pady=5)
    output_button = tk.Button(frame, text="Save As...", command=lambda: save_file_dialog(output_label))
    output_button.pack(side=tk.TOP, padx=5, pady=5)

    translate_button = tk.Button(frame, text="Translate", command=lambda: translate_xml(input_label['text'], output_label['text']))
    translate_button.pack(side=tk.TOP, padx=5, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
