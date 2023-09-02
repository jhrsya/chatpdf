import pinecone
import json

def init_pinepone():
    # init pinepone
    with open("./api_key.json", "r") as f:
        fread = json.load(f)
        PINECONE_API_KEY = fread["PINECONE_API_KEY"]
        PINECONE_ENVIRONMENT = fread["PINECONE_ENVIRONMENT"]
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)




def make_sure_index_exist(index_name: str, dimension: int = 1536):
    """如果index_name不存在，则新建一个index"""
    if index_name not in pinecone.list_indexes():   # 不存在index_name
        # we create a new index
        pinecone.create_index(
            name=index_name,
            metric='dotproduct',
            dimension=dimension  # 1536 dim of text-embedding-ada-002
        )