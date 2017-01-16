import sys, os
import neural_network
# from vk_base import models
import json
import random
import math

from PIL import Image

def get_histogram(img, size):   
    histogramR = [] 
    histogramG = [] 
    histogramB = [] 
    for i in range(256):
        histogramR.append(0)
        histogramG.append(0)
        histogramB.append(0)        
    for i in range(size[0]):
        for j in range(size[1]):
            r, g, b = img.getpixel((i, j))
            histogramR[r] += 1
            histogramG[g] += 1
            histogramB[b] += 1
    histogram = []
    for i in range(256):
        histogramR[i] /= size[0]*size[1]
        histogramG[i] /= size[0]*size[1]
        histogramB[i] /= size[0]*size[1]
        histogram.append(histogramR[i])
        histogram.append(histogramG[i])
        histogram.append(histogramB[i])
    return histogram

def create_training_sets():
    image_paths = ['./autumn/', './summer/', './spring/', './winter/']
    imgList = {'image': []}
    size = 64, 64

    for season_idx, path in enumerate(image_paths):
        season = [0, 0, 0, 0]
        season[season_idx] = 1
        imageList = os.listdir(path)
        for inImage1 in imageList:
            img = Image.open(path + inImage1)
            img = img.convert(mode='RGB') 
            img = img.resize(size, Image.ANTIALIAS)
            histogram = get_histogram(img, size)
            obj = {
                'histogram': histogram,
                'season': season,
            }
            imgList['image'].append(obj)

    with open('training_set.json', 'w') as outfile:
        json.dump(imgList, outfile)


class NetworkInfo:
    num_inputs = 256*3
    num_hidden = 4
    num_outputs = 4

    hidden_layer_weights = None
    hidden_layer_bias = None
    output_layer_weights = None
    output_layer_bias = None

    total_error = 1

    is_read_file_error = False

    training_sets = []

    def __init__(self, is_train=False):
        self.get_training_sets()
        self.get_network_from_file(is_train)
    
    def get_training_sets(self):
        while True:
            try:
                with open('training_set.json') as json_data:
                    training_set = json.load(json_data)
                    for image in training_set['image']:
                        row = [image['histogram'], image['season']]
                        self.training_sets.append(row)       
                break
            except FileNotFoundError as error:
                create_training_sets()

    def get_network_from_file(self, is_train=False):
        network = None
        try:
            with open('network.json') as json_data:
                network = json.load(json_data)
        except FileNotFoundError as error:
            if not is_train:
                print(error)
                print('if you want create new neural-network run with key -t')
                self.is_read_file_error = True
        if network:
            self.num_hidden = network['hidden_layer']['count_neurons']    
            self.hidden_layer_bias = []
            self.hidden_layer_weights = []    
            for neuron in network['hidden_layer']['neurons']:
                self.hidden_layer_bias.append(neuron['bias'])
                for weight in neuron['weights']:
                    self.hidden_layer_weights.append(weight)
            
            self.output_layer_bias = []
            self.output_layer_weights = []    
            for neuron in network['output_layer']['neurons']:
                self.output_layer_bias.append(neuron['bias'])
                for weight in neuron['weights']:
                    self.output_layer_weights.append(weight)
            self.total_error = network['total_error']

