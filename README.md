# seasonsNNetwork
<meta charset="utf-8">
<h1>Classification of seasons</h1>
<h2>Run</h2>
<p>To determine the season in the image, go to the folder <i>neural-network</i> and run application with arguments <i><b>-f</i></b> or <i><b>--file</i></b>:</p>
<p><i><b>python seasons.py -f [path to image]</i></b></p>
<h2>Training a neural network</h2>
<p>To train a neural network you, go to the folder <i>neural-network</i> and run application with arguments <i><b>-t</i></b> or <i><b>--train</i></b>:</p>
<p><i><b>python seasons.py -t [путь до файла]</i></b></p>
<h2>Changing training set</h2>
<p>To changing training set you need to add or remove images in folder <i>neural-network/[season_name]</i>. Next remove file <i>neural-network/training_set.json</i> and run application with arguments <i><b>-t</i></b> or <i><b>--train</i></b>:</p>
<p><i><b>python seasons.py -t [ошибка]</i></b></p>
<p>Then wait for the error reaches the required value</p>
<h2>Create new neural network</h2>
<p>To create new neural networ remove file <i>neural-network/network.json</i> and run application with arguments <i><b>-t</i></b> or <i><b>--train</i></b>:</p>
<p><i><b>python seasons.py -t [ошибка]</i></b></p>
<p>Then wait for the error reaches the required value</p>
<h2>Help</h2>
<p>To view help information run application with arguments <i><b>-h</i></b> or <i><b>--help</i></b>:</p>
<p><i><b>python seasons.py -h</i></b></p>
<p>Help information:</p>
<p>Use: python main.py [-h] [-t] [-f]<br>
-t, --train [epsilon]        Training a neural network or create new (default epsilon is 0.0001)<br>
-f, --file [file_path]       Classification of seasons</p>
