from __future__ import print_function

'''
Given a sentence-aligned parallel corpus (i.e., two CQP corpora
with a suitable alignment attribute), write pairs of aligned
sentences (or sentence spans) in a suitable file.

Using the --eatt and --fatt attributes, you can select another
attribute rather than the word attribute to be used here.
'''

import sys
import optparse
from CWB.CL import Corpus

try:
    from pathconfig import load_configuration
    ctx = load_configuration('pynlp')
    CQP_REGISTRY = ctx.get_config_var('pycwb.cqp_registry')
except ImportError:
    CQP_REGISTRY = None
except KeyError:
    CQP_REGISTRY = None


class CorpusInfo:
    '''
    encapsulates information about a corpus
    '''

    def __init__(self, corpus_name):
        self.name = corpus_name
        self.corpus = Corpus(corpus_name, registry_dir=CQP_REGISTRY)
        self.words = self.corpus.attribute('word', 'p')
        self.sentences = self.corpus.attribute('s', 's')
        id_to_start = {}
        text_ids = self.corpus.attribute('file_id', 's')
        for start, end, fname in text_ids:
            id_to_start[fname] = start
        self.id_to_start = id_to_start

    def __getitem__(self, fname):
        return self.sentences.cpos2struc(self.id_to_start[fname])


def get_alignments(corpus1, corpus2,
                   att1='word', att2='word'):
    att_align = corpus1.corpus.attribute(corpus2.name.lower(), 'a')
    seq1 = corpus1.corpus.attribute(att1, 'p')
    seq2 = corpus2.corpus.attribute(att2, 'p')
    for start1, end1, start2, end2 in att_align:
        line1 = ' '.join(seq1[start1:end1 + 1])
        line2 = ' '.join(seq2[start2:end2 + 1])
        yield line1, line2


def maybe_write(fname):
    if fname is None:
        return None
    else:
        return open(fname, 'w')

oparse = optparse.OptionParser(usage='%prog CORPUS1 CORPUS2')
oparse.add_option('--e', dest='lang1_fname',
                  default=None)
oparse.add_option('--f', dest='lang2_fname',
                  default=None)
oparse.add_option('--ef', dest='both_fname',
                  default=None)
oparse.add_option('--eatt', dest='attr_e',
                  default='word')
oparse.add_option('--fatt', dest='attr_f',
                  default='word')


def main(argv=None):
    (opts, args) = oparse.parse_args(argv)
    if len(args) < 2:
        oparse.print_help()
        sys.exit(1)
    corpus1 = CorpusInfo(args[0])
    corpus2 = CorpusInfo(args[1])
    f_lang1 = maybe_write(opts.lang1_fname)
    f_lang2 = maybe_write(opts.lang2_fname)
    f_both = maybe_write(opts.both_fname)
    if f_lang1 is None and f_lang2 is None and f_both is None:
        f_both = sys.stdout
    for line1, line2 in get_alignments(corpus1, corpus2,
                                       att1=opts.attr_e,
                                       att2=opts.attr_f):
        if f_lang1 is not None:
            print(line1, file=f_lang1)
        if f_lang2 is not None:
            print(line2, file=f_lang2)
        if f_both is not None:
            print('{} ||| {}'.format(line1, line2), file=f_both)

if __name__ == '__main__':
    main()
