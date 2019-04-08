import importlib

import src.Models as mdl
import numpy as np
import tensorflow as tf
import json

data_types = {'fashion_mnist': tf.keras.datasets.fashion_mnist, 'mnist': tf.keras.datasets.mnist,
              'cifar10': tf.keras.datasets.cifar10}
models = {"CW_1": mdl.CW_1, "CW_2": mdl.CW_2, "FGSM": mdl.FGSM}
train_mode = {"CTR": "encryptions.ctr", "CBC": "encryptions.cbc", "ECB": "encryptions.ecb",
              "PERMUTATED": "encryptions.permutated", "UNENCRYPTED": "encryptions.unencrypted"}


def main():
    data = data_types[DATASET]

    (x_train, y_train), (x_test, y_test) = data.load_data()
    x_train, x_test = x_train / 1.0, x_test / 1.0



    helper = importlib.import_module(train_mode[TRAIN_WITH_ME])

    dims = np.array(x_train).shape
    if len(dims) != 4:
        # expanding the images to get a third dimension (needed for conv layers)
        x_train = np.expand_dims(x_train, -1)
        x_test = np.expand_dims(x_test, -1)



    input_shape = np.array(x_train[0]).shape

    seed = 42

    '''
    num_of_examples = 3

    x_train = x_train[:num_of_examples]
    y_train = y_train[:num_of_examples]

    x_test = x_test[:num_of_examples]
    y_test = y_test[:num_of_examples]
    '''



    with tf.Session() as sess:
        x_train = [tf.reshape(tf.random.shuffle(tf.reshape(image, [-1]), seed=seed), tf.shape(image)) for image in
                   x_train]
        x_test = [tf.reshape(tf.random.shuffle(tf.reshape(image, [-1]), seed=seed), tf.shape(image)) for image in
                  x_test]

        x_train = sess.run(x_train)
        x_test = sess.run(x_test)

    x_train = np.array([img / 255.0 - 0.5 for img in x_train])
    x_test = np.array([img / 255.0 - 0.5 for img in x_test])




    # getting the desired model
    #    model = models[MODEL](input_shape, encrypt=helper.encrypt)

    model = models[MODEL](input_shape)

    # training
    loss, epoch_accs, epochs = model.train(x_train, y_train, ep=6)

    # evaluating
    model.compile()
    test_loss, test_acc = model.evaluate(x_test, y_test)

    r.write("{}\taccuracy: {:.2f}%\terror rate: {:.2f}%\n".format(MODEL_NAME, 100 * test_acc, (1.0 - test_acc) * 100))
    helper.print_encryption_details(out=r)
    r.write("#####################################################\n")

    results = {
        "name": MODEL_NAME,
        "acc": epoch_accs,
        "epochs": epochs
    }

    # writing the training results
    with open("json/{}_{}_models.json".format(DATASET, TRAIN_WITH_ME), 'a') as j:
        json.dump(results, j)
        j.write('\n')

    '''
    # writing the training results
    with open("json/{}_{}{}_models.json".format(DATASET, TRAIN_WITH_ME, VERSION), 'a') as j:
        json.dump(results, j)
        j.write('\n')
    '''

    # saving model
    model.save(MODEL_NAME)


'''
if __name__ == '__main__':
    # these two change to get desired model
    DATASET = "fashion_mnist"
    MODEL = "CW_2"
    TRAIN_WITH_ME = "ECB"
    VERSION = "_V2"

    for TRAIN_WITH_ME in ["CTR"]:
        for DATASET in ["mnist", "fashion_mnist"]:
            for MODEL in ["FGSM", "CW_1", "CW_2"]:

                MODEL_NAME = DATASET + "_" + MODEL + "_" + TRAIN_WITH_ME + VERSION

                print("DATASET = {}".format(DATASET))
                print("MODEL = {}".format(MODEL))
                print("TRAINER = {}\n".format(TRAIN_WITH_ME))

                r = open("../results", "a")
                main()
                r.close()

'''

if __name__ == '__main__':
    # DATASET = "mnist"
    MODEL = "CW_1"
    TRAIN_WITH_ME = "PERMUTATED"
    # VERSION = "_V2"
    r = open("results_permutated_0.5NORM_TENSORFLOW_PERMUTATED", "a")

    for DATASET in ["mnist", "fashion_mnist"]:
        MODEL_NAME = DATASET + "_" + MODEL + "_" + TRAIN_WITH_ME + "_0.5NORM_TENSORFLOW_PERMUTATED_SEED=42"  # + VERSION

        print("DATASET = {}".format(DATASET))
        print("MODEL = {}".format(MODEL))
        print("TRAINER = {}\n".format(TRAIN_WITH_ME))

        main()

    r.close()