def train(epsilon=0.001):
    network = NetworkInfo(is_train=True)    
    nn = neural_network.NeuralNetwork(
        num_inputs = network.num_inputs, 
        num_hidden = network.num_hidden, 
        num_outputs = network.num_outputs, 
        hidden_layer_weights = network.hidden_layer_weights, 
        hidden_layer_bias = network.hidden_layer_bias, 
        output_layer_weights = network.output_layer_weights, 
        output_layer_bias = network.output_layer_bias,
    )
    print('networ is get')
    total_error = network.total_error
    count = 0
    while total_error > epsilon:
        try:
            training_inputs, training_outputs = random.choice(network.training_sets)
            nn.train(training_inputs, training_outputs)
            outputs = nn.feed_forward(training_inputs)
            for i in range(len(outputs)):
                outputs[i] = round(outputs[i])

            if count == 1000:
                print(outputs, training_outputs)
                total_error = nn.calculate_total_error(network.training_sets)
                print('error = ', total_error)
                network_data = nn.inspect(network.training_sets)
                with open('network.json', 'w') as outfile:
                    json.dump(network_data, outfile)
                count = 0
            else:
                count += 1
        except Exception as e:
            print(e)
            network_data = nn.inspect(network.training_sets)
            with open('network.json', 'w') as outfile:
                json.dump(network_data, outfile)

    network_data = nn.inspect(network.training_sets)
    with open('network.json', 'w') as outfile:
        json.dump(network_data, outfile)
    print(json.dumps(network_data, sort_keys=True, indent=4, separators=(',', ': ')))
    print(nn.feed_forward(network.training_sets[0][0]))
    print('Total error: ', total_error)

def main(filepath = './ToTest/Kuindji_Rannyy_vesna.jpg'):
    size = 64, 64    

    network = NetworkInfo()
    if network.is_read_file_error:
        return
    nn = neural_network.NeuralNetwork(
        num_inputs = network.num_inputs, 
        num_hidden = network.num_hidden, 
        num_outputs = network.num_outputs, 
        hidden_layer_weights = network.hidden_layer_weights, 
        hidden_layer_bias = network.hidden_layer_bias, 
        output_layer_weights = network.output_layer_weights, 
        output_layer_bias = network.output_layer_bias,
    )
    # network_data = nn.inspect(network.training_sets)
    # print(json.dumps(network_data, sort_keys=True, indent=4, separators=(',', ': ')))
    # print(network.training_sets[0])

    img = Image.open(filepath)
    img.show()
    img = img.convert(mode='RGB') 
    img = img.resize(size, Image.ANTIALIAS)
    histogram = get_histogram(img, size)

    network_outputs = nn.feed_forward(histogram)
    answer_text = ['осень', 'лето', 'весна', 'зима']
    print('network_outputs:') 
    answer = []
    count = 0
    for indx, output in enumerate(network_outputs):
        print(answer_text[indx].title() + ':\t', output)
        if round(output) == 1:
            answer.append(indx)
    if len(answer) == 0:
        index = maxToIndex(network_outputs)
        print('Время года: наверное это', answer_text[index])
    elif len(answer) > 1:        
        index = maxOfOutputsToIndex(answer, network_outputs)
        print('Время года: скорее всего это', answer_text[index])
        for result in answer:
            if result != index:
                print('И это похоже на:', answer_text[result])
    else:        
        print('Время года: ', answer_text[answer[0]])

def maxToIndex(vList):
    max = 0
    indexOfMax = 0
    for indx, output in enumerate(vList):
        if output > max:
            max = output
            indexOfMax = indx  
    return indexOfMax

def maxOfOutputsToIndex(answer, network_outputs):
    max = 0
    indexOfMax = 0
    for output in answer:    
        if network_outputs[output] > max:
            max = network_outputs[output]
            indexOfMax = output  
    return indexOfMax
            

def help():
    print('Usage: python main.py [-h] [-t] [-f]')
    print('-t, --train [error]        train neural-network or create new (standart error = 0.0001)')
    print('-f, --file [file_path]       get image season')

if __name__ == "__main__":
    try:
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            sys.exit(help())
        if sys.argv[1] == '--file' or sys.argv[1] == '-f':
            try:
                sys.exit(main(sys.argv[2]))
            except IndexError as e:
                print(e)
                help()
                sys.exit()
        if sys.argv[1] == '--train' or sys.argv[1] == '-t':
            try:
                sys.exit(train(sys.argv[2]))
            except IndexError:
                sys.exit(train())
    except IndexError:
        sys.exit(main())