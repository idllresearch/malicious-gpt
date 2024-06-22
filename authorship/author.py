from __future__ import print_function, division
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import KFold
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score, confusion_matrix
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
kfold_state_num = 64


categories = ["Davinci_002", "Davinci_003", "ChatGPT_3.5", "GPT_J", "Pygmalion_13B", "Luna_AI_Llama2_Uncensored"]

textdim = 384
codedim = 384


class AuthorshipClassification:
    def load(self):
        self.textdim = textdim
        self.codedim = codedim
        self.outdim = len(categories)

        self.classifier = self.build_classifier()
        self.classifier.trainable = True

        _textEmbedding = Input(shape=(1, self.textdim))
        _codeEmbedding = Input(shape=(1, self.codedim))

        prob = self.classifier([_textEmbedding, _codeEmbedding])
        self.final_model = Model(inputs=[_textEmbedding, _codeEmbedding], outputs=prob,
                                 name="Final_prediction")
        self.final_model.compile(loss=tf.keras.losses.CategoricalCrossentropy(),
                                 optimizer=Adam(learning_rate=0.001*2),
                                 metrics=['accuracy'])
        # self.final_model.summary()

    def build_classifier(self):
        textEmbedding = Input(shape=(1, self.textdim), name="textEmbed_input")
        codeEmbedding = Input(shape=(1, self.codedim), name="codeEmbed_input")

        textmodel = tf.keras.models.Sequential(
            [
                tf.keras.layers.Conv1D(256, 1, activation='relu'),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(256, activation="relu", name="text_dense0"),
                tf.keras.layers.Dense(128, activation="relu", name="text_dense1")
            ]
        )

        codemodel = tf.keras.models.Sequential(
            [
                tf.keras.layers.Conv1D(256, 1, activation='relu'),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(256, activation="relu", name="text_dense0"),
                tf.keras.layers.Dense(128, activation="relu", name="text_dense1")
            ]
        )

        mixmodel = tf.keras.models.Sequential(
            [
                tf.keras.layers.Conv1D(64, 2, activation='relu'),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(64, activation="relu", name="all_dense0"),
                tf.keras.layers.Dense(16, activation="relu", name="all_dense1"),
                tf.keras.layers.Dense(self.outdim, activation="softmax", name="all_dense2")
            ]
        )

        text_vec = textmodel(textEmbedding)
        code_vec = codemodel(codeEmbedding)
        mix_vec = tf.keras.layers.concatenate([text_vec, code_vec], axis=-2)
        classification_probs = mixmodel(mix_vec)

        model = Model(inputs=[textEmbedding, codeEmbedding],
                      outputs=classification_probs,
                      name="classifier")
        return model


def pred(saved_model, codevecfile=None, textvecfile=None):
    info_dict = {}
    with open(codevecfile, "r", encoding="utf8") as coderf:
        for line in coderf.readlines():
            line = json.loads(line)
            filename = line["filename"]
            vector = line["vector"]
            if filename not in info_dict:
                info_dict[filename] = {"codevec": [0 for _ in range(codedim)],
                                       "textvec": [0 for _ in range(textdim)]}
            info_dict[filename]["codevec"] = vector

    with open(textvecfile, "r", encoding="utf8") as textrf:
        for line in textrf.readlines():
            line = json.loads(line)
            filename = line["filename"]
            vector = line["vector"]
            if filename not in info_dict:
                info_dict[filename] = {"codevec": [0 for _ in range(codedim)],
                                       "textvec": [0 for _ in range(textdim)]}
            info_dict[filename]["textvec"] = vector

    X_code_matrix = []
    X_text_matrix = []
    filenames = []
    for filename in info_dict.keys():
        X_code_matrix.append(info_dict[filename]["codevec"])
        X_text_matrix.append(info_dict[filename]["textvec"])
        filenames.append(filename)
    X_code_matrix = np.expand_dims(np.array(X_code_matrix), axis=1)
    X_text_matrix = np.expand_dims(np.array(X_text_matrix), axis=1)

    final_model_fake = tf.keras.models.load_model(saved_model)
    result_matrix = final_model_fake.predict(x=[X_text_matrix, X_code_matrix])
    max_indices = np.argmax(result_matrix, axis=1).tolist()
    max_probs = np.max(result_matrix, axis=1).tolist()
    predicted_backend_names = [categories[model_index] for model_index in max_indices]
    return list(zip(filenames, predicted_backend_names, max_probs))


