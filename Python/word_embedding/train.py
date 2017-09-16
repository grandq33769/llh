import logging
from gensim.models import word2vec


def main():

    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus("wiki_seg.txt")
    model = word2vec.Word2Vec(sentences, size=400, workers=6, iter=10, hs=1)

    # 保存模型，供日後使用
    model.save("med400.model.bin")

    # 模型讀取方式
    # model = word2vec.Word2Vec.load("your_model.bin")


if __name__ == "__main__":
    main()
