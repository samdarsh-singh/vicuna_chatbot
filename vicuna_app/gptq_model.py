# gptq_model.py

from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model():
    # x = "AlekseyKorshuk/vicuna-7b"
    # x = "eachadea/legacy-ggml-vicuna-7b-4bit"
    x = "TheBloke/vicuna-7B-1.1-GPTQ-4bit-128g"

    tokenizer = AutoTokenizer.from_pretrained(x)
    model = AutoModelForCausalLM.from_pretrained(x)
    return model, tokenizer
#https://huggingface.co/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5