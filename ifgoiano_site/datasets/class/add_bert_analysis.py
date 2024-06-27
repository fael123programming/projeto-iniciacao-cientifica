import pandas as pd
import os
from transformers import AutoTokenizer, pipeline

tokenizer = AutoTokenizer.from_pretrained(
   pretrained_model_name_or_path='nlptown/bert-base-multilingual-uncased-sentiment'
)
analyse = pipeline(
   task='sentiment-analysis', 
   model='nlptown/bert-base-multilingual-uncased-sentiment'
)

if __name__ == '__main__':
   files = [file for file in os.listdir(os.getcwd()) if file.endswith('.csv')]
   max_length = 512
   for file in files:
      results = []
      df = pd.read_csv(file)
      df_slice = df[['titulo', 'descricao']]
      df_slice.loc[:, 'combined'] = df_slice['titulo'].str.cat(df_slice['descricao'], sep=' ').values
      values = df_slice['combined'].tolist()
      for value in values:
         tokens = tokenizer(
            value, 
            max_length=max_length, 
            padding=True, 
            truncation=True, 
            return_tensors="pt"
         )
         res = analyse(
            tokenizer.decode(
               tokens["input_ids"].squeeze().tolist(), 
               skip_special_tokens=True
            )
         )
         results.append(res[0])
      df['estrelas_bert'] = [int(res['label'].split(' ')[0]) for res in results]
      df['pontuacao_bert'] = [res['score'] for res in results]
      df.to_csv(file, index=False)



'''
# PyTorch, TensorFlow, BERT to sentiment analysis.
# Label: how many stars?
# Score: how closer to

BERT (Bidirectional Encoder Representations from Transformers) is a pre-trained natural language processing model developed by Google. It belongs to the transformer architecture family. Here's an overview of how pre-trained BERT models work:

1. Pre-training:
   - Unsupervised Learning: BERT is pre-trained using unsupervised learning on a massive amount of text data. During this phase, BERT learns to predict missing words in sentences. It does this by training on a masked language modeling (MLM) task, where some words in a sentence are randomly replaced with a special [MASK] token, and the model learns to predict these masked words.
   - Bidirectional Context: BERT differs from traditional language models by considering context from both left and right sides of a word. This bidirectional context allows BERT to capture richer semantic meaning.

2. Architecture:
   - Transformer Architecture: BERT utilizes the transformer architecture, which includes self-attention mechanisms to capture relationships between words in a sentence. This attention mechanism allows BERT to weigh the importance of different words based on their contextual relevance.

3. Layers and Attention Heads:
   - BERT consists of multiple layers, each with attention heads. Each layer captures different levels of abstraction, from low-level features to high-level semantic information.
   - Attention heads enable BERT to focus on different aspects of the input sentence simultaneously.

4. Tokenization:
   - BERT tokenizes input text into subwords or tokens. It uses WordPiece tokenization, breaking words into subword units.
   - Special tokens, such as [CLS] (classification) and [SEP] (separator), are added to the input to indicate the beginning and separation of sentences.

5. Fine-Tuning:
   - After pre-training, BERT can be fine-tuned for specific tasks, such as sentiment analysis, question answering, or named entity recognition. Fine-tuning involves training the model on a smaller dataset labeled for the target task.

6. Inference:
   - During inference, the pre-trained BERT model can be used as a feature extractor or as part of a larger model for downstream tasks. For example, in sentiment analysis, the [CLS] token's output may be used as a representation of the entire input sentence.

The pre-trained BERT model is powerful because it captures contextual relationships between words, allowing it to understand the nuances of language. Fine-tuning on task-specific datasets tailors the model to perform well on specific applications. The multilingual variant of BERT, as in the example you provided, is trained to understand and handle multiple languages.

'''