from app.init_app import app
import numpy as np
import pandas as pd
import pickle
import os

import caffe

REPO_DIRNAME = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..')

def init_net(app):
    app.clf = ImagenetClassifier(**ImagenetClassifier.default_args)	

class ImagenetClassifier(object):
    default_args = {
        'model_def_file': (
            'model/deploy.prototxt'.format(REPO_DIRNAME)),
        'pretrained_model_file': (
            'model/bvlc_reference_caffenet.caffemodel'.format(REPO_DIRNAME)),
        'mean_file': (
            'model/ilsvrc_2012_mean.npy'.format(REPO_DIRNAME)),
        'class_labels_file': (
            'model/synset_words.txt'.format(REPO_DIRNAME)),
        'bet_file': (
            'model/imagenet.bet.pickle'.format(REPO_DIRNAME)),
    }
    for key, val in list(default_args.items()):
        if not os.path.exists(val):
            raise Exception(
                "File for {} is missing. Should be at: {}".format(key, val))
    default_args['image_dim'] = 227
    default_args['raw_scale'] = 255.

    def __init__(self, model_def_file, pretrained_model_file, mean_file,
                 raw_scale, class_labels_file, bet_file, image_dim, gpu_mode=False):
        self.net = caffe.Classifier(
            model_def_file, pretrained_model_file,
            image_dims=(image_dim, image_dim), raw_scale=raw_scale,
            mean=np.load(mean_file).mean(1).mean(1), channel_swap=(2, 1, 0)
        )
        with open(class_labels_file) as f:
            labels_df = pd.DataFrame([
                {
                    'synset_id': l.strip().split(' ')[0],
                    'name': ' '.join(l.strip().split(' ')[1:]).split(',')[0]
                }
                for l in f.readlines()
            ])
        self.labels = labels_df.sort_values('synset_id')['name'].values
        with open(bet_file, 'rb') as f:
            self.bet = pickle.load(f, encoding='latin1')

        # A bias to prefer children nodes in single-chain paths
        # I am setting the value to 0.1 as a quick, simple model.
        # We could use better psychological models here...

        self.bet['infogain'] -= np.array(self.bet['preferences']) * 0.1

    def classify_image(self, image):
        try:
            scores = self.net.predict([image], oversample=True).flatten()
            indices = (-scores).argsort()[:5]
            predictions = self.labels[indices]
            meta = [
                (p, '%.5f' % scores[i])
                for i, p in zip(indices, predictions)
            ]
            # Compute expected information gain		
            expected_infogain = np.dot(
                self.bet['probmat'], scores[self.bet['idmapping']])
            expected_infogain *= self.bet['infogain']
            # sort the scores
            infogain_sort = expected_infogain.argsort()[::-1]
            bet_result = [(self.bet['words'][v], '%.5f' % expected_infogain[v])
                for v in infogain_sort[:5]]
            return (True, meta, bet_result)

        except Exception as err:
            app.logger.debug('Classification error: %s', err)
            return (False, 'Something went wrong when classifying the '
                           'image. Maybe try another one?')