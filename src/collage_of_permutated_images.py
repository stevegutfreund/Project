import tensorflow as tf
import src.encryptions.permutated as e
import matplotlib.pyplot as plt


(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

num_of_classes = 10
num_of_examples_per_class = 10

dict = {i:[] for i in range(num_of_classes)}

counter = num_of_classes

for i,y in enumerate(y_train):
    if len(dict[y]) < num_of_examples_per_class:
        dict[y].append(i)
        if len(dict[y]) == num_of_examples_per_class:
            counter -= 1
    if counter == 0:
        break

rows = 10
columns = num_of_examples_per_class

for title in ["Original", "Permutated"]:
    fig = plt.figure()
    fig.suptitle(title)
    for i in range(rows * columns):
        ax = fig.add_subplot(rows, columns, i + 1)
        _class = int(i / num_of_examples_per_class)
        _example = i % num_of_examples_per_class
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        img = x_train[dict[_class][_example]]
        if title == "Permutated":
            img = e.encrypt(img)
        ax.imshow(img, cmap=plt.cm.binary)
        #ax.imshow(img)

plt.show()