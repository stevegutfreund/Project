import src.Models as mdl
import numpy as np
import tensorflow as tf
import json

data_types = {'fashion_mnist':tf.keras.datasets.fashion_mnist, 'mnist':tf.keras.datasets.mnist, 'cifar10':tf.keras.datasets.cifar10}
models = {"CW_1": mdl.CW_1(), "CW_2": mdl.CW_2(), "FGSM": mdl.FGSM()}


def main():
    data = data_types[DATASET]

    (x_train, y_train), (x_test, y_test) = data.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    dims = np.array(x_train).shape

    if len(dims) != 4:
        # expanding the images to get a third dimension (needed for conv layers)
        x_train = np.expand_dims(x_train, -1)
        x_test = np.expand_dims(x_test, -1)

    input_shape = np.array(x_train[0]).shape

    # getting the desired model
    model = models[MODEL]

    # building the networks' structure
    model.build(input_shape)

    # training
    loss, acc, epochs = model.train(x_train, y_train, ep=5)

    results = {
        "name": MODEL_NAME,
        "acc": acc,
        "epochs": epochs
    }

    # writing the training results
    with open("../unencrypted_{}_models.json".format(DATASET), 'a') as j:
        json.dump(results, j)
        j.write('\n')

    # evaluating
    model.compile()
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print("{0} {1} {2}\n".format(DATASET, MODEL, test_acc))
    r.write("{0} {1} {2}\n".format(DATASET, MODEL, test_acc))

    # saving model
    model.save(MODEL_NAME)


if __name__ == '__main__':
    # these two change to get desired model
    DATASET = "mnist"
    MODEL = "CW_2"

    MODEL_NAME = DATASET + "_" + MODEL + "_model"

    r = open("../results", "a")
    main()
    r.close()