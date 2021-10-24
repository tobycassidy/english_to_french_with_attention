import re 
import os 
import unicodedata
import zipfile


def preprocess_sentence(sent):
    sent = "".join([c for c in unicodedata.normalize('NFD', sent)
                   if unicodedata.category(c) != 'Mn'])
    sent = re.sub(r"([!.?])", r" \1", sent)
    sent = re.sub(r"[^a-zA-Z!.?]+", r" ", sent)
    sent = re.sub(r"\+s", r" ", sent)
    sent = sent.lower()
    return sent


def download_and_read_url(url, num_sent_pairs=1000):
    if not os.path.exists("data"):
        os.system("mkdir data")
    local_file = 'data/' + url.split('/')[-1]
    if not os.path.exists(local_file):
        os.system("wget -O {:s} {:s}".format(local_file, url))
        with zipfile.ZipFile(local_file, "r") as zip_ref:
            zip_ref.extractall("data/.")
    local_file = os.path.join("data", "fra.txt")
    en_sents, fr_sents_in, fr_sents_out = [], [], []
    with open(local_file, "r") as fin:
        for i, line in enumerate(fin):
            en_sent, fr_sent = line.strip().split('\t')[0], line.strip().split('\t')[1]
            en_sent = [w for w in preprocess_sentence(en_sent).split()]
            fr_sent = preprocess_sentence(fr_sent)
            fr_sent_in = [w for w in ("BOS " + fr_sent).split()]
            fr_sent_out = [w for w in (fr_sent + " EOS").split()]
            en_sents.append(en_sent)
            fr_sents_in.append(fr_sent_in)
            fr_sents_out.append(fr_sent_out)
            if i >= num_sent_pairs - 1:
                break
    return en_sents, fr_sents_in, fr_sents_out