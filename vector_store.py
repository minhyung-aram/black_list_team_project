def create_file(file_path, client):
    with open(file_path, "rb") as file_content:
        result = client.files.create(file=file_content, purpose="assistants")

    return result.id

def vector_store_with_file(file_path, store_name, client):
    # 벡터 스토어 생성
    vector_store = client.vector_stores.create(name=store_name)

    file_id = create_file(file_path, client)
    client.vector_stores.files.create(
        vector_store_id=vector_store.id,
        file_id=file_id
    )

    # 벡터 스토어 ID 반환
    return vector_store.id