from sentence_transformers import SentenceTransformer, util
sentences = ["I'm full of happiness"]

sentences2 = ["I'm  ", "I'm full of happiness"]
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

#Compute embedding for both lists
embedding_1= model.encode(sentences[0], convert_to_tensor=True)
for i in sentences2:
  ij = model.encode(i, convert_to_tensor=True)
  print(util.pytorch_cos_sim(embedding_1, ij).item())
