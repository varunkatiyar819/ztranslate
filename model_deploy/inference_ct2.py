import sentencepiece as spm
import ctranslate2
from typing import List

class ModelInference:

    def __init__(self):
        # Load the trained SentencePiece models for source and target languages
        self.sp_source = spm.SentencePieceProcessor(model_file='./spm-en.model')
        self.sp_target = spm.SentencePieceProcessor(model_file='./spm-mr.model')

        # Load the CTranslate2 model
        self.translator = ctranslate2.Translator('./ct2_model/')

    def tokenize_input(self, text):
        # Tokenize the input text using SentencePiece
        tokens = self.sp_source.encode(text, out_type=str)
        return tokens

    def detokenize_output(self, tokens):
        # Detokenize the output tokens using SentencePiece
        text = self.sp_target.decode(tokens)
        return text

    def translate(self, tokens):
        # Perform translation using CTranslate2
        translation = self.translator.translate_batch(tokens)

        # translation = translator.translate_batch([tokens], num_hypotheses=3, beam_size=3)
        return [translation[idx].hypotheses[0] for idx, _ in enumerate(translation)]

    def batch_translate(self, raw_input: List[str]):
        # Tokenize the raw input using the source language SentencePiece model
        tokenized_input = self.tokenize_input(raw_input)

        # Translate the tokenized input
        translation_tokens = self.translate(tokenized_input)

        # Detokenize the translation using the target language SentencePiece model
        detokenized_translation = self.detokenize_output(translation_tokens)
        return detokenized_translation
