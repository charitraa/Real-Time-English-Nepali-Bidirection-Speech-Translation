# translator/translator.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from IndicTransToolkit.processor import IndicProcessor
import torch

class LocalTranslator:
    def __init__(self, model_dir="models"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.ip = IndicProcessor(inference=True)

        # Load models
        self.ne2en_tokenizer = AutoTokenizer.from_pretrained(f"{model_dir}/ne2en", trust_remote_code=True)
        self.ne2en_model = AutoModelForSeq2SeqLM.from_pretrained(f"{model_dir}/ne2en", trust_remote_code=True).to(self.device)

        self.en2ne_tokenizer = AutoTokenizer.from_pretrained(f"{model_dir}/en2ne", trust_remote_code=True)
        self.en2ne_model = AutoModelForSeq2SeqLM.from_pretrained(f"{model_dir}/en2ne", trust_remote_code=True).to(self.device)

    def translate_en_to_ne(self, text: str) -> str:
        src_lang = "eng_Latn"
        tgt_lang = "npi_Deva"

        batch = self.ip.preprocess_batch([text], src_lang=src_lang, tgt_lang=tgt_lang)
        inputs = self.en2ne_tokenizer(batch, truncation=True, padding="longest", return_tensors="pt", return_attention_mask=True).to(self.device)

        with torch.no_grad():
            generated = self.en2ne_model.generate(**inputs, use_cache=False, max_length=256, num_beams=5)

        decoded = self.en2ne_tokenizer.batch_decode(generated, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        return self.ip.postprocess_batch(decoded, lang=tgt_lang)[0]

    def translate_ne_to_en(self, text: str) -> str:
        src_lang = "npi_Deva"
        tgt_lang = "eng_Latn"

        batch = self.ip.preprocess_batch([text], src_lang=src_lang, tgt_lang=tgt_lang)
        inputs = self.ne2en_tokenizer(batch, truncation=True, padding="longest", return_tensors="pt", return_attention_mask=True).to(self.device)

        with torch.no_grad():
            generated = self.ne2en_model.generate(**inputs, use_cache=False, max_length=256, num_beams=5)

        decoded = self.ne2en_tokenizer.batch_decode(generated, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        return self.ip.postprocess_batch(decoded, lang=tgt_lang)[0]