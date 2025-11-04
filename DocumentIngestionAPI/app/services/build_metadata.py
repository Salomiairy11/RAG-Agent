from datetime import datetime

def build_metadata(docs_to_index, filename):
    metadata_list = []
    for doc in docs_to_index:
        metadata_list.append(
            {
                "chunk_index": doc.metadata.get("chunk_index"),
                "chunk_strategy": doc.metadata.get("strategy"),
                "chunk_filename": filename,
                "created_at": datetime.now(),
            }
        )
    return metadata_list