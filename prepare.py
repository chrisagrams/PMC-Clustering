import psycopg2
import numpy as np
import hdbscan
import umap
import pandas as pd
import json
from tqdm import tqdm


if __name__ == "__main__":
    conn = psycopg2.connect(
        host="localhost",
        database="embeddings",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT pmcid, front_embedding FROM pubmed_embeddings LIMIT 20000;")
    rows = cursor.fetchall()

    pmcids = []
    embeddings = []
    for row in tqdm(rows):
        if row[1] is not None:
            pmcid, embedding = row[0], json.loads(row[1])
            pmcids.append(pmcid)
            embeddings.append(embedding)
    embeddings = np.array(embeddings)

    clusterer = hdbscan.HDBSCAN(min_cluster_size=10)
    labels = clusterer.fit_predict(embeddings)

    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric='cosine')
    embedding_2d = reducer.fit_transform(embeddings)

    df = pd.DataFrame({
        'x': embedding_2d[:, 0],
        'y': embedding_2d[:, 1],
        'cluster': labels,
        'pmcid': pmcids
    })

    df.to_parquet('clustered_data_20000.parquet', index=False)
    print("Data saved to clustered_data_20000.parquet")