def train(saved_model, epoch=2, batch_size=64, codevecfile=None, textvecfile=None):
    X_code_matrix, X_text_matrix, y_matrix = dataload(codevecfile, textvecfile)

    authorship_classifier = AuthorshipClassification()
    authorship_classifier.load()
    final_model = authorship_classifier.final_model
    final_model.fit(
                x=[X_text_matrix, X_code_matrix],
                y=y_matrix,
                batch_size=batch_size,
                epochs=epoch,
                verbose=0,
                callbacks=None,
                validation_split=0.1,
                validation_data=None,
                shuffle=True,
                class_weight=None,
                sample_weight=None,
                initial_epoch=0,
                steps_per_epoch=None,
                validation_steps=None,
                validation_batch_size=None,
                validation_freq=1,
                max_queue_size=10,
                workers=1,
                use_multiprocessing=False
                )
    test_loss, test_acc = final_model.evaluate(
            x=[X_text_matrix, X_code_matrix],
            y=y_matrix,
            batch_size=batch_size,
            verbose=0,
            sample_weight=None,
            steps=None,
            callbacks=None,
            max_queue_size=10,
            workers=1,
            use_multiprocessing=False,
            return_dict=False,
        )
    print("test_loss: {}, test_acc: {}".format(test_loss, test_acc))
    final_model.save(saved_model, save_format="tf")


def dataload(codevecfile, textvecfile):
    info_dict = {}
    with open(textvecfile, "r", encoding="utf8") as textrf:
        for line in textrf.readlines():
            line = json.loads(line)
            filename = line["filename"]
            filename = ".".join(filename.split(".")[:-1])
            textvector = line["vector"]
            if filename not in info_dict:
                info_dict[filename] = {"codevec": [0 for _ in range(codedim)],
                                       "textvec": [0 for _ in range(textdim)]}
            info_dict[filename]["textvec"] = textvector

    with open(codevecfile, "r", encoding="utf8") as coderf:
        for line in coderf.readlines():
            line = json.loads(line)
            filename = line["filename"]
            filename = ".".join(filename.split(".")[:-1])
            codevector = line["vector"]
            info_dict[filename]["codevec"] = codevector

    X_code_matrix = []
    X_text_matrix = []
    labels, y_matrix, y_index_matrix = [], [], []
    for filename in info_dict.keys():
        assert len(info_dict[filename]["codevec"]) == codedim
        assert len(info_dict[filename]["textvec"]) == textdim
        X_code_matrix.append(info_dict[filename]["codevec"])
        X_text_matrix.append(info_dict[filename]["textvec"])
        labels.append(filename)

    for i in range(len(labels)):
        category_id = categories.index(labels[i].split("-", 1)[0])
        y_index_matrix.append(category_id)
        one_y_matrix = [0 for _ in range(len(categories))]
        one_y_matrix[category_id] = 1
        y_matrix.append(one_y_matrix)

    X_code_matrix = np.expand_dims(np.array(X_code_matrix), axis=1)
    X_text_matrix = np.expand_dims(np.array(X_text_matrix), axis=1)
    y_matrix = np.array(y_matrix)
    return X_code_matrix, X_text_matrix, y_matrix


