'''
Date: 2017/08/24
Combine word cluster to raw data
'''
from llh.Python.project.input_data import raw_data, word_sim, word_cluster


def combine(num_cluster):
    '''
    Combine word cluster result to student data
    Return: Dict{sid: raw data}
    '''
    raws = raw_data()
    sims = word_sim()
    words, clusters = word_cluster(num_cluster)
    cluster = clusters.labels_
    for sid, datas in raws.items():
        cset = set()
        try:
            ans = sims[sid]
            for keyword in ans:
                cset.add(word2cluster(keyword, words, cluster))

        except KeyError:
            print('Null ID:', sid)
        for cno in range(num_cluster):
            value = str(cno + 1) + ':'
            if cno in cset:
                value += 'Y'
            else:
                value += 'N'
            datas.append(value)
    return raws


def word2cluster(word, words, cluster):
    '''
    Convert a word to specific cluster
    Return: Number of cluster
    '''
    try:
        index = words.index(word)
        cno = cluster[index]
    except ValueError:
        cno = -1

    return cno


if __name__ == '__main__':
    combine(20)
