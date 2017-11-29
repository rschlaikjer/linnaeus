import caffe
import numpy as np
import sys


class Classifier(object):

    def classify_image(self, fname):
        """
        Returns a map of class -> probability for image fname
        """
        # TODO: Conf file
        caffe_root = "/home/malcolm/Projects/caffe/"
        sys.path.insert(0, caffe_root + 'python')
        caffe.set_mode_cpu()
        model_def = caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
        model_weights = caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'
        net = caffe.Net(model_def,      # defines the structure of the model
                        model_weights,  # contains the trained weights
                        caffe.TEST)     # use test mode (e.g., don't perform dropout)

        # load the mean ImageNet image (as distributed with Caffe) for subtraction
        mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
        mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
        print 'mean-subtracted values:', zip('BGR', mu)
        
        # create transformer for the input called 'data'
        transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

        transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
        transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
        transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
        transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

        image = caffe.io.load_image(fname)
        transformed_image = transformer.preprocess('data', image)

        # copy the image data into the memory allocated for the net
        net.blobs['data'].data[...] = transformed_image

        ### perform classification
        output = net.forward()

        output_prob = output['prob'][0]  # the output probability vector for the first image in the batch

        labels_file = caffe_root + 'data/ilsvrc12/synset_words.txt'
        labels = np.loadtxt(labels_file, str, delimiter='\t')
        srtd = output_prob.argsort()
        top_ten = srtd[:-10:-1]
        ret = []
        for idx in top_ten:
            class_name = labels[idx]
            probability = output['prob'][0][idx]
            ret.append({
                "class_name": class_name,
                "probability": probability
            })
        # top_ten_labels = labels[srtd[:-10:-1]]
        return list(ret)
