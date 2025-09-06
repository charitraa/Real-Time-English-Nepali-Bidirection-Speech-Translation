# translate_from_local.py
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class LocalTranslator:
    def __init__(self, en2ne_path="models/en2ne", ne2en_path="models/ne2en"):
        # Load English -> Nepali
        self.en2ne_tokenizer = AutoTokenizer.from_pretrained(en2ne_path)
        self.en2ne_model = AutoModelForSeq2SeqLM.from_pretrained(en2ne_path)

        # Load Nepali -> English
        self.ne2en_tokenizer = AutoTokenizer.from_pretrained(ne2en_path)
        self.ne2en_model = AutoModelForSeq2SeqLM.from_pretrained(ne2en_path)

    def translate_en_to_ne(self, text: str) -> str:
        encoded = self.en2ne_tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=128
        )
        generated = self.en2ne_model.generate(**encoded, max_length=128)
        return self.en2ne_tokenizer.decode(generated[0], skip_special_tokens=True)

    def translate_ne_to_en(self, text: str) -> str:
        self.ne2en_tokenizer.src_lang = "ne_NP"
        encoded = self.ne2en_tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=128
        )
        generated = self.ne2en_model.generate(
            **encoded,
            forced_bos_token_id=self.ne2en_tokenizer.lang_code_to_id["en_XX"],
            max_length=128
        )
        return self.ne2en_tokenizer.decode(generated[0], skip_special_tokens=True)

