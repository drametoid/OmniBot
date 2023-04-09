import spacy
import sys,fitz

nlp_model = spacy.load('../models/nlp_model')
fname = '../files/alice_clark.pdf'
doc = fitz.open(fname)
text = ""
for page in doc:
    text = text + str(page.getText())
tx = " ".join(text.split('\n'))
doc = nlp_model(tx)
for ent in doc.ents:
    print(f'{ent.label_.upper():{30}}- {ent.text}')
