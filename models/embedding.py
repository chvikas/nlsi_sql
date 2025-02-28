import psycopg2
from sentence_transformers import SentenceTransformer

# Load local embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text, model):
    """
    Get a vector embedding for the given text using the SentenceTransformer model.
    
    Args:
        text (str): The text to embed
        model (SentenceTransformer): The SentenceTransformer model to use
        
    Returns:
        list: The embedding vector
    """
    if not text:
        return [0.0] * 384 if isinstance(text, str) else []
    
    try:
        # Get the embedding using the SentenceTransformer model
        embedding = model.encode(text.strip(), convert_to_tensor=False).tolist()
        return embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        # Return a zero vector in case of error
        return [0.0] * 384

def get_embedding_batch(texts, model, batch_size):
    """
    Get embeddings for a batch of texts using the SentenceTransformer model.
    
    Args:
        texts (list): List of texts to embed
        model (SentenceTransformer): The SentenceTransformer model to use
        batch_size (int): Maximum number of texts to process in a single batch
        
    Returns:
        list: List of embedding vectors
    """
    all_embeddings = []
    
    # Process in batches to avoid memory issues
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        valid_batch = [text.strip() for text in batch if text and text.strip() != ""]
        
        if not valid_batch:
            # If batch is empty, add zero vectors
            all_embeddings.extend([[0.0] * 384 for _ in range(len(batch))])
            continue
        
        try:
            # Get embeddings for the valid batch
            embeddings = model.encode(valid_batch, convert_to_tensor=False).tolist()
            
            # Map back to original positions, using zero vectors for invalid texts
            batch_embeddings = []
            embedding_idx = 0
            for text in batch:
                if text and text.strip() != "":
                    batch_embeddings.append(embeddings[embedding_idx])
                    embedding_idx += 1
                else:
                    batch_embeddings.append([0.0] * 384)
            
            all_embeddings.extend(batch_embeddings)
            
        except Exception as e:
            print(f"Error getting batch embeddings: {e}")
            # Return zero vectors for the entire batch in case of error
            all_embeddings.extend([[0.0] * 384 for _ in range(len(batch))])
    
    return all_embeddings