def trainKFold(epoch=2, batch_size=64, codevecfile=None, textvecfile=None):
    X_code_matrix, X_text_matrix, y_matrix = dataload(codevecfile, textvecfile)

    losses, accuracies = [], []
    precisions, recalls = [], []
    kFold = KFold(n_splits=5, random_state=kfold_state_num, shuffle=True)
    for train_index, test_index in kFold.split(X_code_matrix):

        X_code_train, X_text_train = X_code_matrix[train_index], X_text_matrix[train_index]
        X_code_test, X_text_test =  X_code_matrix[test_index], X_text_matrix[test_index]
        y_train, y_test = y_matrix[train_index], y_matrix[test_index]

        authorship_classifier = AuthorshipClassification()
        authorship_classifier.load()
        final_model = authorship_classifier.final_model
        final_model.fit(
                    x=[X_text_train, X_code_train],
                    y=y_train,
                    batch_size=batch_size,
                    epochs=epoch,
                    verbose=0,
                    callbacks=None,
                    validation_split=0.1,
                    validation_data=None,
                    shuffle=True,
                    class_weight=None,
                    sample_weight=None,
                    initial_epoch=0,
                    steps_per_epoch=None,
                    validation_steps=None,
                    validation_batch_size=None,
                    validation_freq=1,
                    max_queue_size=10,
                    workers=1,
                    use_multiprocessing=False,
                    )
        test_loss, test_acc = final_model.evaluate(
                    x=[X_text_test, X_code_test],
                    y=y_test,
                    batch_size=batch_size,
                    verbose=0,
                    sample_weight=None,
                    steps=None,
                    callbacks=None,
                    max_queue_size=10,
                    workers=1,
                    use_multiprocessing=False,
                    return_dict=False,
                    )
        losses.append(test_loss)
        accuracies.append(test_acc)
        result = final_model.predict(x=[X_text_test, X_code_test])
        result_max_indices = np.argmax(result, axis=1).tolist()
        y_test_max_indices = np.argmax(y_test, axis=1).tolist()
        # print(confusion_matrix(result_max_indices, y_test_max_indices))
        test_prec = precision_score(result_max_indices, y_test_max_indices, average='macro')
        test_reca = recall_score(result_max_indices, y_test_max_indices, average='macro')
        precisions.append(test_prec)
        recalls.append(test_reca)
        del final_model
        del authorship_classifier

    print("5-Fold Validation Result:")
    print("5-fold accuracies: {:.2f}".format(sum(accuracies)/len(accuracies)))
    print("5-fold precisions: {:.2f}".format(sum(precisions) / len(precisions)))
    print("5-fold recalls: {:.2f}".format(sum(recalls) / len(recalls)))
    return sum(precisions) / len(precisions), sum(recalls) / len(recalls)


if __name__ == '__main__':
    start_K_Fold_validation = True
    start_authorship_identification = True
    use_pretrained_model = True

    # K-Fold validation
    if start_K_Fold_validation:
        prec, recall = trainKFold(epoch=50, batch_size=32,
                                  codevecfile="./data/codevec.json", textvecfile="./data/textvec.json")

    # Train model and predict
    if start_authorship_identification:
        if not use_pretrained_model:
            saved_model = "author_classify_model-retrain"
            train(saved_model, epoch=50, batch_size=32,
                  codevecfile="./data/codevec.json", textvecfile="./data/textvec.json")
        else:
            saved_model = "author_classify_model-raw"
        result = pred(saved_model, codevecfile="./data/test-codevec.json", textvecfile="./data/test_textvec.json")
        result_dict = {"DarkGPT": {LLM: 0 for LLM in categories},
                       "FreedomGPT": {LLM: 0 for LLM in categories},
                       "EscapeGPT": {LLM: 0 for LLM in categories},
                       }
        for piece in result:
            malla = piece[0].split("-")[1]
            if malla == "DarkGPT":
                result_dict["DarkGPT"][piece[1]] += 1
            elif malla == "FreedomGPT":
                result_dict["FreedomGPT"][piece[1]] += 1
            elif malla == "EscapeGPT":
                result_dict["EscapeGPT"][piece[1]] += 1
        DarkGPT_backend = sorted(result_dict["DarkGPT"].items(), key=lambda x: x[1], reverse=True)[0][0]
        FreedomGPT_backend = sorted(result_dict["FreedomGPT"].items(), key=lambda x: x[1], reverse=True)[0][0]
        EscapeGPT_backend = sorted(result_dict["EscapeGPT"].items(), key=lambda x: x[1], reverse=True)[0][0]
        print("Prediction result:")
        print(result_dict)
        print("Identified Backend:")
        print("Backends of DarkGPT -> {} \nBackends of FreedomGPT -> {} \nBackends of EscapeGPT ->"
              " {}.".format(DarkGPT_backend, FreedomGPT_backend, EscapeGPT_backend))
